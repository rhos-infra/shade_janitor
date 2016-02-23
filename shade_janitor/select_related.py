#!/usr/bin/env python


class SelectRelatedResources:
    """ Helper class to allow you to easily select a group of resources

    this uses a shade openstack_cloud instance to query resources from
    it stores id and name in a double dictionary with the first level
    being resource type

    import shade
    cloud = shade.openstack_cloud(cloud='cloud_name')
    resources = SelectRelatedResources(cloud)

    resources.select_all_networks()
    selection = resources.get_selection()
    for key in selection:
        print selection[key]
    """

    def __init__(self, cloud):
        self._cloud = cloud
        if self._cloud is None:
            raise Exception('No cloud provided')

        self._selection = {}

    def _add(self, resource_type, uuid, name=None, data=None):
        if resource_type not in self._selection:
            self._selection[resource_type] = {}
        if uuid not in self._selection[resource_type]:
            entry = {'id': uuid}
            if name is not None:
                entry['name'] = name
            if data is not None:
                for key in data.keys():
                    entry[key] = data[key]
            self._selection[resource_type][uuid] = entry

    def _add_instance(self, instance):
        """
        Helper to add instances to the selection list
        """
        self._add('instances', instance.id, instance.name,
                  data={'created_on': instance.created})

    def select_instances(self):
        """
        Excludes instances with either 'jenkins' or 'slave' in their names
        """
        for instance in self._cloud.list_servers():
            for entry in ['jenkins', 'slave']:
                if entry in instance.name:
                    continue
            self._add_instance(instance)

    def select_instances_name_substring(self, search_substring):
        """
        will select related resources based on provided substring

        Excludes instances with either 'jenkins' or 'slave' in their names
        """
        for instance in self._cloud.list_servers():
            for entry in ['jenkins', 'slave']:
                if entry in instance.name:
                    continue
            if search_substring in instance.name:
                self._add_instance(instance)

    def select_networks(self):
        """
        Exlcude router:external routers
        """
        for network in self._cloud.list_networks():
            if network['router:external']:
                continue
            self._add('nets', network['id'], network['name'])

    def select_networks_name_substring(self, search_substring):
        """
        Exlcude router:external routers
        """
        for network in self._cloud.list_networks():
            if network['router:external']:
                continue
            if search_substring in network['name']:
                self._add('nets', network['id'], network['name'])

    def select_subnets(self):
        for subnet in self._cloud.list_subnets():
            self._add('subnets', subnet['id'], subnet['name'])

    def select_subnets_name_substring(self, search_substring):
        for subnet in self._cloud.list_subnets():
            if search_substring in subnet['name']:
                self._add('subnets', subnet['id'], subnet['name'])

    def select_routers(self):
        for router in self._cloud.list_routers():
            self._add('routers', router['id'], router['name'])

    def select_routers_name_substring(self, search_substring):
        for router in self._cloud.list_routers():
            if search_substring in router['name']:
                self._add('routers', router['id'], router['name'])

    def select_floatingips(self):
        for fip in self._cloud.list_floating_ips():
            self._add('fips', fip.id, data={'attached': fip.attached})

    def select_floatingips_unattached(self):
        for fip in self._cloud.list_floating_ips():
            if fip.attached:
                continue
            self._add('fips', fip.id, data={'attached': fip.attached})

    def get_selection(self):
        return self._selection
