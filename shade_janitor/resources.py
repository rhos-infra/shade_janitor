import shade


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

    BLACKLIST = ['jenkins', 'slave', 'mirror']

    def __init__(self, cloud):
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
            for entry in self.BLACKLIST:
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

    def select_related_ports(self):
        """Select related ports."""
        for port in self._cloud.list_ports():

            pick_it = False

            router_interface = False
            if port['device_owner'] == 'network:router_interface':
                router_interface = True

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

            if pick_it and not router_interface:
                self._add('ports', port['id'],
                          data={'subnet_ids': subnet_ids,
                                'network_id': network_id})

            if pick_it and router_interface:
                self._add('router_interfaces', port['id'],
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
            self.select_related_ports()
            self.select_floatingips_unattached()
        except shade.exc.OpenStackCloudException:
            # We don't care as this is the case for QEOS4 lab
            pass

    def get_selection(self):
        """Returns selected resources."""
        return self._selection
