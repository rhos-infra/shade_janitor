#!/usr/bin/env python


def cleanup_resources(cloud, resource_selection, dry_run=True):
    if 'instances' in resource_selection:
        for uuid in resource_selection['instances']:
            print('nova delete {}'.format(uuid))

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
                print(
                    'neutron router-interface-delete {0} {1}'.format(
                        r_uuid, uuid))

    if 'ports' in resource_selection:
        for uuid in resource_selection['ports']:
            print('neutron port-delete {}'.format(uuid))

    if 'subnets' in resource_selection:
        for uuid in resource_selection['subnets']:
            print('neutron subnet-delete {}'.format(uuid))

    if 'nets' in resource_selection:
        for uuid in resource_selection['nets']:
            print('neutron net-delete {}'.format(uuid))

    if 'routers' in resource_selection:
        for uuid in resource_selection['routers']:
            print('neutron router-delete {}'.format(uuid))

    if 'fips' in resource_selection:
        for uuid in resource_selection['fips']:
            print('neutron floatingip-delete {}'.format(uuid))
