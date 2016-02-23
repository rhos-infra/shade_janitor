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

    pp.pprint(cleanup)
    cleanup_resources(cloud, cleanup, dry_run=True)

    if args.run_cleanup:
        cleanup_resources(cloud, cleanup, dry_run=False)

#    if args.run_cleanup:
#        nova = auth['nova']
#        if 'instances' in cleanup:
#            instance_list = nova.servers.list()
#            for uuid in cleanup['instances']:
#                if cleanup['instances'][uuid] is not None and 'name' in cleanup['instances'][uuid]:
#                    for instance in instance_list:
#                        if instance.id == uuid:
#                            print "attempting to delete {} instance".format(instance.id)
#                            instance.delete()
#
#        neutron = auth['neutron']
#        if 'ports' in cleanup:
#            for uuid in cleanup['ports']:
#                if cleanup['ports'][uuid] is not None and 'name' in cleanup['ports'][uuid]:
#                    print 'attempting port-delete {}'.format(uuid)
#                    neutron.delete_port(uuid)
#
#        if 'router_interfaces' in cleanup and False:
#            for uuid in cleanup['router_interfaces']:
#                rec = cleanup['router_interfaces'][uuid]
#                router_map_list = neutron.list_routers()
#                for router in router_map_list['routers']:
#                    print router
#                    neutron.remove_interface_router(router,rec['subnet_id'])
#
#        if 'subnets' in cleanup:
#            for uuid in cleanup['subnets']:
#                if cleanup['subnets'][uuid] is not None and 'name' in cleanup['subnets'][uuid]:
#                    print 'attempting subnet-delete {}'.format(uuid)
#                    neutron.delete_subnet(uuid)
#
#        if 'nets' in cleanup:
#            for uuid in cleanup['nets']:
#                if cleanup['nets'][uuid] is not None and 'name' in cleanup['nets'][uuid]:
#                    print 'attempting net-delete {}'.format(uuid)
#                    neutron.delete_network(uuid)
#
#        if 'routers' in cleanup:
#            for uuid in cleanup['routers']:
#                if cleanup['routers'][uuid] is not None and 'name' in cleanup['routers'][uuid]:
#                    print 'attempting router-delete {}'.format(uuid)
#                    neutron.delete_router(uuid)
