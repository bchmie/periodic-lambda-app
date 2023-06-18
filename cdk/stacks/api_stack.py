from os import path
from pathlib import Path

from aws_cdk import Stack, BundlingOptions, CfnOutput, IgnoreMode, BundlingFileAccess
from constructs import Construct
from aws_cdk import aws_lambda as _lambda


class ApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_lambda = _lambda.Function(
            self,
            "API function",
            code=_lambda.Code.from_asset(
                ".",  # path is relative from app.py, i.e. project root
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_10.bundling_image,
                    bundling_file_access=BundlingFileAccess.VOLUME_COPY,
                    command=[
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ]
                ),
                ignore_mode=IgnoreMode.DOCKER
            ),
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="main.handler",
        )
        url = api_lambda.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)

        CfnOutput(self, "ApiUrl", value=url.url)
