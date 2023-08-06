# cdk-fargate-express

Deploy your serverless Express app in AWS with AWS CDK

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_fargate_express import ExpressService

ExpressService(stack, "testing",
    vpc=vpc,
    # define your local express assets directory containing the Dockerfile
    docker_assets=path.join(__dirname, "../express.d")
)
```
