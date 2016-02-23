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
# CI naming uses a job prefix like this for all resources
prefix = '0y9d4-rhos-ci-122'
resources.select_instances_name_substring(prefix)
resources.select_networks_name_substring(prefix)
resources.select_subnets_name_substring(prefix)
resources.select_routers_name_substring(prefix)
resources.select_related_ports()

# General Cleanup
resources.select_floatingips_unattached()

pp.pprint(resources.get_selection())
