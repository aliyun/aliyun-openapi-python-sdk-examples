#encoding=utf-8
import json
import time

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import DeleteRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import DescribeRouteTablesRequest
from sdk_lib.exception import ExceptionHandler
from sdk_lib.check_status import CheckStatus
from sdk_lib.consts import *

class RouteEntry(object):
    def __init__(self, client):
        self.client = client

    def create_route_entry(self, params):
        """
        create_route_entry: 创建route_entry路由条目
        官网API参考链接: https://help.aliyun.com/document_detail/36012.html
        """
        try:
            request = CreateRouteEntryRequest.CreateRouteEntryRequest()
            # 路由表ID
            request.set_RouteTableId(params['route_table_id'])
            # 自定义路由条目的目标网段
            request.set_DestinationCidrBlock(params['destination_cidr_block'])
            # 下一跳的类型
            request.set_NextHopType(params['nexthop_type'])
            # 下一跳实例的ID
            request.set_NextHopId(params['nexthop_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断router entry状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_route_entry_status,
                                        AVAILABLE, params['route_table_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def delete_route_entry(self, params):
        """
        delete_route_entry: 删除route_entry路由条目
        官网API参考链接: https://help.aliyun.com/document_detail/36013.html
        """
        try:
            request = DeleteRouteEntryRequest.DeleteRouteEntryRequest()
            # 路由条目所在的路由表的ID
            request.set_RouteTableId(params['route_table_id'])
            # 路由条目的目标网段
            request.set_DestinationCidrBlock(params['destination_cidr_block'])
            # 下一跳实例的ID
            request.set_NextHopId(params['nexthop_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            time.sleep(DEFAULT_TIME)
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_route_entry_vrouter(self, params):
        """
        describe_route_entry_vrouter: 查询route_entry路由条目
        官网API参考链接: https://help.aliyun.com/document_detail/36014.html
        """
        try:
            request = DescribeRouteTablesRequest.DescribeRouteTablesRequest()
            # 路由表所属的VPC路由器或边界路由器的ID
            request.set_VRouterId(params['vrouter_id'])
            # 路由表的ID
            request.set_RouteTableId(params['route_table_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_route_entry(self, route_table_id):
        """
        describe_route_entry: 查询route_entry路由条目
        官网API参考链接: https://help.aliyun.com/document_detail/36014.html
        """
        try:
            request = DescribeRouteTablesRequest.DescribeRouteTablesRequest()
            request.set_RouteTableId(route_table_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_route_entry_status(self, route_table_id):
        """
        describe_route_entry_status: 查询route_entry路由条目当前状态
        """
        response = self.describe_route_entry(route_table_id)
        return response["RouteTables"]["RouteTable"][0]["RouteEntrys"]["RouteEntry"][0]["Status"]