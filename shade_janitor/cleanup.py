#!/usr/bin/env python


def cleanup_instances(cloud, instances):
    """Cleanup instances."""
    for uuid in instances:
        cloud.delete_server(uuid, wait=True, delete_ips=True)


def dry_cleanup_instances(instances):
    """Dry cleanup of instances."""
    for uuid in instances:
        print('nova delete {}'.format(uuid))


def dry_cleanup_router_interfaces(routers_id, subnets_id):
    """Dry cleanup of router interfaces."""
    for r_uuid in routers_id:
        for uuid in subnets_id:
            print('neutron router-interface-delete {0} {1}'.format(
                r_uuid, uuid))


def cleanup_router_interfaces(cloud, routers_id, subnets_id):
    """Cleanup router interfaces."""
    for r_uuid in routers_id:
        for uuid in subnets_id:
            for router in cloud.search_routers(r_uuid):
                cloud.remove_router_interface(router, uuid)


def setup_router_interfaces_cleanup(routers, router_interfaces, dry_run):
    """Setup router interfaces cleanup."""
    routers_id = []
    subnets_id = []
    for r_uuid in routers:
        routers_id.append(r_uuid)
    for uuid in router_interfaces:
        subs = router_interfaces[uuid]['subnet_ids']
        subnets_id.extend(subs)
    return routers_id, subnets_id
    if dry_run:
        dry_cleanup_router_interfaces(routers_id, subnets_id)
    else:
        cleanup_router_interfaces(routers_id, subnets_id)


def cleanup_ports(cloud, ports):
    """Cleanup ports."""
    for uuid in ports:
        cloud.delete_ports(uuid)


def dry_cleanup_ports(ports):
    """Dry cleanup of ports."""
    for uuid in ports:
        print('neutron port-delete {}'.format(uuid))


def cleanup_subnets(cloud, subnets):
    """Cleanup subnets."""
    for uuid in subnets:
        cloud.delete_subnet(uuid)


def dry_cleanup_subnets(subnets):
    """Dry cleanup of subnets."""
    for uuid in subnets:
        print('neutron subnet-delete {}'.format(uuid))


def cleanup_networks(cloud, networks):
    """Cleanup networks."""
    for uuid in networks:
        cloud.delete_network(uuid)


def dry_cleanup_networks(networks):
    """Dry cleanup of networks."""
    for uuid in networks:
        print('neutron net-delete {}'.format(uuid))


def cleanup_routers(cloud, routers):
    """Cleanup routers."""
    for uuid in routers:
        cloud.delete_router(uuid)


def dry_cleanup_routers(routers):
    """Dry cleanup of routers."""
    for uuid in routers:
        print('neutron router-delete {}'.format(uuid))


def cleanup_floating_ips(cloud, floating_ips):
    """Cleanup floating IPs."""
    for uuid in floating_ips:
        cloud.delete_floating_ip(uuid)


def dry_cleanup_floating_ips(floating_ips):
    """Dry cleanup of floating IPs."""
    for uuid in floating_ips:
        print('neutron floatingip-delete {}'.format(uuid))


def cleanup_resources(cloud, resource_selection, dry_run=True):
    """Cleanup resources

    :param cloud: the cloud object.
    :param resource_selection: selected resources intended for a cleanup.
    :param dry_run: indicates if a real cleanup will run or a simulation.
    """
    if dry_run:
        if 'instances' in resource_selection:
            dry_cleanup_instances(resource_selection['instances'])
        if 'router_interfaces' in resource_selection:
            routers_id, subnets_id = setup_router_interfaces_cleanup(
                resource_selection['routers'],
                resource_selection['router_interfaces'],
                dry_run)
            dry_cleanup_router_interfaces(routers_id, subnets_id)
        if 'ports' in resource_selection:
            dry_cleanup_ports(resource_selection['ports'])
        if 'subnets' in resource_selection:
            dry_cleanup_subnets(resource_selection['subnets'])
        if 'nets' in resource_selection:
            dry_cleanup_networks(resource_selection['nets'])
        if 'routers' in resource_selection:
            dry_cleanup_routers(resource_selection['routers'])
        if 'fips' in resource_selection:
            dry_cleanup_floating_ips(resource_selection['fips'])
        print("Nothing cleaned up!")
    else:
        if 'instances' in resource_selection:
            cleanup_instances(cloud, resource_selection['instances'])
        if 'router_interfaces' in resource_selection:
            routers_id, subnets_id = setup_router_interfaces_cleanup(
                resource_selection['routers'],
                resource_selection['router_interfaces'])
            cleanup_router_interfaces(cloud, routers_id, subnets_id)
        if 'ports' in resource_selection:
            cleanup_ports(cloud, resource_selection['ports'])
        if 'subnets' in resource_selection:
            cleanup_subnets(cloud, resource_selection['subnets'])
        if 'nets' in resource_selection:
            cleanup_networks(cloud, resource_selection['nets'])
        if 'routers' in resource_selection:
            cleanup_routers(cloud, resource_selection['routers'])
        if 'fips' in resource_selection:
            cleanup_floating_ips(cloud, resource_selection['fips'])
