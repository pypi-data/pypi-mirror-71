"""
# Welcome to `cdk-gitlab-runner`

This repository template helps you create gitlab runner on your aws account via AWS CDK one line.

## Before start your need gitlab runner token in your  `gitlab project` or   `gitlab group`

### In Group

Group > Settings > CI/CD
![group](image/group_runner_page.png)

### In Group

Project > Settings > CI/CD > Runners
![project](image/project_runner_page.png)

## Usage Replace your gitlab runner roken in `$GITLABTOKEN`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner

# create a new github repository pahud/new-repo and import all files from ./lib to it
GitlabContainerRunner(stack, "testing", gitlabtoken="$GITLABTOKEN")
```

## Wait about 6 mins , If success you will see your runner in that page .

![runner](image/group_runner2.png)

#### you can use tag `gitlab` , `runner` , `awscdk`  ,

## Example     *`gitlab-ci.yaml`*

[gitlab docs see more ...](https://docs.gitlab.com/ee/ci/yaml/README.html)

```yaml
dockerjob:
  image: docker:18.09-dind
  variables:
  tags:
    - runner
    - awscdk
    - gitlab
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker info
  script:
    - docker info;
    - echo 'test 123';
    - echo 'hello world 1228'
```

### If your want to debug your can go to aws console

# `In your runner region !!!`

## AWS Systems Manager  >  Session Manager  >  Start a session

#### click your `runner` and click `start session`

#### in the brower console in put `bash`

```bash
# become to root
sudo -i

# list runner container .
root# docker ps -a
```
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

import aws_cdk.core


class GitlabContainerRunner(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-gitlab-runner.GitlabContainerRunner"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, gitlabtoken: str) -> None:
        """
        :param scope: -
        :param id: -
        :param gitlabtoken: 

        stability
        :stability: experimental
        """
        props = GitlabContainerRunnerProps(gitlabtoken=gitlabtoken)

        jsii.create(GitlabContainerRunner, self, [scope, id, props])


@jsii.data_type(jsii_type="cdk-gitlab-runner.GitlabContainerRunnerProps", jsii_struct_bases=[], name_mapping={'gitlabtoken': 'gitlabtoken'})
class GitlabContainerRunnerProps():
    def __init__(self, *, gitlabtoken: str) -> None:
        """
        :param gitlabtoken: 

        stability
        :stability: experimental
        """
        self._values = {
            'gitlabtoken': gitlabtoken,
        }

    @builtins.property
    def gitlabtoken(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('gitlabtoken')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitlabContainerRunnerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "GitlabContainerRunner",
    "GitlabContainerRunnerProps",
]

publication.publish()
