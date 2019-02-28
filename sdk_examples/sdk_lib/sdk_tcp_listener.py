#encoding=utf-8
import json

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from sdk_lib.consts import *
from aliyunsdkslb.request.v20140515 import CreateLoadBalancerTCPListenerRequest
from sdk_lib.exception import ExceptionHandler

class TcpListener(object):
    def __init__(self, client):
        self.client = client

    def create_tcp_listener(self, params):
        '''
        create_tcp_listener：创建tcp监听
        官网API参考链接: https://help.aliyun.com/document_detail/27594.html
        '''
        counter = 0
        while counter < TRY_TIME:
            try:
                request = CreateLoadBalancerTCPListenerRequest.CreateLoadBalancerTCPListenerRequest()
                # 负载均衡实例的ID
                request.set_LoadBalancerId(params["load_balancer_id"])
                # 监听的带宽峰值
                request.set_Bandwidth(params["bandwidth"])
                # 负载均衡实例前端使用的端口
                request.set_ListenerPort(params["listener_port"])
                # 负载均衡实例后端使用的端口
                request.set_BackendServerPort(params["backend_server_port"])
                response = self.client.do_action_with_exception(request)
                response_json = json.loads(response)
                return response_json
            except ServerException as e:
                ExceptionHandler.server_exception(e)
            except ClientException as e:
                ExceptionHandler.client_exception(e)
            finally:
                counter += 1