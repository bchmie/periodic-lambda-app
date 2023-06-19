from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import aws_lambda as _lambda, aws_lambda_python_alpha as python


class ApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_lambda = python.PythonFunction(
            self,
            "API function",
            entry="/home/bartek/Development/periodic-lambda-app",
            runtime=_lambda.Runtime.PYTHON_3_10,
            index="periodic_lambda_app/main.py",
            handler="handler",
            bundling=python.BundlingOptions(
                asset_excludes=[".venv", "cdk", "cdk_infra", "cdk.out", ".idea", ".git"]
            ),
        )
        url = api_lambda.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)

        CfnOutput(self, "ApiUrl", value=url.url)
