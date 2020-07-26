import logging
import re
import shade
import time


class NoCloudException(Exception):
    pass


class Resources(object):
    """Helper class to allow you to easily select a group of resources

    this uses a shade openstack_cloud instance to query resources from
    it stores id and name in a double dictionary with the first level
    being resource type

    import shade
    cloud = shade.openstack_cloud(cloud='cloud_name')
    resources = Resources(cloud)

    resources.select_all_networks()
    selection = resources.get_selection()
    for key in selection:
        print selection[key]
    """

    def __init__(self, cloud):
        self.blacklist = ['jenkins', 'slave', 'mirror', 'default']
        self._cloud = cloud
        if self._cloud is None:
            raise NoCloudException('No cloud provided')

        self._selection = {}

    def _add(self, resource_type, uuid, name=None, data=None):
        """Add resource to selection list."""
        if uuid is not None:
            if resource_type not in self._selection:
                self._selection[resource_type] = {}
            if uuid not in self._selection[resource_type]:
                entry = {'id': uuid}
                if name is not None:
                    entry['name'] = name
                if data is not None:
                    for key in list(data.keys()):
                        entry[key] = data[key]
                self._selection[resource_type][uuid] = entry

    def _add_instance(self, instance, age=None):
        """Add instance to the selection list"""
        if instance is not None:
            data = {'created_on': instance.created}
            if age is not None:
                data['age'] = age
            self._add('instances', instance.id, instance.name, data=data)

    def _add_floatingip(self, fip):
        """Add floating ip to the selection list"""
        self._add('fips', fip.id,
                  data={'attached': fip.attached,
                        'network_id': fip.network,
                        'fixed_ip': fip.fixed_ip_address,
                        'floating_ip': fip.floating_ip_address,
                        })

    def reset(self):
        """Reset selection to nothing"""
        self._selection = {}

    def is_blacklisted(self, instance):
        """Check if instance is blacklisted."""
        if instance is not None and instance.name is not None:
            for entry in self.blacklist:
                if entry in instance.name:
                    return True

        return False

    def is_permanent(self, instance):
        """Check if instance is permanent."""
        if instance is None or instance.name is None:
            return False

        return 'permanent' in instance.name

    def select_instances(self):
        """Select all instances.

        Excludes blacklisted instances
        """
        for instance in self._cloud.list_servers():
            if self.is_blacklisted(instance):
                continue
            self._add_instance(instance)

    def select_instances_name_substring(self, search_substring):
        """will select related resources based on provided substring

        Excludes blacklisted instances
        """
        for instance in self._cloud.list_servers():
            if self.is_blacklisted(instance):
                continue
            if search_substring in instance.name:
                self._add_instance(instance)

    def select_keypairs_name_substring(self, search_substring):
        """Select keypairs based on substring."""
        for keypair in self._cloud.list_keypairs():
            if search_substring in keypair['name']:
                if keypair['name'] in ('rhos-jenkins'):
                    continue
                self._add('keypairs', keypair['id'], keypair['name'])

    def select_networks(self):
        """Exlcude router:external routers"""
        for network in self._cloud.list_networks():
            if network['router:external']:
                continue
            self._add('nets', network['id'], network['name'])

    def select_networks_name_substring(self, search_substring):
        """Select networks based on substring."""
        for network in self._cloud.list_networks():
            if network['router:external']:
                continue
            if search_substring in network['name']:
                self._add('nets', network['id'], network['name'])

    def select_stacks(self):
        """Select stacks."""
        for stack in self._cloud.list_stacks():
            self._add('stacks', stack.id, stack.stack_name)

    def select_stacks_name_substring(self, search_substring):
        """Select stacks based on substring."""
        for stack in self._cloud.list_stacks():
            if search_substring in stack.stack_name:
                self._add('stacks', stack.id, stack.stack_name)

    def select_subnets(self):
        """Select routers."""
        for subnet in self._cloud.list_subnets():
            self._add('subnets', subnet['id'], subnet['name'])

    def select_subnets_name_substring(self, search_substring):
        """Select subnets based on substring."""
        for subnet in self._cloud.list_subnets():
            if search_substring in subnet['name']:
                self._add('subnets', subnet['id'], subnet['name'])

    def select_routers(self):
        """Select routers."""
        for router in self._cloud.list_routers():
            self._add('routers', router['id'], router['name'])

    def select_routers_name_substring(self, search_substring):
        """Select routers based on substring."""
        for router in self._cloud.list_routers():
            if search_substring in router['name']:
                self._add('routers', router['id'], router['name'])

    def select_security_groups(self):
        """Select security groups."""
        for secgroup in self._cloud.list_security_groups():
            self._add('secgroups', secgroup['id'], secgroup['name'])

    def select_floatingips(self):
        """Select floating ip."""
        for fip in self._cloud.list_floating_ips():
            self._add_floatingip(fip)

    def select_floatingips_unattached(self):
        """Select unattached floating ip."""
        for fip in self._cloud.list_floating_ips():
            if fip.attached:
                continue
            self._add_floatingip(fip)

    def select_related_router_interfaces(self):
        """Select only related router interface ports"""
        if 'routers' in self._selection:
            for router_id in self._selection['routers']:
                for router in self._cloud.search_routers(router_id):
                    for inter in self._cloud.list_router_interfaces(router):
                        subnet_ids = []
                        pick_it = False
                        network_id = None

                        if 'fixed_ips' in inter:
                            for sub in inter['fixed_ips']:
                                subnet_ids.append(sub['subnet_id'])
                        if 'subnets' in self._selection:
                            for sub in subnet_ids:
                                if sub in self._selection['subnets']:
                                    pick_it = True
                                    break

                        if 'network_id' in inter:
                            network_id = inter['network_id']
                            if 'nets' in self._selection:
                                if network_id in self._selection['nets']:
                                    pick_it = True

                        if pick_it:
                            self._add('router_interfaces', inter['id'],
                                      data={'subnet_ids': subnet_ids,
                                            'network_id': network_id})

    def select_related_ports(self):
        """Select related ports."""
        for port in self._cloud.list_ports():

            pick_it = False

            if port['device_owner'] == 'network:router_interface':
                continue

            subnet_ids = []
            for sub in port['fixed_ips']:
                if 'subnet_id' in sub:
                    subnet_ids.append(sub['subnet_id'])

            if 'subnets' in self._selection:
                for sub in subnet_ids:
                    if sub in self._selection['subnets']:
                        pick_it = True
                        break

            network_id = None
            if 'network_id' in port:
                network_id = port['network_id']
                if 'nets' in self._selection:
                    if network_id in self._selection['nets']:
                        pick_it = True

            if pick_it:
                self._add('ports', port['id'],
                          data={'subnet_ids': subnet_ids,
                                'network_id': network_id})

    def select_resources(self, substring):
        """Select different type of resources.

        :param resources: collection of resources
        :param substring: part of resources name
        """
        self.select_instances_name_substring(substring)
        try:
            self.select_networks_name_substring(substring)
            self.select_subnets_name_substring(substring)
            self.select_routers_name_substring(substring)
            self.select_stacks_name_substring(substring)
            self.select_keypairs_name_substring(substring)
            self.select_related_ports()
            self.select_related_router_interfaces()
            self.select_floatingips_unattached()
            self.select_security_groups()
        except shade.exc.OpenStackCloudException:
            # We don't care as this is the case for QEOS4 lab
            pass

    def get_selection(self):
        """Returns selected resources."""
        return self._selection


class SelectUnusedResources(Resources):

    # which port['device_owner'] values explicitely mean unused for us
    # ... atm when it has just dhcp or routers plugged
    # anything else is considered 'used'
    PORT_OWNER_UNUSED = ('network:dhcp', 'network:router_interface')

    def select_unuset_netresources(self,
                                   search_substring='',
                                   refine_count=3,
                                   refine_delay=60,
                                   exclude_flips=None,
                                   exclude_pattern=None,
                                   ):
        def intersect(original, update):
            for key in original.keys():
                if key not in update:
                    original.pop(key)
            return original

        def filter_name(collection, search_substring, exclude_matcher):
            for item_id, item in collection.iteritems():
                if search_substring and search_substring not in item['name']:
                    continue
                if exclude_matcher and exclude_matcher(item['name']):
                    continue
                yield (item_id, item)

        flips = self.find_unused_flips(exclude_flips)
        networks = {}
        routers = {}
        try:
            networks = self.find_unused_networks()
            routers = self.find_unused_routers(networks.keys())
        except shade.exc.OpenStackCloudException:
            logging.info('Seems Neutron is not available, ignoring networks'
                         'and routers.')

        run_count = 1
        while run_count < refine_count and any((networks, routers, flips)):
            run_count += 1

            logging.info('Waiting %d seconds before recheck search %d/%d ...'
                         % (refine_delay, run_count, refine_count))
            time.sleep(refine_delay)

            # if's are here to skip searching if the set is already empty
            # (or also if we don't have network_client at all)
            if networks:
                networks = intersect(
                    networks,
                    self.find_unused_networks())
            if routers:
                routers = intersect(
                    routers,
                    self.find_unused_routers(networks.keys()))
            if flips:
                flips = intersect(
                    flips,
                    self.find_unused_flips(exclude_flips))

        exclude_rgx = None
        if exclude_pattern:
            exclude_rgx = re.compile(exclude_pattern).match

        for flip in flips.values():
            if flip.floating_ip_address in exclude_flips:
                logging.info('Found %s - ignoring!' % flip.ip)
                continue
            self._add_floatingip(flip)

        for n_id, net in filter_name(networks, search_substring, exclude_rgx):
            self._add('nets', n_id, net)

        for r_id, rtr in filter_name(routers, search_substring, exclude_rgx):
            self._add('routers', r_id, rtr['name'])

        self.select_related_ports()

    def find_unused_flips(self, exclude_ips=None):
        """find floating IPs which are not attached to VM"""
        unused = {}
        for fip in self._cloud.list_floating_ips():
            # fip.status not used as it differs between neutron and nova FlIPs
            if not fip.attached and fip.fixed_ip_address is None:
                unused[fip.id] = fip
        return unused

    def find_unused_networks(self):
        """find networks without vm's"""
        unused = {}
        networks = self._cloud.list_networks()
        ports = self._cloud.list_ports()
        # query all ports at once, filtering in python is way faster then api

        for net in networks:
            if net.get('router:external', False) or net.get('shared', False):
                continue

            # search the ports if there is any
            # for this network which is considered 'in-use' (vm)
            used_ports = [
                port for port in ports
                if (port['network_id'] == net['id']
                    and (port['device_owner'].lower() not in
                         self.PORT_OWNER_UNUSED))
            ]

            if not any(used_ports):
                unused[net['id']] = net
        return unused

    def find_unused_routers(self, unused_nets):
        """find routers without ports or with ports only in unused networks"""
        unused = {}
        routers = self._cloud.list_routers()
        ports = self._cloud.list_ports()
        for router in routers:
            router_ports = [
                port for port in ports
                if (port['device_id'] == router['id']
                    and port['network_id'] not in unused_nets)
            ]

            if not any(router_ports):
                unused[router['id']] = router
        return unused
