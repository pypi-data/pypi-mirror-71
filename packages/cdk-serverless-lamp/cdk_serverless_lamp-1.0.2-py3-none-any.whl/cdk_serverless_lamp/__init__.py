"""
[![NPM version](https://badge.fury.io/js/cdk-serverless-lamp.svg)](https://badge.fury.io/js/cdk-serverless-lamp)
[![PyPI version](https://badge.fury.io/py/cdk-serverless-lamp.svg)](https://badge.fury.io/py/cdk-serverless-lamp)
![Release](https://github.com/pahud/cdk-serverless-lamp/workflows/Release/badge.svg)

# Welcome to `cdk-serverless-lamp`

A JSII construct library for AWS CDK to build the [New Serverless LAMP Stack](https://aws.amazon.com/tw/blogs/compute/introducing-the-new-serverless-lamp-stack/)

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_serverless_lamp import ServerlessApi

ServerlessApi(self, "API")
```

On deploy complete, the API Gateway URL will be returned in the Output. Click the URL and you will see the Laravel landing page:

![laravel-welcome](./images/laravel.png)

## Prepare the Laravel and bref

```bash
$ git clone https://github.com/pahud/cdk-serverless-lamp.git
$ cd cdk-serverless-lamp
$ mkdir composer && cd composer
# create a laravel project
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer create-project laravel/laravel laravel58-bref --prefer-dist
# enter this project
$ cd laravel58-bref
# install bref in the vendor
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer require bref/bref
```

## Configure Laravel with Bref for Lambda

According to the Bref [document](https://bref.sh/docs/frameworks/laravel.html), we need configure the environment before it can be deployed on Lambda:

edit the `.env` file

```
VIEW_COMPILED_PATH=/tmp/storage/framework/views

# We cannot store sessions to disk: if you don't need sessions (e.g. API) then use `array`
# If you write a website, use `cookie` or store sessions in database.
SESSION_DRIVER=cookie

# Logging to stderr allows the logs to end up in Cloudwatch
LOG_CHANNEL=stderr
```

edit the `app/Providers/AppServiceProvider.php`

```php
    public function boot()
    {
        // Make sure the directory for compiled views exist
        if (! is_dir(config('view.compiled'))) {
            mkdir(config('view.compiled'), 0755, true);
        }
    }
```

edit `bootstrap/app.php`

```php

$app = new Illuminate\Foundation\Application(
    $_ENV['APP_BASE_PATH'] ?? dirname(__DIR__)
);

// add the following statement
// we will configure APP_STORAGE = '/tmp' in Lambda env var
$app->useStoragePath($_ENV['APP_STORAGE'] ?? $app->storagePath());
```

*(credit to [@azole](https://medium.com/@azole/deploy-serverless-laravel-by-bref-6f28b1e0d53a))*

## TODO

* Add Aurora for MySQL stack
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_lambda
import aws_cdk.core


class ServerlessApi(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-serverless-lamp.ServerlessApi"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, handler: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, lambda_code_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param handler: custom lambda function for the API. Default: - A Lambda function with Lavavel and Bref support will be created
        :param lambda_code_path: custom lambda code asset path. Default: - DEFAULT_LAMBDA_ASSET_PATH

        stability
        :stability: experimental
        """
        props = ServerlessApiProps(handler=handler, lambda_code_path=lambda_code_path)

        jsii.create(ServerlessApi, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> aws_cdk.aws_lambda.IFunction:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "handler")


@jsii.data_type(jsii_type="cdk-serverless-lamp.ServerlessApiProps", jsii_struct_bases=[], name_mapping={'handler': 'handler', 'lambda_code_path': 'lambdaCodePath'})
class ServerlessApiProps():
    def __init__(self, *, handler: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, lambda_code_path: typing.Optional[str]=None) -> None:
        """
        :param handler: custom lambda function for the API. Default: - A Lambda function with Lavavel and Bref support will be created
        :param lambda_code_path: custom lambda code asset path. Default: - DEFAULT_LAMBDA_ASSET_PATH

        stability
        :stability: experimental
        """
        self._values = {
        }
        if handler is not None: self._values["handler"] = handler
        if lambda_code_path is not None: self._values["lambda_code_path"] = lambda_code_path

    @builtins.property
    def handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """custom lambda function for the API.

        default
        :default: - A Lambda function with Lavavel and Bref support will be created

        stability
        :stability: experimental
        """
        return self._values.get('handler')

    @builtins.property
    def lambda_code_path(self) -> typing.Optional[str]:
        """custom lambda code asset path.

        default
        :default: - DEFAULT_LAMBDA_ASSET_PATH

        stability
        :stability: experimental
        """
        return self._values.get('lambda_code_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerlessApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ServerlessApi",
    "ServerlessApiProps",
]

publication.publish()
