from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            scope=self,
            id="vpc.logger",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                {
                    "cidrMask": 24,
                    "name": "subnet-1.logger",
                    "subnetType": ec2.SubnetType.PUBLIC,
                },
                {
                    "cidrMask": 24,
                    "name": "subnet-2.logger",
                    "subnetType": ec2.SubnetType.PRIVATE_WITH_EGRESS,
                },
                {
                    "cidrMask": 24,
                    "name": "subnet-3.logger",
                    "subnetType": ec2.SubnetType.PRIVATE_ISOLATED,
                },
            ],
        )
