from os.path import abspath, dirname

from setuptools import setup

LONG_DESCRIPTION = open(dirname(abspath(__file__)) + "/README.md", "r").read()


setup(
    name="boto3-stubs",
    version="1.14.0.2",
    packages=["boto3-stubs"],
    url="https://github.com/vemel/mypy_boto3_builder",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description="Type annotations for boto3 1.14.0, generated by mypy-boto3-buider 2.2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
    keywords="boto3 type-annotations boto3-stubs mypy mypy-stubs typeshed autocomplete auto-generated",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_data={"boto3-stubs": ["py.typed", "*.pyi", "*/*.pyi"]},
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://mypy-boto3-builder.readthedocs.io/en/latest/",
        "Source": "https://github.com/vemel/mypy_boto3_builder",
        "Tracker": "https://github.com/vemel/mypy_boto3_builder/issues",
    },
    install_requires=["typing_extensions; python_version < '3.8'", "mypy-boto3==1.14.0.2",],
    extras_require={
        "all": [
            "mypy-boto3-accessanalyzer==1.14.0.2",
            "mypy-boto3-acm==1.14.0.2",
            "mypy-boto3-acm-pca==1.14.0.2",
            "mypy-boto3-alexaforbusiness==1.14.0.2",
            "mypy-boto3-amplify==1.14.0.2",
            "mypy-boto3-apigateway==1.14.0.2",
            "mypy-boto3-apigatewaymanagementapi==1.14.0.2",
            "mypy-boto3-apigatewayv2==1.14.0.2",
            "mypy-boto3-appconfig==1.14.0.2",
            "mypy-boto3-application-autoscaling==1.14.0.2",
            "mypy-boto3-application-insights==1.14.0.2",
            "mypy-boto3-appmesh==1.14.0.2",
            "mypy-boto3-appstream==1.14.0.2",
            "mypy-boto3-appsync==1.14.0.2",
            "mypy-boto3-athena==1.14.0.2",
            "mypy-boto3-autoscaling==1.14.0.2",
            "mypy-boto3-autoscaling-plans==1.14.0.2",
            "mypy-boto3-backup==1.14.0.2",
            "mypy-boto3-batch==1.14.0.2",
            "mypy-boto3-budgets==1.14.0.2",
            "mypy-boto3-ce==1.14.0.2",
            "mypy-boto3-chime==1.14.0.2",
            "mypy-boto3-cloud9==1.14.0.2",
            "mypy-boto3-clouddirectory==1.14.0.2",
            "mypy-boto3-cloudformation==1.14.0.2",
            "mypy-boto3-cloudfront==1.14.0.2",
            "mypy-boto3-cloudhsm==1.14.0.2",
            "mypy-boto3-cloudhsmv2==1.14.0.2",
            "mypy-boto3-cloudsearch==1.14.0.2",
            "mypy-boto3-cloudsearchdomain==1.14.0.2",
            "mypy-boto3-cloudtrail==1.14.0.2",
            "mypy-boto3-cloudwatch==1.14.0.2",
            "mypy-boto3-codeartifact==1.14.0.2",
            "mypy-boto3-codebuild==1.14.0.2",
            "mypy-boto3-codecommit==1.14.0.2",
            "mypy-boto3-codedeploy==1.14.0.2",
            "mypy-boto3-codeguru-reviewer==1.14.0.2",
            "mypy-boto3-codeguruprofiler==1.14.0.2",
            "mypy-boto3-codepipeline==1.14.0.2",
            "mypy-boto3-codestar==1.14.0.2",
            "mypy-boto3-codestar-connections==1.14.0.2",
            "mypy-boto3-codestar-notifications==1.14.0.2",
            "mypy-boto3-cognito-identity==1.14.0.2",
            "mypy-boto3-cognito-idp==1.14.0.2",
            "mypy-boto3-cognito-sync==1.14.0.2",
            "mypy-boto3-comprehend==1.14.0.2",
            "mypy-boto3-comprehendmedical==1.14.0.2",
            "mypy-boto3-compute-optimizer==1.14.0.2",
            "mypy-boto3-config==1.14.0.2",
            "mypy-boto3-connect==1.14.0.2",
            "mypy-boto3-connectparticipant==1.14.0.2",
            "mypy-boto3-cur==1.14.0.2",
            "mypy-boto3-dataexchange==1.14.0.2",
            "mypy-boto3-datapipeline==1.14.0.2",
            "mypy-boto3-datasync==1.14.0.2",
            "mypy-boto3-dax==1.14.0.2",
            "mypy-boto3-detective==1.14.0.2",
            "mypy-boto3-devicefarm==1.14.0.2",
            "mypy-boto3-directconnect==1.14.0.2",
            "mypy-boto3-discovery==1.14.0.2",
            "mypy-boto3-dlm==1.14.0.2",
            "mypy-boto3-dms==1.14.0.2",
            "mypy-boto3-docdb==1.14.0.2",
            "mypy-boto3-ds==1.14.0.2",
            "mypy-boto3-dynamodb==1.14.0.2",
            "mypy-boto3-dynamodbstreams==1.14.0.2",
            "mypy-boto3-ebs==1.14.0.2",
            "mypy-boto3-ec2==1.14.0.2",
            "mypy-boto3-ec2-instance-connect==1.14.0.2",
            "mypy-boto3-ecr==1.14.0.2",
            "mypy-boto3-ecs==1.14.0.2",
            "mypy-boto3-efs==1.14.0.2",
            "mypy-boto3-eks==1.14.0.2",
            "mypy-boto3-elastic-inference==1.14.0.2",
            "mypy-boto3-elasticache==1.14.0.2",
            "mypy-boto3-elasticbeanstalk==1.14.0.2",
            "mypy-boto3-elastictranscoder==1.14.0.2",
            "mypy-boto3-elb==1.14.0.2",
            "mypy-boto3-elbv2==1.14.0.2",
            "mypy-boto3-emr==1.14.0.2",
            "mypy-boto3-es==1.14.0.2",
            "mypy-boto3-events==1.14.0.2",
            "mypy-boto3-firehose==1.14.0.2",
            "mypy-boto3-fms==1.14.0.2",
            "mypy-boto3-forecast==1.14.0.2",
            "mypy-boto3-forecastquery==1.14.0.2",
            "mypy-boto3-frauddetector==1.14.0.2",
            "mypy-boto3-fsx==1.14.0.2",
            "mypy-boto3-gamelift==1.14.0.2",
            "mypy-boto3-glacier==1.14.0.2",
            "mypy-boto3-globalaccelerator==1.14.0.2",
            "mypy-boto3-glue==1.14.0.2",
            "mypy-boto3-greengrass==1.14.0.2",
            "mypy-boto3-groundstation==1.14.0.2",
            "mypy-boto3-guardduty==1.14.0.2",
            "mypy-boto3-health==1.14.0.2",
            "mypy-boto3-iam==1.14.0.2",
            "mypy-boto3-imagebuilder==1.14.0.2",
            "mypy-boto3-importexport==1.14.0.2",
            "mypy-boto3-inspector==1.14.0.2",
            "mypy-boto3-iot==1.14.0.2",
            "mypy-boto3-iot-data==1.14.0.2",
            "mypy-boto3-iot-jobs-data==1.14.0.2",
            "mypy-boto3-iot1click-devices==1.14.0.2",
            "mypy-boto3-iot1click-projects==1.14.0.2",
            "mypy-boto3-iotanalytics==1.14.0.2",
            "mypy-boto3-iotevents==1.14.0.2",
            "mypy-boto3-iotevents-data==1.14.0.2",
            "mypy-boto3-iotsecuretunneling==1.14.0.2",
            "mypy-boto3-iotsitewise==1.14.0.2",
            "mypy-boto3-iotthingsgraph==1.14.0.2",
            "mypy-boto3-kafka==1.14.0.2",
            "mypy-boto3-kendra==1.14.0.2",
            "mypy-boto3-kinesis==1.14.0.2",
            "mypy-boto3-kinesis-video-archived-media==1.14.0.2",
            "mypy-boto3-kinesis-video-media==1.14.0.2",
            "mypy-boto3-kinesis-video-signaling==1.14.0.2",
            "mypy-boto3-kinesisanalytics==1.14.0.2",
            "mypy-boto3-kinesisanalyticsv2==1.14.0.2",
            "mypy-boto3-kinesisvideo==1.14.0.2",
            "mypy-boto3-kms==1.14.0.2",
            "mypy-boto3-lakeformation==1.14.0.2",
            "mypy-boto3-lambda==1.14.0.2",
            "mypy-boto3-lex-models==1.14.0.2",
            "mypy-boto3-lex-runtime==1.14.0.2",
            "mypy-boto3-license-manager==1.14.0.2",
            "mypy-boto3-lightsail==1.14.0.2",
            "mypy-boto3-logs==1.14.0.2",
            "mypy-boto3-machinelearning==1.14.0.2",
            "mypy-boto3-macie==1.14.0.2",
            "mypy-boto3-macie2==1.14.0.2",
            "mypy-boto3-managedblockchain==1.14.0.2",
            "mypy-boto3-marketplace-catalog==1.14.0.2",
            "mypy-boto3-marketplace-entitlement==1.14.0.2",
            "mypy-boto3-marketplacecommerceanalytics==1.14.0.2",
            "mypy-boto3-mediaconnect==1.14.0.2",
            "mypy-boto3-mediaconvert==1.14.0.2",
            "mypy-boto3-medialive==1.14.0.2",
            "mypy-boto3-mediapackage==1.14.0.2",
            "mypy-boto3-mediapackage-vod==1.14.0.2",
            "mypy-boto3-mediastore==1.14.0.2",
            "mypy-boto3-mediastore-data==1.14.0.2",
            "mypy-boto3-mediatailor==1.14.0.2",
            "mypy-boto3-meteringmarketplace==1.14.0.2",
            "mypy-boto3-mgh==1.14.0.2",
            "mypy-boto3-migrationhub-config==1.14.0.2",
            "mypy-boto3-mobile==1.14.0.2",
            "mypy-boto3-mq==1.14.0.2",
            "mypy-boto3-mturk==1.14.0.2",
            "mypy-boto3-neptune==1.14.0.2",
            "mypy-boto3-networkmanager==1.14.0.2",
            "mypy-boto3-opsworks==1.14.0.2",
            "mypy-boto3-opsworkscm==1.14.0.2",
            "mypy-boto3-organizations==1.14.0.2",
            "mypy-boto3-outposts==1.14.0.2",
            "mypy-boto3-personalize==1.14.0.2",
            "mypy-boto3-personalize-events==1.14.0.2",
            "mypy-boto3-personalize-runtime==1.14.0.2",
            "mypy-boto3-pi==1.14.0.2",
            "mypy-boto3-pinpoint==1.14.0.2",
            "mypy-boto3-pinpoint-email==1.14.0.2",
            "mypy-boto3-pinpoint-sms-voice==1.14.0.2",
            "mypy-boto3-polly==1.14.0.2",
            "mypy-boto3-pricing==1.14.0.2",
            "mypy-boto3-qldb==1.14.0.2",
            "mypy-boto3-qldb-session==1.14.0.2",
            "mypy-boto3-quicksight==1.14.0.2",
            "mypy-boto3-ram==1.14.0.2",
            "mypy-boto3-rds==1.14.0.2",
            "mypy-boto3-rds-data==1.14.0.2",
            "mypy-boto3-redshift==1.14.0.2",
            "mypy-boto3-rekognition==1.14.0.2",
            "mypy-boto3-resource-groups==1.14.0.2",
            "mypy-boto3-resourcegroupstaggingapi==1.14.0.2",
            "mypy-boto3-robomaker==1.14.0.2",
            "mypy-boto3-route53==1.14.0.2",
            "mypy-boto3-route53domains==1.14.0.2",
            "mypy-boto3-route53resolver==1.14.0.2",
            "mypy-boto3-s3==1.14.0.2",
            "mypy-boto3-s3control==1.14.0.2",
            "mypy-boto3-sagemaker==1.14.0.2",
            "mypy-boto3-sagemaker-a2i-runtime==1.14.0.2",
            "mypy-boto3-sagemaker-runtime==1.14.0.2",
            "mypy-boto3-savingsplans==1.14.0.2",
            "mypy-boto3-schemas==1.14.0.2",
            "mypy-boto3-sdb==1.14.0.2",
            "mypy-boto3-secretsmanager==1.14.0.2",
            "mypy-boto3-securityhub==1.14.0.2",
            "mypy-boto3-serverlessrepo==1.14.0.2",
            "mypy-boto3-service-quotas==1.14.0.2",
            "mypy-boto3-servicecatalog==1.14.0.2",
            "mypy-boto3-servicediscovery==1.14.0.2",
            "mypy-boto3-ses==1.14.0.2",
            "mypy-boto3-sesv2==1.14.0.2",
            "mypy-boto3-shield==1.14.0.2",
            "mypy-boto3-signer==1.14.0.2",
            "mypy-boto3-sms==1.14.0.2",
            "mypy-boto3-sms-voice==1.14.0.2",
            "mypy-boto3-snowball==1.14.0.2",
            "mypy-boto3-sns==1.14.0.2",
            "mypy-boto3-sqs==1.14.0.2",
            "mypy-boto3-ssm==1.14.0.2",
            "mypy-boto3-sso==1.14.0.2",
            "mypy-boto3-sso-oidc==1.14.0.2",
            "mypy-boto3-stepfunctions==1.14.0.2",
            "mypy-boto3-storagegateway==1.14.0.2",
            "mypy-boto3-sts==1.14.0.2",
            "mypy-boto3-support==1.14.0.2",
            "mypy-boto3-swf==1.14.0.2",
            "mypy-boto3-synthetics==1.14.0.2",
            "mypy-boto3-textract==1.14.0.2",
            "mypy-boto3-transcribe==1.14.0.2",
            "mypy-boto3-transfer==1.14.0.2",
            "mypy-boto3-translate==1.14.0.2",
            "mypy-boto3-waf==1.14.0.2",
            "mypy-boto3-waf-regional==1.14.0.2",
            "mypy-boto3-wafv2==1.14.0.2",
            "mypy-boto3-workdocs==1.14.0.2",
            "mypy-boto3-worklink==1.14.0.2",
            "mypy-boto3-workmail==1.14.0.2",
            "mypy-boto3-workmailmessageflow==1.14.0.2",
            "mypy-boto3-workspaces==1.14.0.2",
            "mypy-boto3-xray==1.14.0.2",
        ],
        "essential": [
            "mypy-boto3-cloudformation==1.14.0.2",
            "mypy-boto3-dynamodb==1.14.0.2",
            "mypy-boto3-ec2==1.14.0.2",
            "mypy-boto3-lambda==1.14.0.2",
            "mypy-boto3-rds==1.14.0.2",
            "mypy-boto3-s3==1.14.0.2",
            "mypy-boto3-sqs==1.14.0.2",
        ],
        "accessanalyzer": ["mypy-boto3-accessanalyzer==1.14.0.2"],
        "acm": ["mypy-boto3-acm==1.14.0.2"],
        "acm-pca": ["mypy-boto3-acm-pca==1.14.0.2"],
        "alexaforbusiness": ["mypy-boto3-alexaforbusiness==1.14.0.2"],
        "amplify": ["mypy-boto3-amplify==1.14.0.2"],
        "apigateway": ["mypy-boto3-apigateway==1.14.0.2"],
        "apigatewaymanagementapi": ["mypy-boto3-apigatewaymanagementapi==1.14.0.2"],
        "apigatewayv2": ["mypy-boto3-apigatewayv2==1.14.0.2"],
        "appconfig": ["mypy-boto3-appconfig==1.14.0.2"],
        "application-autoscaling": ["mypy-boto3-application-autoscaling==1.14.0.2"],
        "application-insights": ["mypy-boto3-application-insights==1.14.0.2"],
        "appmesh": ["mypy-boto3-appmesh==1.14.0.2"],
        "appstream": ["mypy-boto3-appstream==1.14.0.2"],
        "appsync": ["mypy-boto3-appsync==1.14.0.2"],
        "athena": ["mypy-boto3-athena==1.14.0.2"],
        "autoscaling": ["mypy-boto3-autoscaling==1.14.0.2"],
        "autoscaling-plans": ["mypy-boto3-autoscaling-plans==1.14.0.2"],
        "backup": ["mypy-boto3-backup==1.14.0.2"],
        "batch": ["mypy-boto3-batch==1.14.0.2"],
        "budgets": ["mypy-boto3-budgets==1.14.0.2"],
        "ce": ["mypy-boto3-ce==1.14.0.2"],
        "chime": ["mypy-boto3-chime==1.14.0.2"],
        "cloud9": ["mypy-boto3-cloud9==1.14.0.2"],
        "clouddirectory": ["mypy-boto3-clouddirectory==1.14.0.2"],
        "cloudformation": ["mypy-boto3-cloudformation==1.14.0.2"],
        "cloudfront": ["mypy-boto3-cloudfront==1.14.0.2"],
        "cloudhsm": ["mypy-boto3-cloudhsm==1.14.0.2"],
        "cloudhsmv2": ["mypy-boto3-cloudhsmv2==1.14.0.2"],
        "cloudsearch": ["mypy-boto3-cloudsearch==1.14.0.2"],
        "cloudsearchdomain": ["mypy-boto3-cloudsearchdomain==1.14.0.2"],
        "cloudtrail": ["mypy-boto3-cloudtrail==1.14.0.2"],
        "cloudwatch": ["mypy-boto3-cloudwatch==1.14.0.2"],
        "codeartifact": ["mypy-boto3-codeartifact==1.14.0.2"],
        "codebuild": ["mypy-boto3-codebuild==1.14.0.2"],
        "codecommit": ["mypy-boto3-codecommit==1.14.0.2"],
        "codedeploy": ["mypy-boto3-codedeploy==1.14.0.2"],
        "codeguru-reviewer": ["mypy-boto3-codeguru-reviewer==1.14.0.2"],
        "codeguruprofiler": ["mypy-boto3-codeguruprofiler==1.14.0.2"],
        "codepipeline": ["mypy-boto3-codepipeline==1.14.0.2"],
        "codestar": ["mypy-boto3-codestar==1.14.0.2"],
        "codestar-connections": ["mypy-boto3-codestar-connections==1.14.0.2"],
        "codestar-notifications": ["mypy-boto3-codestar-notifications==1.14.0.2"],
        "cognito-identity": ["mypy-boto3-cognito-identity==1.14.0.2"],
        "cognito-idp": ["mypy-boto3-cognito-idp==1.14.0.2"],
        "cognito-sync": ["mypy-boto3-cognito-sync==1.14.0.2"],
        "comprehend": ["mypy-boto3-comprehend==1.14.0.2"],
        "comprehendmedical": ["mypy-boto3-comprehendmedical==1.14.0.2"],
        "compute-optimizer": ["mypy-boto3-compute-optimizer==1.14.0.2"],
        "config": ["mypy-boto3-config==1.14.0.2"],
        "connect": ["mypy-boto3-connect==1.14.0.2"],
        "connectparticipant": ["mypy-boto3-connectparticipant==1.14.0.2"],
        "cur": ["mypy-boto3-cur==1.14.0.2"],
        "dataexchange": ["mypy-boto3-dataexchange==1.14.0.2"],
        "datapipeline": ["mypy-boto3-datapipeline==1.14.0.2"],
        "datasync": ["mypy-boto3-datasync==1.14.0.2"],
        "dax": ["mypy-boto3-dax==1.14.0.2"],
        "detective": ["mypy-boto3-detective==1.14.0.2"],
        "devicefarm": ["mypy-boto3-devicefarm==1.14.0.2"],
        "directconnect": ["mypy-boto3-directconnect==1.14.0.2"],
        "discovery": ["mypy-boto3-discovery==1.14.0.2"],
        "dlm": ["mypy-boto3-dlm==1.14.0.2"],
        "dms": ["mypy-boto3-dms==1.14.0.2"],
        "docdb": ["mypy-boto3-docdb==1.14.0.2"],
        "ds": ["mypy-boto3-ds==1.14.0.2"],
        "dynamodb": ["mypy-boto3-dynamodb==1.14.0.2"],
        "dynamodbstreams": ["mypy-boto3-dynamodbstreams==1.14.0.2"],
        "ebs": ["mypy-boto3-ebs==1.14.0.2"],
        "ec2": ["mypy-boto3-ec2==1.14.0.2"],
        "ec2-instance-connect": ["mypy-boto3-ec2-instance-connect==1.14.0.2"],
        "ecr": ["mypy-boto3-ecr==1.14.0.2"],
        "ecs": ["mypy-boto3-ecs==1.14.0.2"],
        "efs": ["mypy-boto3-efs==1.14.0.2"],
        "eks": ["mypy-boto3-eks==1.14.0.2"],
        "elastic-inference": ["mypy-boto3-elastic-inference==1.14.0.2"],
        "elasticache": ["mypy-boto3-elasticache==1.14.0.2"],
        "elasticbeanstalk": ["mypy-boto3-elasticbeanstalk==1.14.0.2"],
        "elastictranscoder": ["mypy-boto3-elastictranscoder==1.14.0.2"],
        "elb": ["mypy-boto3-elb==1.14.0.2"],
        "elbv2": ["mypy-boto3-elbv2==1.14.0.2"],
        "emr": ["mypy-boto3-emr==1.14.0.2"],
        "es": ["mypy-boto3-es==1.14.0.2"],
        "events": ["mypy-boto3-events==1.14.0.2"],
        "firehose": ["mypy-boto3-firehose==1.14.0.2"],
        "fms": ["mypy-boto3-fms==1.14.0.2"],
        "forecast": ["mypy-boto3-forecast==1.14.0.2"],
        "forecastquery": ["mypy-boto3-forecastquery==1.14.0.2"],
        "frauddetector": ["mypy-boto3-frauddetector==1.14.0.2"],
        "fsx": ["mypy-boto3-fsx==1.14.0.2"],
        "gamelift": ["mypy-boto3-gamelift==1.14.0.2"],
        "glacier": ["mypy-boto3-glacier==1.14.0.2"],
        "globalaccelerator": ["mypy-boto3-globalaccelerator==1.14.0.2"],
        "glue": ["mypy-boto3-glue==1.14.0.2"],
        "greengrass": ["mypy-boto3-greengrass==1.14.0.2"],
        "groundstation": ["mypy-boto3-groundstation==1.14.0.2"],
        "guardduty": ["mypy-boto3-guardduty==1.14.0.2"],
        "health": ["mypy-boto3-health==1.14.0.2"],
        "iam": ["mypy-boto3-iam==1.14.0.2"],
        "imagebuilder": ["mypy-boto3-imagebuilder==1.14.0.2"],
        "importexport": ["mypy-boto3-importexport==1.14.0.2"],
        "inspector": ["mypy-boto3-inspector==1.14.0.2"],
        "iot": ["mypy-boto3-iot==1.14.0.2"],
        "iot-data": ["mypy-boto3-iot-data==1.14.0.2"],
        "iot-jobs-data": ["mypy-boto3-iot-jobs-data==1.14.0.2"],
        "iot1click-devices": ["mypy-boto3-iot1click-devices==1.14.0.2"],
        "iot1click-projects": ["mypy-boto3-iot1click-projects==1.14.0.2"],
        "iotanalytics": ["mypy-boto3-iotanalytics==1.14.0.2"],
        "iotevents": ["mypy-boto3-iotevents==1.14.0.2"],
        "iotevents-data": ["mypy-boto3-iotevents-data==1.14.0.2"],
        "iotsecuretunneling": ["mypy-boto3-iotsecuretunneling==1.14.0.2"],
        "iotsitewise": ["mypy-boto3-iotsitewise==1.14.0.2"],
        "iotthingsgraph": ["mypy-boto3-iotthingsgraph==1.14.0.2"],
        "kafka": ["mypy-boto3-kafka==1.14.0.2"],
        "kendra": ["mypy-boto3-kendra==1.14.0.2"],
        "kinesis": ["mypy-boto3-kinesis==1.14.0.2"],
        "kinesis-video-archived-media": ["mypy-boto3-kinesis-video-archived-media==1.14.0.2"],
        "kinesis-video-media": ["mypy-boto3-kinesis-video-media==1.14.0.2"],
        "kinesis-video-signaling": ["mypy-boto3-kinesis-video-signaling==1.14.0.2"],
        "kinesisanalytics": ["mypy-boto3-kinesisanalytics==1.14.0.2"],
        "kinesisanalyticsv2": ["mypy-boto3-kinesisanalyticsv2==1.14.0.2"],
        "kinesisvideo": ["mypy-boto3-kinesisvideo==1.14.0.2"],
        "kms": ["mypy-boto3-kms==1.14.0.2"],
        "lakeformation": ["mypy-boto3-lakeformation==1.14.0.2"],
        "lambda": ["mypy-boto3-lambda==1.14.0.2"],
        "lex-models": ["mypy-boto3-lex-models==1.14.0.2"],
        "lex-runtime": ["mypy-boto3-lex-runtime==1.14.0.2"],
        "license-manager": ["mypy-boto3-license-manager==1.14.0.2"],
        "lightsail": ["mypy-boto3-lightsail==1.14.0.2"],
        "logs": ["mypy-boto3-logs==1.14.0.2"],
        "machinelearning": ["mypy-boto3-machinelearning==1.14.0.2"],
        "macie": ["mypy-boto3-macie==1.14.0.2"],
        "macie2": ["mypy-boto3-macie2==1.14.0.2"],
        "managedblockchain": ["mypy-boto3-managedblockchain==1.14.0.2"],
        "marketplace-catalog": ["mypy-boto3-marketplace-catalog==1.14.0.2"],
        "marketplace-entitlement": ["mypy-boto3-marketplace-entitlement==1.14.0.2"],
        "marketplacecommerceanalytics": ["mypy-boto3-marketplacecommerceanalytics==1.14.0.2"],
        "mediaconnect": ["mypy-boto3-mediaconnect==1.14.0.2"],
        "mediaconvert": ["mypy-boto3-mediaconvert==1.14.0.2"],
        "medialive": ["mypy-boto3-medialive==1.14.0.2"],
        "mediapackage": ["mypy-boto3-mediapackage==1.14.0.2"],
        "mediapackage-vod": ["mypy-boto3-mediapackage-vod==1.14.0.2"],
        "mediastore": ["mypy-boto3-mediastore==1.14.0.2"],
        "mediastore-data": ["mypy-boto3-mediastore-data==1.14.0.2"],
        "mediatailor": ["mypy-boto3-mediatailor==1.14.0.2"],
        "meteringmarketplace": ["mypy-boto3-meteringmarketplace==1.14.0.2"],
        "mgh": ["mypy-boto3-mgh==1.14.0.2"],
        "migrationhub-config": ["mypy-boto3-migrationhub-config==1.14.0.2"],
        "mobile": ["mypy-boto3-mobile==1.14.0.2"],
        "mq": ["mypy-boto3-mq==1.14.0.2"],
        "mturk": ["mypy-boto3-mturk==1.14.0.2"],
        "neptune": ["mypy-boto3-neptune==1.14.0.2"],
        "networkmanager": ["mypy-boto3-networkmanager==1.14.0.2"],
        "opsworks": ["mypy-boto3-opsworks==1.14.0.2"],
        "opsworkscm": ["mypy-boto3-opsworkscm==1.14.0.2"],
        "organizations": ["mypy-boto3-organizations==1.14.0.2"],
        "outposts": ["mypy-boto3-outposts==1.14.0.2"],
        "personalize": ["mypy-boto3-personalize==1.14.0.2"],
        "personalize-events": ["mypy-boto3-personalize-events==1.14.0.2"],
        "personalize-runtime": ["mypy-boto3-personalize-runtime==1.14.0.2"],
        "pi": ["mypy-boto3-pi==1.14.0.2"],
        "pinpoint": ["mypy-boto3-pinpoint==1.14.0.2"],
        "pinpoint-email": ["mypy-boto3-pinpoint-email==1.14.0.2"],
        "pinpoint-sms-voice": ["mypy-boto3-pinpoint-sms-voice==1.14.0.2"],
        "polly": ["mypy-boto3-polly==1.14.0.2"],
        "pricing": ["mypy-boto3-pricing==1.14.0.2"],
        "qldb": ["mypy-boto3-qldb==1.14.0.2"],
        "qldb-session": ["mypy-boto3-qldb-session==1.14.0.2"],
        "quicksight": ["mypy-boto3-quicksight==1.14.0.2"],
        "ram": ["mypy-boto3-ram==1.14.0.2"],
        "rds": ["mypy-boto3-rds==1.14.0.2"],
        "rds-data": ["mypy-boto3-rds-data==1.14.0.2"],
        "redshift": ["mypy-boto3-redshift==1.14.0.2"],
        "rekognition": ["mypy-boto3-rekognition==1.14.0.2"],
        "resource-groups": ["mypy-boto3-resource-groups==1.14.0.2"],
        "resourcegroupstaggingapi": ["mypy-boto3-resourcegroupstaggingapi==1.14.0.2"],
        "robomaker": ["mypy-boto3-robomaker==1.14.0.2"],
        "route53": ["mypy-boto3-route53==1.14.0.2"],
        "route53domains": ["mypy-boto3-route53domains==1.14.0.2"],
        "route53resolver": ["mypy-boto3-route53resolver==1.14.0.2"],
        "s3": ["mypy-boto3-s3==1.14.0.2"],
        "s3control": ["mypy-boto3-s3control==1.14.0.2"],
        "sagemaker": ["mypy-boto3-sagemaker==1.14.0.2"],
        "sagemaker-a2i-runtime": ["mypy-boto3-sagemaker-a2i-runtime==1.14.0.2"],
        "sagemaker-runtime": ["mypy-boto3-sagemaker-runtime==1.14.0.2"],
        "savingsplans": ["mypy-boto3-savingsplans==1.14.0.2"],
        "schemas": ["mypy-boto3-schemas==1.14.0.2"],
        "sdb": ["mypy-boto3-sdb==1.14.0.2"],
        "secretsmanager": ["mypy-boto3-secretsmanager==1.14.0.2"],
        "securityhub": ["mypy-boto3-securityhub==1.14.0.2"],
        "serverlessrepo": ["mypy-boto3-serverlessrepo==1.14.0.2"],
        "service-quotas": ["mypy-boto3-service-quotas==1.14.0.2"],
        "servicecatalog": ["mypy-boto3-servicecatalog==1.14.0.2"],
        "servicediscovery": ["mypy-boto3-servicediscovery==1.14.0.2"],
        "ses": ["mypy-boto3-ses==1.14.0.2"],
        "sesv2": ["mypy-boto3-sesv2==1.14.0.2"],
        "shield": ["mypy-boto3-shield==1.14.0.2"],
        "signer": ["mypy-boto3-signer==1.14.0.2"],
        "sms": ["mypy-boto3-sms==1.14.0.2"],
        "sms-voice": ["mypy-boto3-sms-voice==1.14.0.2"],
        "snowball": ["mypy-boto3-snowball==1.14.0.2"],
        "sns": ["mypy-boto3-sns==1.14.0.2"],
        "sqs": ["mypy-boto3-sqs==1.14.0.2"],
        "ssm": ["mypy-boto3-ssm==1.14.0.2"],
        "sso": ["mypy-boto3-sso==1.14.0.2"],
        "sso-oidc": ["mypy-boto3-sso-oidc==1.14.0.2"],
        "stepfunctions": ["mypy-boto3-stepfunctions==1.14.0.2"],
        "storagegateway": ["mypy-boto3-storagegateway==1.14.0.2"],
        "sts": ["mypy-boto3-sts==1.14.0.2"],
        "support": ["mypy-boto3-support==1.14.0.2"],
        "swf": ["mypy-boto3-swf==1.14.0.2"],
        "synthetics": ["mypy-boto3-synthetics==1.14.0.2"],
        "textract": ["mypy-boto3-textract==1.14.0.2"],
        "transcribe": ["mypy-boto3-transcribe==1.14.0.2"],
        "transfer": ["mypy-boto3-transfer==1.14.0.2"],
        "translate": ["mypy-boto3-translate==1.14.0.2"],
        "waf": ["mypy-boto3-waf==1.14.0.2"],
        "waf-regional": ["mypy-boto3-waf-regional==1.14.0.2"],
        "wafv2": ["mypy-boto3-wafv2==1.14.0.2"],
        "workdocs": ["mypy-boto3-workdocs==1.14.0.2"],
        "worklink": ["mypy-boto3-worklink==1.14.0.2"],
        "workmail": ["mypy-boto3-workmail==1.14.0.2"],
        "workmailmessageflow": ["mypy-boto3-workmailmessageflow==1.14.0.2"],
        "workspaces": ["mypy-boto3-workspaces==1.14.0.2"],
        "xray": ["mypy-boto3-xray==1.14.0.2"],
    },
    zip_safe=False,
)
