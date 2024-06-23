# -*- coding: utf-8 -*-
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from constructs import Construct

from infra.config import VPC_CIDR


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            scope=self,
            id="vpc.logger",
            ip_addresses=ec2.IpAddresses.cidr(VPC_CIDR),
            max_azs=2,
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

        subnet_filter = ec2.SubnetFilter

        self.subnet_group = rds.SubnetGroup(
            scope=scope,
            id="DatabaseSubnetGroup",
            description="Database subnet group",
            vpc=self.vpc,
            subnet_group_name="database.rds.logger",
            vpc_subnets=ec2.SubnetSelection(
                subnets=self.vpc.isolated_subnets,
            ),
        )
