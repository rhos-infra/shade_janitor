# shade_janitor
Utility based on shade to select and cleanup resources from CI runs in a tenant

Intended to automate selecting resouces for janitor cleanup in a cattle only
automation tenant

That means there are only a couple of restrictions on cleanup:

if no instances are running for network resources they are subject to cleanup
if an instance is hanginging around for more than 8 hours it is subject to cleanup

don't try to cleanup resources this tenant doesn't control
don't touch jenkins or slave instances
