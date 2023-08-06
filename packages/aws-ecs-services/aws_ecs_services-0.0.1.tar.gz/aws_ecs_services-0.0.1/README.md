# aws_ecs_services

## Why
I would like to easily ssh into the instance an ECS service is running on. When deployed into a cluster with several instances you cannot accomplish this using `awscli`.

I work through a VPN, so I am only interested in the instances' private IP addresses. When using the AWS Session Manager I am interested in the instances' ids.

The script provides two ways to get the instance's information:
* **1. approach**: For **ECS services that use service discovery** and register a DNS name with AWS Route53, it's possible to get the services's/container's private IP and then check which EC2 instance contains the same private IP.
* **2. approach**: When using AWS SSM (with `ssm-agent` on EC2 instances and AWS Session Manager Plugin locally) the tool will connect to every ECS cluster instance and compares a given service with running ones (running docker containers).

In case the infrastructure is deployed with terraform, the service names as well as the DNS names of the services become predictable.

## How

The tool is best used with `aws-vault`. So far I did not implement reading AWS profiles with `boto3` e.g.

**1. approach** (services with service discovery only) using `by-service-dns`:

```
aws_ecs_services by-service-dns --region <aws_region> --cluster <ecs_cluster_name> --dns <service_dns_name> [--output <output_info>]
```

The tool gets the DNS name of the service (AWS Route53). It also gets the name of the cluster the service was created in. Also the tool gets the AWS region to use.

The association between the service's DNS name and the instance private IP:
* Get the IP of the service by DNS name (host name).
  - IP is changing constantly (with every deployment), DNS name is not.
* Get all the cluster instances.
  - Make sure you configure the correct cluster (The service nneds to be located in there.).
* Get the private IP addresses of these instances and compareto the IP address of the service.
* The match reveals the correct instance.

**2. approach** (all services, requires a working AWS SSM setup) using `by-service-name`:

```
aws_ecs_services by-service-name --region <aws_region> --cluster <ecs_cluster_name> --name <part_of_service_name_even_regex>
```

The tool gets the name of the service (AWS ECS service) or part of it (regular expressions allowed). It also gets the name of the cluster the service was created in. Also the tool gets the AWS region to work in.

All cluster instances are checked for running docker containers. Using regular expressions the given service name is searched for in the list of docker container names. If a match is found the according instance id will be returned.

Only the first match will be considered.


## Usage
For better readability I will leave out `aws-vault` in the examples below.

There are 4 sub commands:
* `by-service-dns` - Get instance information by service's dns name.
* `by-service-name` - Get instance id by service's name.
* `list-instances` - Get all cluster instances (instance ids).
* `list-services` - Get all active cluster services.

Here you can find some examples to ssh into the appropriate EC2 instance:
```
# Get instance IP address by service DNS name
ssh ec2-user@"$(aws_ecs_services by-service-dns --region eu-west-2 --cluster my-cluster --dns dns.name.com)"
# Get instance ID by service DNS name
aws ssm start-session --target "$(aws_ecs_services by-service-dns --region eu-west-2 --cluster my-cluster --dns dns.name.com --output id)"
# Get instance ID by service name
aws ssm start-session --target "$(aws_ecs_services by-service-name --region eu-west-2 --cluster my-cluster --name part_of_service_name_even_regex)"
```

Here you can find further examples of how to use this tool:
```
# List all instance IDs in cluster
aws_ecs_services list-instances --region eu-west-2 --cluster my-cluster
# List all service names deployed in the cluster
aws_ecs_services list-services --region eu-west-2 --cluster my-cluster
```

Using regular expressions
`aws_ecs_services by-service-name --region eu-west-2 --cluster dev --name "price-redis-[a-z0-9]*$" --debug`

`--debug` shows additional output in order to really get the correct container (service) in case more than one was found e.g..


The default output of the subcommand `by-service-dns` is the instance's private IP address.
* If called with `--output id` it displays the instance's id.
    ```
        # Get instance id by service DNS name
        aws ssm start-session --target "$(aws_ecs_services by-service-dns --region eu-west-2 --cluster my-cluster --dns dns.name.com --output id)"
    ```
* If called with `--output all` it displays both of the values above. In addition it returns the instance's private DNS name.
* If called with `--output service` it displays the service's IP address only.
