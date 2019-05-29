#encoding=utf-8
import sys
import json
from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import AllocateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import AssociateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import DescribeEipAddressesRequest
from aliyunsdkvpc.request.v20160428 import UnassociateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import ModifyEipAddressAttributeRequest
from aliyunsdkvpc.request.v20160428 import ReleaseEipAddressRequest
from sdk_lib.exception import ExceptionHandler
from sdk_lib.check_status import CheckStatus
from sdk_lib.consts import *
from sdk_lib.common_util import CommonUtil

"""
创建EIP->绑定EIP到ECS->查询EIP->解绑EIP->查询EIP->释放EIP
"""
class Eip(object):
    def __init__(self, client):
        self.client = client

    def allocate_eip_address(self, params):
        """
        allocate_eip_address: 申请弹性公网IP（EIP)
        官网API参考: https://help.aliyun.com/document_detail/36016.html
        """
        try:
            request = AllocateEipAddressRequest.AllocateEipAddressRequest()
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_eip_status,
                                        AVAILABLE, response_json["AllocationId"]):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def associate_eip_address(self, params):
        """
        associate_eip_address: 将EIP绑定到同地域的云产品实例上
        官网API参考: https://help.aliyun.com/document_detail/36017.html
        """
        try:
            request = AssociateEipAddressRequest.AssociateEipAddressRequest()
            # EIP的ID
            request.set_AllocationId(params['allocation_id'])
            # 要绑定的云产品实例的类型
            request.set_InstanceType(params['instance_type'])
            # 要绑定的实例ID
            request.set_InstanceId(params['instance_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_eip_status,
                                        InUse, params['allocation_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_eip_address(self, allocation_id):
        """
        describe_eip_status: 查询指定地域已创建的EIP。
        官网API参考: https://help.aliyun.com/document_detail/36018.html
        """
        try:
            request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
            # EIP的ID
            request.set_AllocationId(allocation_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_eip_status(self, allocation_id):
        """
        describe_eip_status: 查询指定地域已创建的EIP的状态
        官网API参考: https://help.aliyun.com/document_detail/36018.html
        """
        # EIP的ID
        response = self.describe_eip_address(allocation_id)
        return response["EipAddresses"]["EipAddress"][0]["Status"]


    def unassociate_eip_address(self, params):
        """
        unassociate_eip_address: 将EIP从绑定的云资源上解绑。
        官网API参考: https://help.aliyun.com/document_detail/36021.html
        """
        try:
            request = UnassociateEipAddressRequest.UnassociateEipAddressRequest()
            # EIP的ID
            request.set_AllocationId(params['allocation_id'])
            # 要解绑的资源类型
            request.set_InstanceType(params['instance_type'])
            # 要解绑的云产品的实例ID
            request.set_InstanceId(params['instance_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_eip_status,
                                        AVAILABLE, params['allocation_id']):
                return response_json
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def modify_eip_address(self, params):
        """
        modify_eip_address: 修改指定EIP的名称、描述信息和带宽峰值
        官网API参考: https://help.aliyun.com/document_detail/36019.html
        """
        try:
            request = ModifyEipAddressAttributeRequest.ModifyEipAddressAttributeRequest()
            # 弹性公网IP的ID
            request.set_AllocationId(params['allocation_id'])
            # EIP的带宽峰值，单位为Mbps
            request.set_Bandwidth(params['bandwidth'])
            # EIP的名称
            request.set_Name(params['name'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def release_eip_address(self, params):
        """
        release_eip_address: 释放指定的EIP。
        官网API参考: https://help.aliyun.com/document_detail/36020.html
        """
        try:
            request = ReleaseEipAddressRequest.ReleaseEipAddressRequest()
            # 要释放的弹性公网IP的ID
            request.set_AllocationId(params['allocation_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)
def main():
    client = ACS_CLIENT
    eip = Eip(client)

    params = {}

    # 创建EIP
    eip_response_json = eip.allocate_eip_address(params)
    CommonUtil.log("allocate_eip_address", eip_response_json)

    # 绑定EIP到ECS
    params['allocation_id'] = eip_response_json["AllocationId"]
    params['instance_id'] = ECS_INSTANCE_ID
    params['instance_type'] = 'EcsInstance'
    eip_response_json = eip.associate_eip_address(params)
    CommonUtil.log("associate_eip_address", eip_response_json)

    # 查询EIP
    eip_response_json = eip.describe_eip_address(params['allocation_id'])
    CommonUtil.log("describe_eip_address", eip_response_json)

    # 解绑EIP
    eip_response_json = eip.unassociate_eip_address(params)
    CommonUtil.log("unassociate_eip_address", eip_response_json)

    # 查询EIP
    eip_response_json = eip.describe_eip_address(params['allocation_id'])
    CommonUtil.log("describe_eip_address", eip_response_json)

    # 释放EIP
    eip_response_json = eip.release_eip_address(params)
    CommonUtil.log("release_eip_address", eip_response_json)

if __name__ == '__main__':
    sys.exit(main())

