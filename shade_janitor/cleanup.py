#!/usr/bin/env python

import logging

from summary import Summary


def show_cleanup(cleanup_cmd):
    logging.info(cleanup_cmd)


def cleanup_instances(cloud, instances):
    """Cleanup instances."""
    for uuid in instances:
        Summary.num_of_instances += 1
        cloud.delete_server(uuid, wait=True, delete_ips=True)


def dry_cleanup_instances(instances):
    """Dry cleanup of instances."""
    for uuid in instances:
        Summary.num_of_instances += 1
        show_cleanup('nova delete {}'.format(uuid))


def cleanup_stacks(cloud, stacks):
    """Cleanup stacks."""
    for uuid in stacks:
        Summary.num_of_stacks += 1
        cloud.delete_stack(uuid)


def dry_cleanup_stacks(stacks):
    """Dry cleanup of stacks."""
    for uuid in stacks:
        Summary.num_of_stacks += 1
        show_cleanup('heat stack-delete {}'.format(uuid))


def cleanup_ports(cloud, ports):
    """Cleanup ports."""
    for uuid in ports:
        Summary.num_of_ports += 1
        cloud.delete_port(uuid)


def dry_cleanup_ports(ports):
    """Dry cleanup of ports."""
    for uuid in ports:
        Summary.num_of_ports += 1
        show_cleanup('neutron port-delete {}'.format(uuid))


def cleanup_subnets(cloud, subnets):
    """Cleanup subnets."""
    for uuid in subnets:
        Summary.num_of_subnets += 1
        cloud.delete_subnet(uuid)


def dry_cleanup_subnets(subnets):
    """Dry cleanup of subnets."""
    for uuid in subnets:
        Summary.num_of_subnets += 1
        show_cleanup('neutron subnet-delete {}'.format(uuid))


def cleanup_networks(cloud, networks):
    """Cleanup networks."""
    for uuid in networks:
        Summary.num_of_networks += 1
        cloud.delete_network(uuid)


def dry_cleanup_networks(networks):
    """Dry cleanup of networks."""
    for uuid in networks:
        Summary.num_of_networks += 1
        show_cleanup('neutron net-delete {}'.format(uuid))


def cleanup_routers(cloud, routers):
    """Cleanup routers."""
    for uuid in routers:
        Summary.num_of_routers += 1
        cloud.delete_router(uuid)


def dry_cleanup_routers(routers):
    """Dry cleanup of routers."""
    for uuid in routers:
        Summary.num_of_routers += 1
        show_cleanup('neutron router-delete {}'.format(uuid))


def cleanup_floating_ips(cloud, floating_ips):
    """Cleanup floating IPs."""
    for uuid in floating_ips:
        Summary.num_of_floating_ips += 1
        cloud.delete_floating_ip(uuid)


def dry_cleanup_floating_ips(floating_ips):
    """Dry cleanup of floating IPs."""
    for uuid in floating_ips:
        Summary.num_of_floating_ips += 1
        show_cleanup('neutron floatingip-delete {}'.format(uuid))


def cleanup_keypairs(cloud, keypairs):
    """Cleanup keypairs."""
    for uuid in keypairs:
        Summary.num_of_keypairs += 1
        cloud.delete_keypair(keypairs[uuid]['name'])


def dry_cleanup_keypairs(keypairs):
    """Dry cleanup keypairs."""
    for uuid in keypairs:
        Summary.num_of_keypairs += 1
        show_cleanup('nova keypair-delete {}'.format(keypairs[uuid]['name']))


def cleanup_resources(cloud, resource_selection, dry_run=True):
    """Cleanup resources

    :param cloud: the cloud object.
    :param resource_selection: selected resources intended for a cleanup.
    :param dry_run: indicates if a real cleanup will run or a simulation.
    """
    if dry_run:
        if 'instances' in resource_selection:
            dry_cleanup_instances(resource_selection['instances'])
    else:
        if 'instances' in resource_selection:
            cleanup_instances(cloud, resource_selection['instances'])

    if 'router_interfaces' in resource_selection:
        router_ids = []
        if 'routers' in resource_selection:
            for r_uuid in resource_selection['routers']:
                router_ids.append(r_uuid)

        interface_entries = resource_selection['router_interfaces']

        for r_uuid in router_ids:
            for router in cloud.search_routers(r_uuid):
                for key in interface_entries:
                    inter = interface_entries[key]

                    if dry_run:
                        for sub_id in inter['subnet_ids']:
                            show_cleanup(
                                ('neutron router-interface-delete ' +
                                 ' {0} {1}').format(
                                    r_uuid, sub_id))
                    else:
                        cloud.remove_router_interface(
                            router, port_id=inter['id'])

    if dry_run:
        if 'stacks' in resource_selection:
            dry_cleanup_stacks(resource_selection['stacks'])
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
        if 'keypairs' in resource_selection:
            dry_cleanup_keypairs(resource_selection['keypairs'])
    else:
        if 'stacks' in resource_selection:
            cleanup_stacks(cloud, resource_selection['stacks'])
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
        if 'keypairs' in resource_selection:
            cleanup_keypairs(cloud, resource_selection['keypairs'])
