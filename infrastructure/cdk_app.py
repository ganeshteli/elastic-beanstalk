#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from elastic_beanstalk import ElasticBeanstalkStack

env = Environment(account="003529669851", region="ap-south-1")

app = App()

ElasticBeanstalkStack(app, "eb-flask-app", env=env)

app.synth()