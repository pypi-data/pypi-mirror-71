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
