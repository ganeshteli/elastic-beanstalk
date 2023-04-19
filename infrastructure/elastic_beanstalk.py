from os import path
from aws_cdk import Stack, aws_elasticbeanstalk as elasticbeanstalk
from constructs import Construct


class ElasticBeanstalkStack(Stack):
	def __init__(self, scope:Construct, construct_id:str, **kwargs) ->	None:
		super().__init__(scope,construct_id,**kwargs)

		app_name = "ElasticBeanstalkCdkApp"
		app =elasticbeanstalk.CfnApplication(self, "Application", application_name=app_name)
		eb_env = elasticbeanstalk.CfnEnvironment(self, "ebs-env", application_name=app_name)

		if path.exists('flask-app/app.zip'):
			
			eb_zip_app = assets.Asset(self, "eb-asset-app",
			    path=path.join(sys.path[0], "flask-app/app.zip")
			)

			app_version_props = elasticbeanstalk.CfnApplicationVersion(self, 
				"MyCfnApplicationVersion",
	        	application_name=app_name,
		    	source_bundle=elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty(
		    		s3_bucket=eb_zip_app.s3BucketName,
		    		s3_key=eb_zip_app.s3ObjectKey,
		    	),
			)

			cfn_environment = elasticbeanstalk.CfnEnvironment(self, 
				"MyCfnEnvironment",
				application_name=app_name,
			    environment_name=eb_env,
			    operations_role="operationsRole",
			    option_settings=[elasticbeanstalk.CfnEnvironment.OptionSettingProperty(
			        namespace="aws:autoscaling:launchconfiguration",
			    	option_name="InstanceType",
			    	value="t2.micro"
			    )],
			    version_label=app_version_props.ref,
			)

			app_version_props.addDependsOn(app);