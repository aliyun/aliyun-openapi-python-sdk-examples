#encoding=utf-8
import json
from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import DeleteRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import DescribeRouterInterfacesRequest
from aliyunsdkvpc.request.v20160428 import ConnectRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import DeactivateRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import ModifyRouterInterfaceAttributeRequest
from sdk_lib.exception import ExceptionHandler
from sdk_lib.check_status import CheckStatus
from sdk_lib.consts import *

client = ACS_CLIENT

class RouterInterface(object):
    def __init__(self, client):
        self.client = client

    def create_router_interface(self, params):
        """
        create_router_interface: 创建路由器接口
        官网API参考: https://help.aliyun.com/document_detail/36032.html
        """
        try:
            request = CreateRouterInterfaceRequest.CreateRouterInterfaceRequest()
            # 路由器接口的规格
            request.set_Spec(params['spec'])
            # 路由器接口的角色
            request.set_Role(params['role'])
            # 路由器接口关联的路由器ID
            request.set_RouterId(params['router_id'])
            # 路由器接口关联的路由器类型
            request.set_RouterType(params['router_type'])
            # 连接接收端所在的地域ID
            request.set_OppositeRegionId(params['opposite_region_id'])
            # 对端路由器接口关联的路由器类型
            request.set_OppositeRouterType(params['opposite_router_type'])

            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断Router Interface状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_ri_status,
                                        'Idle', response_json['RouterInterfaceId']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def connect_router_interface(self, params):
        """
        connect_router_interface: 由发起端路由器接口向接收端发起连接
        官网API参考: https://help.aliyun.com/document_detail/36031.html
        """
        try:
            request = ConnectRouterInterfaceRequest.ConnectRouterInterfaceRequest()
            # 发起端路由器接口的ID
            request.set_RouterInterfaceId(params['router_interface_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            if CheckStatus.check_status(TIME_DEFAULT_OUT * 5, DEFAULT_TIME * 5,
                                        self.describe_ri_status,
                                        'Active', params['router_interface_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def deactivate_router_interface(self, params):
        """
        deactivate_router_interface: 冻结路由器接口
        官网API参考: https://help.aliyun.com/document_detail/36033.html
        """
        try:
            request = DeactivateRouterInterfaceRequest.DeactivateRouterInterfaceRequest()
            # 路由器接口的ID
            request.set_RouterInterfaceId(params['router_interface_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断Router Interface状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT * 5, DEFAULT_TIME * 5,
                                        self.describe_ri_status,
                                        'Inactive', params['router_interface_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def modify_router_interface_attribute(self, params):
        """
        modify_router_interface_attribute: 修改路由器接口的配置
        官网API参考: https://help.aliyun.com/document_detail/36036.html
        """
        try:
            request = ModifyRouterInterfaceAttributeRequest.ModifyRouterInterfaceAttributeRequest()
            # 路由器接口的ID
            request.set_RouterInterfaceId(params['router_interface_id'])
            # 对端路由器接口ID
            request.set_OppositeInterfaceId(params['opposite_interface_id'])
            # 对端的路由器的ID
            request.set_OppositeRouterId(params['opposite_router_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断Router Interface状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_ri_status,
                                        'Idle', params['router_interface_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)



    def describe_router_interface(self, instance_id):
        """
        describe_router_interface: 查询指定地域内的路由器接口
        官网API参考: https://help.aliyun.com/document_detail/36035.html
        """
        try:
            request = DescribeRouterInterfacesRequest.DescribeRouterInterfacesRequest()
            # 查询的过滤类型
            request.add_query_param('Filter.1.Key', "RouterInterfaceId")
            # 查询的实例ID
            request.add_query_param('Filter.1.Value.1', instance_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_ri_status(self, instance_id):
        """
        describe_ri_status: 查询指定地域内的路由器接口状态
        官网API参考: https://help.aliyun.com/document_detail/36035.html
        """
        response = self.describe_router_interface(instance_id)
        if len(response['RouterInterfaceSet']['RouterInterfaceType']) == 0:
            return ''
        return response['RouterInterfaceSet']['RouterInterfaceType'][0]['Status']

    def delete_router_interface(self, params):
        """
        delete_router_interface: 删除路由器接口
        官网API参考: https://help.aliyun.com/document_detail/36034.html
        """
        try:
            request = DeleteRouterInterfaceRequest.DeleteRouterInterfaceRequest()
            # 路由器接口的ID
            request.set_RouterInterfaceId(params['instance_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断Router Interface状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME * 5,
                                        self.describe_ri_status,
                                        '', params['instance_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)