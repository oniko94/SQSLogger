# -*- coding: utf-8 -*-
import os

AWS_ACCOUNTID = os.environ["AWS_ACCOUNTID"]
AWS_REGION = os.environ["AWS_REGION"]
VPC_CIDR = os.environ["VPC_CIDR"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_PORT = int(os.environ["DATABASE_PORT"])
DATABASE_USER = os.environ["DATABASE_USER"]
