from aws_cdk import RemovalPolicy, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam
from aws_cdk import aws_rds as rds
from aws_cdk import aws_sqs as sqs
from constructs import Construct

from .config import DATABASE_NAME, DATABASE_PORT, DATABASE_USER
from .network_stack import NetworkStack


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(self, "logs.queue")

        vpc = NetworkStack(self, "Network", **kwargs).vpc

        subnet_group = rds.SubnetGroup(
            scope=self,
            id="DatabaseSubnetGroup",
            description="Database subnet group",
            vpc=vpc,
            subnet_group_name="rds.logger.subnet_group",
            vpc_subnets=ec2.SubnetSelection(
                subnets=vpc.isolated_subnets,
            ),
        )
        db = rds.DatabaseInstance(
            scope=self,
            id=DATABASE_NAME,
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            vpc=vpc,
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

        access_role = iam.Role(
            scope=self,
            id="ECSTaskAccessRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )
        access_role.add_to_policy(
            iam.PolicyStatement(
                sid="CloudWatchLogsWriteAccess",
                actions=["logs:Create*", "logs:PutLogEvents"],
                effect=iam.Effect.ALLOW,
                resources=[f"arn:aws:logs:{self.region}:{self.account}:*"],
            )
        )
        access_role.add_to_policy(
            iam.PolicyStatement(
                sid="SQSReadAccess",
                actions=[
                    "sqs:GetQueueUrl",
                    "sqs:ListQueues",
                    "sqs:ReceiveMessage",
                ],
                effect=iam.Effect.ALLOW,
                resources=[
                    f"arn:aws:sqs:{self.region}:${self.account}:${queue.queue_name}"
                ],
            ),
        )
        access_role.add_to_policy(
            iam.PolicyStatement(
                sid="ECRReadAccess",
                actions=[
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:BatchGetImage",
                    "ecr:GetDownloadUrlForLayer",
                ],
                effect=iam.Effect.ALLOW,
                resources=["*"],
                conditions={"StringEquals": {"aws:SourceVpc": vpc.vpc_id}},
            ),
        )
        cluster = ecs.Cluster(self, "Logger", vpc=vpc)
