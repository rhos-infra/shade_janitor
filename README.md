# shade_janitor

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

### Usage

To list the resources that shade_janitor would cleanup

    ./janitor.py --cloud my_cloud

To cleanup the resources

    ./janitor.py --cloud my_cloud --cleanup

To list the resources that include the substring 'smb'

    ./janitor.py --cloud qeos7 --substring smb

To list old resources

    ./janitor.py --cloud qeos7 --old

To cleanup old resources

    ./janitor.py --cloud qeos7 --old --cleanup
