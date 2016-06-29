#!/usr/bin/env python

from troposphere import Template, Parameter, Ref, events

t = Template()

event_role = t.add_parameter(Parameter(
    'EventRole',
    Type='String',
    Description='Event Role'
))

lambda_arn = t.add_parameter(Parameter(
    'LambdaArn',
    Type='String',
    Description='Lambda Arn'
))

rule = t.add_resource(
    events.Rule(
        "ReC2",
        RoleArn=Ref(event_role),
        Targets=[events.Target(
            Arn=Ref(lambda_arn),
            Id="ReC2"
        )],
        ScheduleExpression="rate(5 minutes)"
    )
    )

if __name__ == '__main__':
    print t.to_json()
