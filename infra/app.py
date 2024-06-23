#!/usr/bin/env python3

import aws_cdk as cdk

from infra.infra_stack import InfraStack

app = cdk.App()
InfraStack(app, "SQSLogger")

app.synth(validate_on_synthesis=True)
