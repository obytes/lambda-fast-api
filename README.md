# AWS Lambda Fast API

Fast API starter application compatible with API Gateway and Lambda Function.


## How to deploy it?

[Terraform AWS Lambda API](https://github.com/obytes/terraform-aws-lambda-api) is a reusable module that can be used to
deploy this Fast Application and It will provision:

- The AWS Lambda Function resources
- The AWS Lambda Function CI/CD resources
- The AWS API Gateway HTTP API resources

## Structure

This Fast Application is using [Mangum](https://github.com/jordaneremieff/mangum) to adapt AWS API Gateway events to 
ASGI requests.

When creating the Lambda Function, make sure that the handler is set to the Adapter Object which is in our case
`app.runtime.lambda.main.handler`.

## Environment variable

- **FIREBASE_APP_API_KEY**: Firebase web application API Key.
- **AWS_API_GW_MAPPING_KEY**: The mapping key used in AWS API Gateway to map the API with custom domain.
- **RUNTIME**: should be `LAMBDA` when deploying to `LAMBDA`
- **AWS_API_GW_STAGE_NAME**: should be the same as the one used with API Gateway
- **JWT_AUTHORIZATION_GROUPS_ATTR_NAME**: the JWT claim attribute name from where to get RBAC roles.

## Blueprints

AWS API Gateway sends Requests HTTP Paths that already contains a stage name to Lambda Function and the Fast
application will not be able to match the request with the available target routes.

To make sure all blueprints routes match the path sent from API Gateway, for each request the adapter will strip the API
Gateway stage name **`AWS_API_GW_STAGE_NAME`** from the original HTTP Path.

The [Terraform AWS Lambda API](https://github.com/obytes/terraform-aws-lambda-api) reusable modules will ensure that the
same stage name is used for both AWS API Gateway and Fast Application so this logic can work.

## Endpoints

To test all use cases we added a public endpoint, a private endpoint and an admin endpoint:

- **Public Endpoint**: simple health check endpoint.

- **Auth Endpoint**: OAuth Password Authentication Flow.

- **Private Endpoint**: `whoami` endpoint that returns to the calling user his JWT decoded claims.

- **Admin Endpoint**: returns to site admins the available Fast routes as a list.

- **Docs Endpoint**: Swagger docs.

## Authentication & Authorization

### Authentication

The public endpoints will be open for all users without prior authentication but how about the private and admin
endpoints? They certainly need an authentication system in place, for that we will not reinvent the wheel, and we will
leverage an IaaS (Identity as a Service) provider like Firebase.

We have agreed to use an IaaS to authenticate users but how we can to verify the users issued JWT tokens? fortunately,
AWS API Gateway can take that burden and it can:

- Allow only access tokens that passed integrity check.
- Verify that access tokens not yet expired.
- Verify that access token is issued for an audience which is in the whitelisted audiences list.
- Verify that access token has sufficient OAuth scopes to consume the endpoint.

### Authorization

Authorization is an important aspect when building APIs, so we want certain functionalities/endpoints to be available to
only a subset of our users. to achieve that there are two famous approaches to tackle that Role Based Access Control
(RBAC) and OAuth Scopes Authorization.

#### Role Based Access Control (RBAC)

We have achieved that by implementing a Role Based Access Control (RBAC) model. where we assign each user a role or
roles by adding them to groups and then decorate each route with the list of groups that can consume it.

When using an Identity as a Service providers like Auth0, Firebase and Cognito make sure to assign users to groups and
during user's authentication, the JWT tokens service will embed the user's groups into the JWT Access/ID tokens claims

After authenticating to Identity Provider, the user can send their JWT access token to API Gateway that will verify the
token integrity/expiration and dispatch the request with decoded JWT token to Lambda Function. Finally, the Lambda
Function will compare user's `groups` claim with the whitelisted groups at route level and decide to allow it or
forbid it.

This approach comes with many benefits but also with drawbacks:

- Requests will not be authorized at the API Gateway level, and they need to travel to Lambda Function to run
  authorization logic.

- Authorization rules will be writen in code, which will be messy from a DevOps perspective but a backend developers
  will favour that because they will have better visibility when coding/debugging, and they will know who can call any
  endpoint without going to infrastructure code.

#### OAuth Scopes Authorization

The second approach is by using OAuth Scopes Authorization model, and for each functionality/route we have to:

- Create an OAuth scope.
- Assign users the list of OAuth scopes that they can claim.
- At API Gateway level specify the list of OAuth scopes that the user should have at least one of them for the API
  Gateway to let it reach the Lambda Function API.

The advantages of this approach are:

- The ability to change permissions scopes at Identity Provider and API Gateway Level without changing/deploying new
  code.
- Unauthorized requests will be revoked at API Gateway Level and before reaching the Lambda Function.

The [Terraform AWS Lambda API](https://github.com/obytes/terraform-aws-lambda-api) module supports this authorization
model and you can customize it using the module's `routes_definitions` Terraform variable.
