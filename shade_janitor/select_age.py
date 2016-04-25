#!/usr/bin/env python

import dateutil.parser
import pytz

from datetime import datetime
from datetime import timedelta
from resources import Resources


class SelectAgeRelatedResources(Resources):
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

    def select_old_instances(self, powered_on_ttl=timedelta(hours=8),
                             powered_off_ttl=timedelta(hours=1),
                             powered_on_permanent_ttl=timedelta(days=14),
                             inerror_ttl=None,
                             now=None):
        """Check for old instances.

        Excludes blacklisted instances.

        :param powered_on_ttl: life cycle for active resources
        :param powered_off_ttl: life cycle for powered off resources
        :param powered_on_permanent_ttl: life cycle of active and permanent
        """
        for instance in self._cloud.list_servers():
            if self.is_blacklisted(instance):
                continue

            created_on = dateutil.parser.parse(instance.created)
            if now is None:
                now = datetime.now(pytz.utc)
            age = now - created_on
            if self.is_permanent(instance):
                if (powered_on_permanent_ttl
                        and age > powered_on_permanent_ttl):
                    self._add_instance(instance, age=age)
            elif instance.status == 'ERROR':
                if (inerror_ttl and age > inerror_ttl):
                    self._add_instance(instance, age=age)
            elif instance['OS-EXT-STS:power_state'] == 0:
                if (powered_off_ttl and age > powered_off_ttl):
                    self._add_instance(instance, age=age)
            elif (powered_on_ttl and age > powered_on_ttl):
                self._add_instance(instance, age=age)
