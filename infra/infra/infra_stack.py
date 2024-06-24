from aws_cdk import Duration, Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from .layers.database_stack import DatabaseStack
from .layers.network_stack import NetworkStack


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = NetworkStack(self, "Network", **kwargs).vpc
        self.db = DatabaseStack(self, "Database", **kwargs)
