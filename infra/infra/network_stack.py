# -*- coding: utf-8 -*-
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from infra.config import VPC_CIDR


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            scope=self,
            id="vpc.logger",
            ip_addresses=ec2.IpAddresses.cidr(VPC_CIDR),
            max_azs=1,
            nat_gateways=1,
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
            gateway_endpoints={
                "S3": ec2.GatewayVpcEndpointOptions(
                    service=ec2.GatewayVpcEndpointAwsService.S3,
                )
            },
        )

        self.vpc.add_interface_endpoint(
            id="ecr-docker.logger.vpcinterface",
            service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
            subnets=ec2.SubnetSelection(
                subnets=self.vpc.private_subnets,
            ),
        )
        self.vpc.add_interface_endpoint(
            id="ecr.logger.vpcinterface",
            service=ec2.InterfaceVpcEndpointAwsService.ECR,
            subnets=ec2.SubnetSelection(
                subnets=self.vpc.private_subnets,
            ),
        )
        self.vpc.add_interface_endpoint(
            id="secrets.logger.vpcinterface",
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            subnets=ec2.SubnetSelection(
                subnets=self.vpc.private_subnets,
            ),
        )
