import logging


class Summary(object):
    """Summary class to summarize cleanedup resources."""

    num_of_instances = 0
    num_of_networks = 0
    num_of_subnets = 0
    num_of_floating_ips = 0
    num_of_routers = 0
    num_of_ports = 0
    num_of_stacks = 0
    num_of_keypairs = 0
    num_of_secgroups = 0

    @classmethod
    def print_summary(cls):
        """Print summary of cleanedup resources."""

        logging.info("====== Summary of cleaned up resouces "
                     "======\n\n\tNumber of instances: {}\n"
                     "\tNumber of networks: {}\n"
                     "\tNumber of subnets: {}\n"
                     "\tNumber of floating IPs: {}\n"
                     "\tNumber of routers: {}\n"
                     "\tNumber of ports: {}\n"
                     "\tNumber of stacks: {}\n"
                     "\tNumber of keypairs: {}\n"
                     "\tNumber of security groups: {}\n"
                     .format(cls.num_of_instances,
                             cls.num_of_networks,
                             cls.num_of_subnets,
                             cls.num_of_floating_ips,
                             cls.num_of_routers,
                             cls.num_of_ports,
                             cls.num_of_stacks,
                             cls.num_of_keypairs,
                             cls.num_of_secgroups))
