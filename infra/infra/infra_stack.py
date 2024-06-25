from aws_cdk import RemovalPolicy, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
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
        postgres = rds.DatabaseInstance(
            scope=self,
            id=DATABASE_NAME,
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            vpc=vpc,
            subnet_group=subnet_group,
            credentials=rds.Credentials.from_generated_secret(DATABASE_USER),
            instance_type=ec2.InstanceType("t3.medium"),
            port=DATABASE_PORT,
            allocated_storage=80,
            multi_az=True,
            database_name=DATABASE_NAME,
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
                    "sqs:SendMessage",
                ],
                effect=iam.Effect.ALLOW,
                resources=[
                    f"arn:aws:sqs:{self.region}:{self.account}:{queue.queue_name}"
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
        access_role.add_to_policy(
            iam.PolicyStatement(
                sid="SecretReadAccess",
                actions=[
                    "secretsmanager:GetSecretValue",
                    "secretsmanager:DescribeSecrets",
                ],
                effect=iam.Effect.ALLOW,
                resources=["*"],
            ),
        )

        container_env = {
            "secrets": {
                "POSTGRES_USER": ecs.Secret.from_secrets_manager(
                    postgres.secret
                ),
                "POSTGRES_PASSWORD": ecs.Secret.from_secrets_manager(
                    postgres.secret
                ),
            },
            "environment": {
                "POSTGRES_DB": DATABASE_NAME,
                "POSTGRES_HOST": postgres.db_instance_endpoint_address,
                "POSTGRES_PORT": postgres.db_instance_endpoint_port,
                "AWS_REGION": self.region,
                "SQS_QUEUE_NAME": queue.queue_name,
            },
        }
        print(container_env)
        image_repository = ecr.Repository.from_repository_name(
            self, id="docker.logger.repo", repository_name="sqslogger"
        )
        cluster = ecs.Cluster(
            self, id="Logger", vpc=vpc, enable_fargate_capacity_providers=True
        )
        api_taskdef = ecs.FargateTaskDefinition(
            self,
            id="api-task.logger",
            execution_role=access_role,
        )
        api_taskdef.add_container(
            "api-latest",
            image=ecs.ContainerImage.from_ecr_repository(
                repository=image_repository, tag="api.latest"
            ),
            port_mappings=[ecs.PortMapping(container_port=8080)],
            secrets=container_env["secrets"],
            environment=container_env["environment"],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="api-service-"),
        )
        api_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            id="logger.api",
            cluster=cluster,
            task_definition=api_taskdef,
            task_subnets=ec2.SubnetSelection(
                subnets=vpc.private_subnets,
            ),
            public_load_balancer=True,
        )
        worker_taskdef = ecs.FargateTaskDefinition(
            self,
            " worker-task.logger",
            execution_role=access_role,
        )
        worker_taskdef.add_container(
            "worker-latest",
            image=ecs.ContainerImage.from_ecr_repository(
                repository=image_repository, tag="worker.latest"
            ),
            environment=container_env["environment"],
            secrets=container_env["secrets"],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="worker-service-"),
        )
        worker_service = ecs.FargateService(
            self,
            "logger.worker",
            cluster=cluster,
            task_definition=worker_taskdef,
        )
