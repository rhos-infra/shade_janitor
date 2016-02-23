#!/usr/bin/env python

import shade
from shade_janitor import select_related
import pprint
import datetime
import pytz

# Initialize and turn on debug logging
shade.simple_logging(debug=True)

# Initialize cloud
# Cloud configs are read with os-client-config
cloud = shade.openstack_cloud(cloud='rhos-component-ci')

pp = pprint.PrettyPrinter(indent=4)
now = datetime.datetime.now(pytz.utc)

resources = select_related.SelectRelatedResources(cloud)

resources.select_instances()
resources.select_networks()
resources.select_subnets()
resources.select_routers()
resources.select_floatingips()
resources.select_related_ports()

pp.pprint(resources.get_selection())
