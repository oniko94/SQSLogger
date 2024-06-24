# -*- coding: utf-8 -*-
from aws_cdk import RemovalPolicy, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from constructs import Construct

from infra.config import DATABASE_NAME, DATABASE_PORT, DATABASE_USER


class DatabaseStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnet_group = rds.SubnetGroup(
            scope=self,
            id="DatabaseSubnetGroup",
            description="Database subnet group",
            vpc=scope.vpc,
            subnet_group_name="rds.logger.subnet_group",
            vpc_subnets=ec2.SubnetSelection(
                subnets=scope.vpc.isolated_subnets,
            ),
        )

        self.db = rds.DatabaseInstance(
            scope=self,
            id=DATABASE_NAME,
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            vpc=scope.vpc,
            subnet_group=subnet_group,
            credentials=rds.Credentials.from_generated_secret(DATABASE_USER),
            instance_type=ec2.InstanceType("t2.micro"),
            port=DATABASE_PORT,
            allocated_storage=80,
            multi_az=True,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            publicly_accessible=False,
        )
