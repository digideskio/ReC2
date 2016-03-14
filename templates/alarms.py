#!/usr/bin/env python

from troposphere import Template, Parameter, Ref, Output
from troposphere.cloudwatch import Alarm, MetricDimension

t = Template()

asg_name = t.add_parameter(Parameter(
    'AsgName',
    Type='String',
    Description='Autoscaling Group to monitor'
))

down_threshold = t.add_parameter(
    Parameter(
        'DownThreshold',
        Type='String'
    )
)

down_evaluations = t.add_parameter(
    Parameter(
        'DownEvaluations',
        Type='String'
    )
)

credit_threshold = t.add_parameter(
    Parameter(
        'CreditThreshold',
        Type='String'
    )
)

credit_evaluations = t.add_parameter(
    Parameter(
        'CreditEvaluations',
        Type='String'
    )
)

low_cpu_alarm = t.add_resource(
    Alarm(
        "ReC2AlarmLow",
        AlarmDescription="CPU Low Alarm",
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Statistic="Average",
        Period=60,
        Dimensions=[
            MetricDimension(
                Name="AutoScalingGroupName",
                Value=Ref(asg_name)
            )
        ],
        EvaluationPeriods=Ref(down_evaluations),
        Threshold=Ref(down_threshold),
        ComparisonOperator="LessThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

low_credit_alarm = t.add_resource(
    Alarm(
        "ReC2NoCredits",
        AlarmDescription="CPU Credits Exhausted Alarm",
        Namespace="AWS/EC2",
        MetricName="CPUCreditBalance",
        Statistic="Average",
        Period=300,
        Dimensions=[
            MetricDimension(
                Name="AutoScalingGroupName",
                Value=Ref(asg_name)
            )
        ],
        EvaluationPeriods=Ref(credit_evaluations),
        Threshold=Ref(credit_threshold),
        ComparisonOperator="LessThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

t.add_output([
    Output(
        'UpAlarm',
        Description='Alarm name for up/high',
        Value=Ref(high_cpu_alarm)
    ),
    Output(
        'DownAlarm',
        Description='Alarm name for down/low',
        Value=Ref(low_cpu_alarm)
    ),
    Output(
        'CreditLowAlarm',
        Description='Alarm name for credits out',
        Value=Ref(low_credit_alarm)
    )
])

if __name__ == '__main__':
    print t.to_json()
