#encoding=utf-8
import json

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateVSwitchRequest
from aliyunsdkvpc.request.v20160428 import DeleteVSwitchRequest
from aliyunsdkvpc.request.v20160428 import DescribeVSwitchAttributesRequest
from sdk_lib.exception import ExceptionHandler
from sdk_lib.check_status import CheckStatus
from sdk_lib.consts import *

class VSwitch(object):

    def __init__(self, client):
        self.client = client

    def create_vswitch(self, params):
        """
        create_vswitch: 创建vpc实例
        官网API参考: https://help.aliyun.com/document_detail/35745.html
        """
        try:
            request = CreateVSwitchRequest.CreateVSwitchRequest()
            # 交换机所属区的ID，您可以通过调用DescribeZones接口获取地域ID
            request.set_ZoneId(params['zone_id'])
            # 交换机所属的VPC ID
            request.set_VpcId(params['vpc_id'])
            # 交换机的网段
            request.set_CidrBlock(params['cidr_block'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断VSwitch状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_vswitch_status,
                                        AVAILABLE, response_json['VSwitchId']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_vswitch_attribute(self, vswitch_id):
        """
        describe_vswitch_attribute: 查询指定地域已创建的vswitch的状态
        官网API参考: https://help.aliyun.com/document_detail/36010.html
        """
        try:
            request = DescribeVSwitchAttributesRequest.DescribeVSwitchAttributesRequest()
            request.set_VSwitchId(vswitch_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_vswitch_status(self, vswitch_id):
        """
        describe_vswitch_status: 查询指定地域已创建的vswitch的状态
        官网API参考: https://help.aliyun.com/document_detail/36010.html
        """
        response = self.describe_vswitch_attribute(vswitch_id)
        return response["Status"]

    def delete_vswitch(self, params):
        """
        delete_vswitch: 删除vswitch实例
        官网API参考: https://help.aliyun.com/document_detail/35746.html
        """
        try:
            request = DeleteVSwitchRequest.DeleteVSwitchRequest()
            # 要删除的交换机的ID
            request.set_VSwitchId(params['vswitch_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断VSwitch是否被删除成功
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME * 5,
                                        self.describe_vswitch_status,
                                        '', params['vswitch_id']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)
