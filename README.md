# shade_janitor

![TravisCI](https://img.shields.io/travis/yazug/shade_janitor.svg)
https://travis-ci.org/yazug/shade_janitor

Utility based on shade, for cleaning up resources from CI runs in tenant on
OpenStack cloud.

With shade_janitor you can:

* List resources intended for cleanup
* Cleanup running or powered-off resources
* Cleanup only old resources
    - Resources which active for more than 8 hours
    - Powered off resources for more than 1 hour
    - Permanent labled resources for more than 14 days
* Cleanup resources (new or old) with specific substring

There are couple of restrictions:

* If no instances are running for network resources, they are subject to cleanup
* If an instance is hanginging around for more than 8 hours, it is subject to cleanup
* Don't try to cleanup resources this tenant doesn't control
* Don't touch jenkins or slave instances

### Configuration
In order to connect the cloud shade_janotir requires setting a cloud configuration.
Since it uses os-client-config [3], several ways exist:

* environment variables or
* /etc/openstack configuration file or
* ~/.config/openstack configuration file or
* clouds.yaml file located in the shade_janitor directory

## Environment variables setup examplee
```
export OS_AUTH_URL=http://xyz.xyz.xyz.xyz:5000/v2.0
export OS_TENANT_NAME="demo"
export OS_REGION_NAME=""
export OS_USERNAME="demo"
export OS_PASSWORD=XYZ
export OS_CLOUD_NAME=my_cloud
```
 
## clouds.yaml content example
```
clouds:
  my_cloud:
    profile: my_cloud
    auth:
      auth_url: http://xyz.xyz.xyz.xyz:5000/v2.0/
      username: demo
      password: XYZ
      project_name: demo
```
### Invocation 
The invocation of shade_janotor is better to be performed from a virtual environment
```
virtualenv shade-env
. shade-env/bin/activate
pip install -r requirements.txt
python shade_janitor/janitor.py --cloud rhos-component-ci --old --cleanup
```

### Usage

To list the resources that shade_janitor would cleanup

    ./janitor.py --cloud my_cloud

To cleanup the resources

    ./janitor.py --cloud my_cloud --cleanup

To list the resources that include the substring 'smb'

    ./janitor.py --cloud qeos7 --substring smb

To list old (oldest instance and associated resources)

    ./janitor.py --cloud qeos7 --old

To cleanup old (oldest instance and associated resources)

    ./janitor.py --cloud qeos7 --old --cleanup

Experimental Feature(s):

unused resources

    janitor.py --unused

this will look through the current resources and attempt
to identify any network resources not associated with IPs
or VMs.  These sets of resources can then be processed for
cleanup.
