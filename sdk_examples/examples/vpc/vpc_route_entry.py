#encoding=utf-8
import sys
import json
import time

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import DeleteRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import DescribeRouteTablesRequest
from sdk_lib.exception import ExceptionHandler
from sdk_lib.check_status import CheckStatus
from sdk_lib.common_util import CommonUtil
from sdk_lib.sdk_vswitch import VSwitch
from sdk_lib.sdk_route_table import RouteTable
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
            return response_json
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

def main():
    client = ACS_CLIENT
    vswitch = VSwitch(client)
    route_table = RouteTable(client)
    route_entry = RouteEntry(client)

    params = {}
    params['route_table_name'] = "sdk_route_table"
    params['destination_cidr_block'] = "0.0.0.0/0"
    params['nexthop_id'] = "i-xxx"
    params['nexthop_type'] = "Instance"

    params['vpc_id'] = "vpc-xxx"
    params['vswitch_id'] = "vsw-xxx"

    #创建route table
    route_table_json = route_table.create_route_table(params)
    CommonUtil.log("create_route_table", route_table_json)

    #查询vswitch
    vswitch_json = vswitch.describe_vswitch_attribute(params)
    CommonUtil.log("describe_vswitch_attribute", vswitch_json)

    #route table绑定vswitch
    params['route_table_id'] = route_table_json['RouteTableId']
    associate_json = route_table.associate_route_table(params)
    CommonUtil.log("associate_route_table", associate_json)

    #创建路由条目
    create_route_entry_json = route_entry.create_route_entry(params)
    CommonUtil.log("create_route_entry", create_route_entry_json)
    
    #删除路由条目
    delete_route_entry_json = route_entry.delete_route_entry(params)
    CommonUtil.log("delete_route_entry", delete_route_entry_json)

    #route table解绑vswitch
    unassociate_json = route_table.unassociate_route_table(params)
    CommonUtil.log("unassociate_route_table", unassociate_json)

    #删除route table
    delete_route_table_json = route_table.delete_route_table(params)
    CommonUtil.log("delete_route_table", delete_route_table_json)


if __name__ == "__main__":
    sys.exit(main())