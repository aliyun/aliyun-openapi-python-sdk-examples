#encoding=utf-8
import json

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkslb.request.v20140515 import CreateLoadBalancerRequest
from aliyunsdkslb.request.v20140515 import DeleteLoadBalancerRequest
from sdk_lib.exception import ExceptionHandler

class LoadBalancer(object):
    def __init__(self, client):
        self.client = client


    def create_load_balancer(self, pay_type='', vpc_id='', vswitch_id=''):
        try:
            request = CreateLoadBalancerRequest.CreateLoadBalancerRequest()
            if pay_type:
                request.set_PayType(pay_type)
            if vpc_id:
                request.set_VpcId(vpc_id)
            if vswitch_id:
                request.set_VSwitchId(vswitch_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def create_load_balancer_private(self, pay_type, name, vpc_id, vswitch_id):
        try:
            request = CreateLoadBalancerRequest.CreateLoadBalancerRequest()
            request.set_PayType(pay_type)
            request.set_LoadBalancerName(name)
            request.set_VpcId(vpc_id)
            request.set_VSwitchId(vswitch_id)
            response = self.client.do_action_with_exception(request)

            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def delete_load_balancer(self, params):
        try:
            request = DeleteLoadBalancerRequest.DeleteLoadBalancerRequest()
            request.set_LoadBalancerId(params["load_balancer_id"])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)