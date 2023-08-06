# cdk-fargate-express

Deploy your serverless Express app in AWS with AWS CDK

## Usage

On deployment, AWS CDK executs `docker build` with your Express code assets at `express.d`

For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_fargate_express import ExpressService

ExpressService(stack, "testing", vpc=vpc)
```

You may specify different folder by specifying `expressAssets` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ExpressService(stack, "testing",
    vpc=vpc,
    express_assets=path.join(__dirname, "../another_express.d")
)
```
