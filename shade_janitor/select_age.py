#!/usr/bin/env python

import dateutil.parser
from datetime import datetime
from datetime import timedelta
import pytz

from select_related import SelectRelatedResources


class SelectAgeRelatedResources(SelectRelatedResources):
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

    def select_old_instances(self, powered_on_ttl=timedelta(hours=8),
                             powered_off_ttl=timedelta(hours=1)):
        """
        Check for old instances

        Excludes blacklisted instances
        """
        for instance in self._cloud.list_servers():
            if self.check_instance_blacklisted(instance):
                continue

            created_on = dateutil.parser.parse(instance.created)
            now = datetime.now(pytz.utc)
            age = now - created_on
            if age > powered_on_ttl:
                self._add_instance(instance, age=age)
            elif instance['OS-EXT-STS:power_state'] == 0 and age > powered_off_ttl:
                self._add_instance(instance, age=age)
