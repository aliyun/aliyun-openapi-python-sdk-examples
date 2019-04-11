#encoding=utf-8
import sys
import json
import time

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import DeleteRouteEntryRequest
from aliyunsdkvpc.request.v20160428 import AssociateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import UnassociateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import DescribeRouteTablesRequest
from sdk_lib.common_util import CommonUtil
from sdk_lib.sdk_vpc import Vpc
from sdk_lib.sdk_vswitch import VSwitch
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

def main():
    client = ACS_CLIENT

    vpc = Vpc(client)
    vswitch = VSwitch(client)
    route_table = RouteTable(client)

    params = {}
    params['cidr_block'] = "172.16.1.0/24"
    params['zone_id'] = "cn-hangzhou-d"
    params['route_table_name'] = "sdk_route_table"

    #创建vpc
    vpc_json = vpc.create_vpc()
    CommonUtil.log("create_vpc", vpc_json)

    #创建vswitch
    params['vpc_id'] = vpc_json['VpcId']
    vswitch_json = vswitch.create_vswitch(params)
    CommonUtil.log("create_vswitch", vswitch_json)

    #创建route table
    route_table_json = route_table.create_route_table(params)
    CommonUtil.log("create_route_table", route_table_json)

    #查询vswitch
    params['vswitch_id'] = vswitch_json['VSwitchId']
    vswitch_json = vswitch.describe_vswitch_attribute(params['vswitch_id'])
    CommonUtil.log("describe_vswitch_attribute", vswitch_json)

    #route table绑定vswitch
    params['route_table_id'] = route_table_json['RouteTableId']
    associate_json = route_table.associate_route_table(params)
    CommonUtil.log("associate_route_table", associate_json)

    #route table解绑vswitch
    unassociate_json = route_table.unassociate_route_table(params)
    CommonUtil.log("unassociate_route_table", unassociate_json)

    #删除route table
    delete_route_table_json = route_table.delete_route_table(params)
    CommonUtil.log("delete_route_table", delete_route_table_json)

    #删除vswitch
    delete_vswitch_json = vswitch.delete_vswitch(params)
    CommonUtil.log("delete_vswitch", delete_vswitch_json)

    #删除vpc
    delete_vpc_json = vpc.delete_vpc(params)
    CommonUtil.log("delete_vpc", delete_vpc_json)

if __name__ == "__main__":
    sys.exit(main())