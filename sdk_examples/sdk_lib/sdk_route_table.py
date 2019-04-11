#encoding=utf-8
import json
import time

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import DeleteRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import AssociateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import UnassociateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import DescribeRouteTablesRequest
from sdk_lib.exception import ExceptionHandler
from sdk_lib.check_status import CheckStatus
from sdk_lib.consts import *

class RouteTable(object):
    def __init__(self, client):
        self.client = client

    def create_route_table(self, params):
        """
        create_route_table: 创建一个自定义路由表
        官网API参考链接: https://help.aliyun.com/document_detail/87586.html
        """
        try:
            request = CreateRouteEntryRequest.CreateRouteEntryRequest()
            request.set_action_name("CreateRouteTable")
            # 自定义路由表所属的VPC ID
            request.add_query_param("VpcId", params['vpc_id'])
            # 路由表的名称
            request.add_query_param("RouteTableName", params['route_table_name'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            route_table_id = response_json['RouteTableId']
            # 判断route table状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME * 5,
                                        self.describe_route_table_status,
                                        route_table_id, route_table_id):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def associate_route_table(self, params):
        """
        associate_route_table: 将创建的自定义路由表和同一VPC内的交换机绑定
        官网API参考链接: https://help.aliyun.com/document_detail/87599.html
        """
        try:
            request = AssociateEipAddressRequest.AssociateEipAddressRequest()
            request.set_action_name("AssociateRouteTable")
            # 路由表ID
            request.add_query_param("RouteTableId", params['route_table_id'])
            # 要绑定的交换机ID
            request.add_query_param("VSwitchId", params['vswitch_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            time.sleep(DEFAULT_TIME * 5)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def unassociate_route_table(self, params):
        """
        unassociate_route_table: 将路由表和交换机解绑
        官网API参考链接: https://help.aliyun.com/document_detail/87628.html
        """
        try:
            request = UnassociateEipAddressRequest.UnassociateEipAddressRequest()
            request.set_action_name("UnassociateRouteTable")
            # 路由表ID
            request.add_query_param("RouteTableId", params['route_table_id'])
            # 要解绑的交换机ID
            request.add_query_param("VSwitchId", params['vswitch_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            time.sleep(DEFAULT_TIME * 5)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def delete_route_table(self, params):
        """
        delete_route_table: 删除自定义路由表
        官网API参考链接: https://help.aliyun.com/document_detail/87601.html
        """
        try:
            request = DeleteRouteEntryRequest.DeleteRouteEntryRequest()
            request.set_action_name("DeleteRouteTable")
            # 路由表ID
            request.add_query_param("RouteTableId", params['route_table_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断route table是否被删除成功
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME * 5,
                                        self.describe_route_table_status,
                                        '', params['route_table_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_route_table(self, route_table_id):
        """
        describe_route_table: 查询路由表
        官网API参考链接: https://help.aliyun.com/document_detail/36014.html
        """
        try:
            request = DescribeRouteTablesRequest.DescribeRouteTablesRequest()
            # 路由表的ID
            request.set_RouteTableId(route_table_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_route_table_status(self, route_table_id):
        """
        describe_route_table_status: 查询路由表状态
        """
        response = self.describe_route_table(route_table_id)
        if len(response["RouteTables"]["RouteTable"]) == 0:
            return ''
        return response["RouteTables"]["RouteTable"][0]["RouteTableId"]