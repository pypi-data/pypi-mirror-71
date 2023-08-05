from localstack.utils.aws import aws_models
USuNJ=super
USuNX=None
USuNe=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  USuNJ(LambdaLayer,self).__init__(arn)
  self.cwd=USuNX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,USuNe,env=USuNX):
  USuNJ(RDSDatabase,self).__init__(USuNe,env=env)
 def name(self):
  return self.USuNe.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
