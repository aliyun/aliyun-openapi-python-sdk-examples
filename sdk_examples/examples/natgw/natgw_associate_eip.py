#encoding=utf-8
import sys
import json
import time

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateNatGatewayRequest
from aliyunsdkvpc.request.v20160428 import DeleteNatGatewayRequest
from aliyunsdkvpc.request.v20160428 import DescribeNatGatewaysRequest
from sdk_lib.sdk_vpc import Vpc
from sdk_lib.sdk_vswitch import VSwitch
from sdk_lib.sdk_eip import Eip
from sdk_lib.sdk_cbwp import CommonBandwidthPackage
from sdk_lib.common_util import CommonUtil
from sdk_lib.check_status import CheckStatus
from sdk_lib.exception import ExceptionHandler
from sdk_lib.consts import *

client = ACS_CLIENT


class NatGateway(object):
    def __init__(self, client):
        self.client = client

    def create_nat_gateway(self, params):
        """
        create_nat_gateway: 创建nat gateway
        官网API参考: https://help.aliyun.com/document_detail/36048.html
        """
        try:
            request = CreateNatGatewayRequest.CreateNatGatewayRequest()
            request.set_VpcId(params['vpc_id'])
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断Nat Gateway状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_nat_gateway_status,
                                        AVAILABLE, response_json['NatGatewayId']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_nat_gateway(self, nat_gateway_id):
        """
        describe_nat_gateway: 查询指定地域已创建的nat gateway的信息
        官网API参考: https://help.aliyun.com/document_detail/36054.html
        """
        try:
            request = DescribeNatGatewaysRequest.DescribeNatGatewaysRequest()
            request.set_NatGatewayId(nat_gateway_id)
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def delete_nat_gateway(self, params):
        """
        delete_nat_gateway: 删除nat gateway
        官网API参考: https://help.aliyun.com/document_detail/36051.html
        """
        try:
            request = DeleteNatGatewayRequest.DeleteNatGatewayRequest()
            request.set_NatGatewayId(params['nat_gateway_id'])
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断Nat Gateway状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME * 5,
                                        self.describe_nat_gateway_status,
                                        '', params['nat_gateway_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_nat_gateway_status(self, nat_gateway_id):
        """
        describe_nat_gateway_status: 查询指定地域已创建的nat gateway的状态
        官网API参考: https://help.aliyun.com/document_detail/36054.html
        """
        response = self.describe_nat_gateway(nat_gateway_id)
        if len(response["NatGateways"]["NatGateway"]) == 0:
            return ''
        return response["NatGateways"]["NatGateway"][0]['Status']


def main():
    vpc = Vpc(client)
    vswitch = VSwitch(client)
    eip = Eip(client)
    cbwp = CommonBandwidthPackage(client)
    nat_gateway = NatGateway(client)

    params = {}

    # 创建vpc
    vpc_json = vpc.create_vpc()
    CommonUtil.log("create_vpc", vpc_json)

    # 创建vswitch
    params['vpc_id'] = vpc_json['VpcId']
    params['zone_id'] = "cn-hangzhou-d"
    params['cidr_block'] = "172.16.1.0/24"
    vswitch_json = vswitch.create_vswitch(params)
    CommonUtil.log("create_vswitch", vswitch_json)

    # 创建natgw
    nat_gateway_json = nat_gateway.create_nat_gateway(params)
    CommonUtil.log("create_nat_gateway", nat_gateway_json)

    # 创建EIP
    eip_response_json = eip.allocate_eip_address(params)
    CommonUtil.log("allocate_eip_address", eip_response_json)
    params['allocation_id'] = eip_response_json["AllocationId"]

    # 绑定EIP到NAT网关
    params['instance_id'] = nat_gateway_json['NatGatewayId']
    params['allocation_id'] = eip_response_json["AllocationId"]
    params['instance_type'] = 'Nat'
    eip_response_json = eip.associate_eip_address(params)
    CommonUtil.log("associate_eip_address eip", eip_response_json)

    # 查询EIP
    eip_response_json = eip.describe_eip_address(params['allocation_id'])
    CommonUtil.log("describe_eip_address", eip_response_json)

    # 创建带宽包
    params['bandwidth'] = BANDWIDTH_10
    cbwp_repsonse_json = cbwp.create_common_bandwidth_package(params)
    CommonUtil.log("create_common_bandwidth_package", cbwp_repsonse_json)

    # 添加EIP到共享带宽包中
    params['ip_instance_id'] = params['allocation_id']
    params['bandwidth_package_id'] = cbwp_repsonse_json['BandwidthPackageId']
    cbwp_repsonse_json = cbwp.add_common_bandwidth_packageIp(params)
    CommonUtil.log("add_common_bandwidth_packageIp", cbwp_repsonse_json)

    # 查询natgw
    params['nat_gateway_id'] = nat_gateway_json['NatGatewayId']
    nat_gateway_json = nat_gateway.describe_nat_gateway(params['nat_gateway_id'])
    CommonUtil.log("describe_nat_gateway", nat_gateway_json)

    # 解绑EIP
    eip_response_json = eip.unassociate_eip_address(params)
    CommonUtil.log("unassociate_eip_address nat", eip_response_json)

    # 移除共享带宽包中的EIP（
    cbwp_repsonse_json = cbwp.remove_common_bandwidth_packageIp(params)
    CommonUtil.log("remove_common_bandwidth_packageIp", cbwp_repsonse_json)

    # 删除共享带宽包
    params['force'] = True
    cbwp_repsonse_json = cbwp.delete_common_bandwidth_package(params)
    CommonUtil.log("delete_common_bandwidth_package", cbwp_repsonse_json)

    # 删除natgw
    nat_gateway_json = nat_gateway.delete_nat_gateway(params)
    CommonUtil.log("delete_nat_gateway", nat_gateway_json)

    # 释放EIP
    eip_response_json = eip.release_eip_address(params)
    CommonUtil.log("release_eip_address", eip_response_json)

    # 删除vswitch
    params['vswitch_id'] = vswitch_json['VSwitchId']
    vswitch_json = vswitch.delete_vswitch(params)
    CommonUtil.log("delete_vswitch", vswitch_json)

    # 删除vpc
    vpc_json = vpc.delete_vpc(params)
    CommonUtil.log("delete_vpc", vpc_json)


if __name__ == "__main__":
    sys.exit(main())