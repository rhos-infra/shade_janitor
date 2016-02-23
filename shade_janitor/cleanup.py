#!/usr/bin/env python


def cleanup_resources(cloud, resource_selection, dry_run=True):
    if 'instances' in resource_selection:
        for uuid in resource_selection['instances']:
            if dry_run:
                print('nova delete {}'.format(uuid))
            else:
                cloud.delete_server(uuid, wait=True, delete_ips=True)

    if 'router_interfaces' in resource_selection:
        router_ids = []
        subnet_ids = []
        if 'routers' in resource_selection:
            for r_uuid in resource_selection['routers']:
                router_ids.append(r_uuid)
        for uuid in resource_selection['router_interfaces']:
            subs = resource_selection['router_interfaces'][uuid]['subnet_ids']
            subnet_ids.extend(subs)

        for r_uuid in router_ids:
            for uuid in subnet_ids:
                if dry_run:
                    print(
                        'neutron router-interface-delete {0} {1}'.format(
                            r_uuid, uuid))
                else:
                    for router in cloud.search_routers(r_uuid):
                        cloud.remove_router_interface(router, uuid)

    if 'ports' in resource_selection:
        for uuid in resource_selection['ports']:
            if dry_run:
                print('neutron port-delete {}'.format(uuid))
            else:
                cloud.delete_port(uuid)

    if 'subnets' in resource_selection:
        for uuid in resource_selection['subnets']:
            if dry_run:
                print('neutron subnet-delete {}'.format(uuid))
            else:
                cloud.delete_subnet(uuid)

    if 'nets' in resource_selection:
        for uuid in resource_selection['nets']:
            if dry_run:
                print('neutron net-delete {}'.format(uuid))
            else:
                cloud.delete_network(uuid)

    if 'routers' in resource_selection:
        for uuid in resource_selection['routers']:
            if dry_run:
                print('neutron router-delete {}'.format(uuid))
            else:
                cloud.delete_router(uuid)

    if 'fips' in resource_selection:
        for uuid in resource_selection['fips']:
            if dry_run:
                print('neutron floatingip-delete {}'.format(uuid))
            else:
                cloud.delete_floating_ip(uuid)
