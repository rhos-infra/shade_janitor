#!/usr/bin/env python

import shade
from select_related import SelectRelatedResources
from cleanup import cleanup_resources
import pprint
import datetime
import pytz

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Identify resources to be cleaned up.')
    parser.add_argument(
        '--cloud', dest='cloud', help='cloud name to connect to')
    parser.add_argument(
        '--substring', dest='substring', help='name substring to search for')
    parser.add_argument(
        '--old', dest='old_instances', action='store_true', help='attempt to identify old instances')
    parser.add_argument(
        '--cleanup', dest='run_cleanup', action='store_true', help='attempt to do cleanup')

    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    now = datetime.datetime.now(pytz.utc)

    # Initialize and turn on debug logging
    shade.simple_logging(debug=True)

    # Initialize cloud
    # Cloud configs are read with os-client-config
    cloud = shade.openstack_cloud(cloud=args.cloud)

    resources = SelectRelatedResources(cloud)
    cleanup = {}

#    if args.old_instances:
#        for instance in cloud.server_list():
#        resources.select_instances_name_substring(args.prefix)
#        resources.select_networks_name_substring(args.prefix)
#        resources.select_subnets_name_substring(args.prefix)
#        resources.select_routers_name_substring(args.prefix)
#        resources.select_related_ports()
#
#        cleanup_old = identify_old_instances(args.prefix, auth, cleanup)
#        oldest = None
#        new_search_prefix = None
#        for instance in cleanup_old['instances']:
#            rec = cleanup_old['instances'][instance]
#            print rec
#            if oldest is None or oldest > rec['created_on']:
#                oldest = rec['created_on']
#                new_search_prefix = rec['name']
#                print (oldest, new_search_prefix, rec['age'])
#
#        if oldest is not None:
#            print (oldest, new_search_prefix, new_search_prefix[0:15])
#            cleanup = identify_network_resources(new_search_prefix[0:15], auth, cleanup)
#
#    else:
    if True:
        substring = args.substring
        if substring is None:
            substring = ''
        resources.select_instances_name_substring(substring)
        resources.select_networks_name_substring(substring)
        resources.select_subnets_name_substring(substring)
        resources.select_routers_name_substring(substring)
        resources.select_related_ports()
        resources.select_floatingips_unattached()

        cleanup = resources.get_selection()

    if len(cleanup) > 0:
        pp.pprint(cleanup)
        cleanup_resources(cloud, cleanup, dry_run=True)

        if args.run_cleanup:
            cleanup_resources(cloud, cleanup, dry_run=False)
