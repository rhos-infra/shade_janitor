#!/usr/bin/env python

import argparse
import datetime
import pprint
import pytz
import shade

from cleanup import cleanup_resources
from resources import Resources
from select_age import SelectAgeRelatedResources


def initialize_cloud(cloud_name):
    """Initialize cloud object.

       Cloud configs are read with os-client-config.

    :param cloud_name: the cloud name
    """

    if not cloud_name:
        return shade.openstack_cloud()
    else:
        return shade.openstack_cloud(cloud=cloud_name)


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description='Identify resources to be cleaned up.')
    parser.add_argument(
        '--cloud', dest='cloud', help='cloud name to connect to')
    parser.add_argument(
        '--substring', dest='substring', help='name substring to search for')
    parser.add_argument(
        '--old', dest='old_instances', action='store_true',
        help='attempt to identify old instances')
    parser.add_argument(
        '--cleanup', dest='run_cleanup', action='store_true',
        help='attempt to do cleanup')
    parser.add_argument(
        '--debug', dest='debug', action='store_true',
        help='turn on debug')

    return parser


def set_debug(debug_mode):
    if debug_mode:
        shade.simple_logging(debug=debug_mode)

if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    now = datetime.datetime.now(pytz.utc)

    set_debug(args.debug)

    cloud = initialize_cloud(args.cloud)

    resources = Resources(cloud)
    cleanup = {}

    if args.old_instances:
        age_resources = SelectAgeRelatedResources(cloud)
        age_resources.select_old_instances()
        old_resources = age_resources.get_selection()
        new_search_prefix = None
        oldest = None
        if 'instances' in old_resources:
            for instance in old_resources['instances']:
                rec = old_resources['instances'][instance]
                if oldest is None or oldest > rec['created_on']:
                    oldest = rec['created_on']
                    new_search_prefix = rec['name']
                print(('Found Old instance [{}] created on [{}]'
                      ' age [{}]').format(
                    rec['name'], rec['created_on'], str(rec['age'])))

        if oldest is not None:
            substring = new_search_prefix[0:15]
            resources.select_resources(substring)
            cleanup = resources.get_selection()

    else:
        substring = args.substring or ''
        resources.select_resources(substring)
        cleanup = resources.get_selection()

    if len(cleanup) > 0:
        pp.pprint(cleanup)
        cleanup_resources(cloud, cleanup, dry_run=True)

        if args.run_cleanup:
            cleanup_resources(cloud, cleanup, dry_run=False)
