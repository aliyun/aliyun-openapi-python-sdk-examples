#encoding=utf-8
import sys
import json
from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import DeleteRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import DescribeRouterInterfacesRequest
from aliyunsdkvpc.request.v20160428 import ConnectRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import DeactivateRouterInterfaceRequest
from aliyunsdkvpc.request.v20160428 import ModifyRouterInterfaceAttributeRequest
from sdk_lib.sdk_route_entry import RouteEntry
from sdk_lib.exception import ExceptionHandler
from sdk_lib.common_util import CommonUtil
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

def main():

    router_interface = RouterInterface(client)
    route_entry = RouteEntry(client)

    params = {}
    params['spec'] = "Large.2"
    params['role'] = "InitiatingSide"
    params['router_id'] = ROUTER_ID
    params['router_type'] = "VRouter"
    params['opposite_region_id'] = "cn-hangzhou"
    params['opposite_router_type'] = "VRouter"

    # 创建发起端ri
    router_interface_json = router_interface.create_router_interface(params)
    CommonUtil.log("create_router_interface", router_interface_json)

    # 创建接收端ri
    params['spec'] = "Negative"
    params['role'] = "AcceptingSide"
    params['router_id'] = ROUTER_ID2
    router_interface_json2 = router_interface.create_router_interface(params)
    CommonUtil.log("create_router_interface", router_interface_json2)

    # 修改发起端ri信息
    params['router_interface_id'] = router_interface_json['RouterInterfaceId']
    params['opposite_interface_id'] = router_interface_json2['RouterInterfaceId']
    params['opposite_router_id'] = ROUTER_ID2
    modify_ri_json = router_interface.modify_router_interface_attribute(params)
    CommonUtil.log("modify_router_interface_attribute", modify_ri_json)

    # 修改接收端ri信息
    params['router_interface_id'] = router_interface_json2['RouterInterfaceId']
    params['opposite_interface_id'] = router_interface_json['RouterInterfaceId']
    params['opposite_router_id'] = ROUTER_ID
    modify_ri_json2 = router_interface.modify_router_interface_attribute(params)
    CommonUtil.log("modify_router_interface_attribute", modify_ri_json2)

    # 查询发起端ri信息
    describe_ri_json = router_interface.describe_router_interface(router_interface_json['RouterInterfaceId'])
    CommonUtil.log("describe_router_interface", describe_ri_json)

    # 查询接收端ri信息
    describe_ri_json2 = router_interface.describe_router_interface(router_interface_json2['RouterInterfaceId'])
    CommonUtil.log("describe_router_interface", describe_ri_json2)

    # 发起连接
    params['router_interface_id'] = router_interface_json['RouterInterfaceId']
    connect_ri_json = router_interface.connect_router_interface(params)
    CommonUtil.log("connect_router_interface", connect_ri_json)

    # 创建下一跳为发起端ri的路由条目
    params['route_table_id'] = TABLE_ID
    params['destination_cidr_block'] = "0.0.0.0/0"
    params['nexthop_type'] = 'RouterInterface'
    params['nexthop_id'] = router_interface_json['RouterInterfaceId']
    route_entry_json = route_entry.create_route_entry(params)
    CommonUtil.log("create_route_entry", route_entry_json)

    # 创建下一跳为接收端ri的路由条目
    params['route_table_id'] = TABLE_ID2
    params['destination_cidr_block'] = "0.0.0.0/0"
    params['nexthop_type'] = 'RouterInterface'
    params['nexthop_id'] = router_interface_json2['RouterInterfaceId']
    route_entry_json2 = route_entry.create_route_entry(params)
    CommonUtil.log("create_route_entry", route_entry_json2)

    # 删除下一跳为接收端ri的路由条目
    route_entry_json = route_entry.delete_route_entry(params)
    CommonUtil.log("delete_route_entry", route_entry_json)

    # 删除下一跳为发起端ri的路由条目
    params['route_table_id'] = TABLE_ID
    params['nexthop_id'] = router_interface_json['RouterInterfaceId']
    route_entry_json = route_entry.delete_route_entry(params)
    CommonUtil.log("delete_route_entry", route_entry_json)

    # 冻结发起端ri
    params['router_interface_id'] = router_interface_json['RouterInterfaceId']
    deactivate_ri_json = router_interface.deactivate_router_interface(params)
    CommonUtil.log("deactivate_router_interface", deactivate_ri_json)

    # 冻结接收端ri
    params['router_interface_id'] = router_interface_json2['RouterInterfaceId']
    deactivate_ri_json2 = router_interface.deactivate_router_interface(params)
    CommonUtil.log("deactivate_router_interface", deactivate_ri_json2)

    # 删除发起端ri
    params['instance_id'] = router_interface_json['RouterInterfaceId']
    router_interface_json = router_interface.delete_router_interface(params)
    CommonUtil.log("delete_router_interface", router_interface_json)

    # 删除接收端ri
    params['instance_id'] = router_interface_json2['RouterInterfaceId']
    router_interface_json2 = router_interface.delete_router_interface(params)
    CommonUtil.log("delete_router_interface", router_interface_json2)


if __name__ == '__main__':
    sys.exit(main())
