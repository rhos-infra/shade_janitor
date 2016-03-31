#!/usr/bin/env python

import argparse
import datetime
import logging
import pprint
import pytz
import shade

from cleanup import cleanup_resources
from resources import Resources
from select_age import SelectAgeRelatedResources
from summary import Summary


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
    parser.add_argument(
        '--unused', dest='unused', action='store_true',
        help='select unused resources')

    return parser


def set_logging(debug_mode):
    if debug_mode:
        log_format = "%(asctime)-15s %(message)s"
        logging.basicConfig(format=log_format, level=logging.DEBUG)
        shade.simple_logging(debug=debug_mode)
    else:
        log_format = "%(message)s"
        logging.basicConfig(format=log_format, level=logging.INFO)

if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    now = datetime.datetime.now(pytz.utc)

    set_logging(args.debug)

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
                logging.info('Found Old instance [{}] created on [{}]'
                             ' age [{}]').format(
                    rec['name'], rec['created_on'], str(rec['age']))

        if oldest is not None:
            substring = new_search_prefix[0:15]
            resources.select_resources(substring)
            cleanup = resources.get_selection()
    if args.unused:

        resources.select_resources('')
        cleanup = resources.get_selection()
        resources = Resources(cloud)

        exclude_list = set(['public', 'provision'])
        dead_list = set()

        # TODO: identify better way to get unique substring from an instance
        if 'instances' in cleanup:
            for key in cleanup['instances']:
                exclude_list.add(cleanup['instances'][key]['name'][0:15])

        for type_key in cleanup:
            for key in cleanup[type_key]:
                entry = cleanup[type_key][key]
                if 'name' in entry:
                    name = entry['name']

                    skip_it = False
                    for rec in exclude_list:
                        if rec in name:
                            skip_it = True
                            break

                    if skip_it:
                        continue

                    # TODO: Special case in here for rhos- naming
                    if 'rhos-' == name[0:5]:
                        name = name[5:]

                    substr = name[0:15]
                    if substr not in exclude_list:
                        dead_list.add(substr)

        for substr in dead_list:
            resources.select_resources(substr)
        cleanup = resources.get_selection()

    if not args.old_instances and not args.unused:
        substring = args.substring or ''
        resources.select_resources(substring)
        cleanup = resources.get_selection()

    if len(cleanup) > 0:
        pp.pprint(cleanup)
        cleanup_resources(cloud, cleanup, dry_run=True)

        if args.run_cleanup:
            cleanup_resources(cloud, cleanup, dry_run=False)

    Summary.print_summary()
