#!/usr/bin/env python3

import aws_cdk as cdk

from infra.config import AWS_ACCOUNTID, AWS_REGION
from infra.infra_stack import InfraStack

app = cdk.App()
InfraStack(
    scope=app,
    construct_id="SQSLogger",
    env={
        "account": AWS_ACCOUNTID,
        "region": AWS_REGION,
    },
)

app.synth(validate_on_synthesis=True)
