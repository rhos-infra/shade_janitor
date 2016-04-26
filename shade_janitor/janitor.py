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
        description='Identify resources with options to show or do cleanup.')
    parser.add_argument(
        '--cloud', dest='cloud', help='cloud name to connect to')
    parser.add_argument(
        '--substring', dest='substring', help='name substring to search for')
    parser.add_argument(
        '--old', dest='old_instances', action='store_true',
        help='attempt to identify oldest instance to be purged')
    parser.add_argument(
        '--old-active', dest='old_active',
        default=8, type=int,
        help=('age (in hours, 0=never) after which ACTIVE servers'
              ' should be considered as old'))
    parser.add_argument(
        '--old-inactive', dest='old_inactive',
        default=1, type=int,
        help=('age (in hours, 0=never) after which SHUTOFF servers'
              ' should be considered as old'))
    parser.add_argument(
        '--old-permanent', dest='old_permanent',
        default=14, type=int,
        help=('age (in days, 0=never) after which even permanent labeled'
              ' servers should be considered as old'))
    parser.add_argument(
        '--cleanup', dest='run_cleanup', action='store_true',
        help='attempt to do cleanup selected resources')
    parser.add_argument(
        '--debug', dest='debug', action='store_true',
        help='turn on debug')
    parser.add_argument(
        '--unused', dest='unused', action='store_true',
        help='select unused network resources')
    parser.add_argument(
        '--dryrun', dest='dryrun', action='store_true',
        help='show dry run cleanup commands for selected resources')
    parser.add_argument(
        '--quiet', '-q', dest='quiet', action='store_true',
        help='quiet down the output for normal runs')

    return parser


def set_logging(debug_mode):
    if debug_mode:
        log_format = "%(asctime)-15s %(message)s"
        logging.basicConfig(format=log_format, level=logging.DEBUG)
        shade.simple_logging(debug=debug_mode)
    else:
        log_format = "%(message)s"
        logging.basicConfig(format=log_format, level=logging.INFO)


# TODO(jmls): identify better way to get unique substring
def get_substr_from_name(resource_name):
    return resource_name[0:15]


def select_oldest(cloud, args):
    if cloud and args is not None:
        resources = Resources(cloud)
        age_resources = SelectAgeRelatedResources(cloud)
        age_resources.select_old_instances(
            datetime.timedelta(hours=args.old_active),
            datetime.timedelta(hours=args.old_inactive),
            datetime.timedelta(days=args.old_permanent)
        )
        old_resources = age_resources.get_selection()
        new_search_prefix = None
        oldest = None
        if 'instances' in old_resources:
            for instance in old_resources['instances']:
                rec = old_resources['instances'][instance]
                if rec is None:
                    continue
                if oldest is None or oldest > rec['created_on']:
                    oldest = rec['created_on']
                    new_search_prefix = rec['name']
                logging.info('Found Old instance [{}] created on [{}] age [{}]'
                             .format(rec['name'],
                                     rec['created_on'],
                                     str(rec['age'])))

        if oldest is not None:
            substring = get_substr_from_name(new_search_prefix)
            resources.select_resources(substring)
        return resources
    return None


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
        resources = select_oldest(cloud, args)
        cleanup = resources.get_selection()
        resources = Resources(cloud)

    if args.unused:
        resources.select_resources('')
        cleanup = resources.get_selection()

        logging.info('attempting cleanup of unused network resources')
        exclude_list = set(['public', 'provision'])
        dead_list = set()

        if 'instances' in cleanup:
            for key in cleanup['instances']:
                sub = get_substr_from_name(cleanup['instances'][key]['name'])
                exclude_list.add(sub)
        logging.debug("exclude list {}".format(str(exclude_list)))
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

                    # TODO(jmls): Special case in here for rhos- naming
                    if 'rhos-' == name[0:5]:
                        name = name[5:]

                    substr = get_substr_from_name(name)
                    if substr not in exclude_list:
                        dead_list.add(substr)
        logging.info('identified possible unused {}'.format(dead_list))

        for substr in dead_list:
            logging.info('cleaning up {}'.format(substr))
            resources = Resources(cloud)
            resources.select_resources(substr)
            cleanup = resources.get_selection()
            if 'instances' in cleanup and len(cleanup['instances']) > 0:
                logging.info('skipping as instances are live on here')
                continue
            if 'fips' in cleanup and len(cleanup['fips']) > 0:
                logging.info('skipping as there are floating ips live on here')
                continue

            resources_selected_str = pp.pformat(cleanup)
            logging.debug(resources_selected_str)

            if args.dryrun:
                cleanup_resources(cloud, cleanup, dry_run=True)
            if args.run_cleanup:
                try:
                    cleanup_resources(cloud, cleanup, dry_run=False)
                except shade.exc.OpenStackCloudException as e:
                    logging.error(
                        'We had a problem trying to clean up [{}]'
                        .format(substr))
                    logging.error(e)

    if not args.old_instances and not args.unused:
        substring = args.substring or ''
        resources.select_resources(substring)
        cleanup = resources.get_selection()

    if len(cleanup) > 0:
        resources_selected_str = pp.pformat(cleanup)
        if not args.quiet:
            logging.info(resources_selected_str)
        else:
            logging.debug(resources_selected_str)

        if args.dryrun:
            cleanup_resources(cloud, cleanup, dry_run=True)

        if args.run_cleanup:
            cleanup_resources(cloud, cleanup, dry_run=False)

    Summary.print_summary()
    if not args.run_cleanup:
        logging.info("Nothing cleaned up. To cleanup resources, "
                     "please use --cleanup")
