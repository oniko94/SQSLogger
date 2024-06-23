from aws_cdk import Duration, Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from .layers.network_stack import NetworkStack


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        net = NetworkStack(self, "Network")
