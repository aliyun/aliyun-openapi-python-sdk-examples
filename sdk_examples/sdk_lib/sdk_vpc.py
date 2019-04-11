#encoding=utf-8
import json

from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
from aliyunsdkvpc.request.v20160428 import CreateVpcRequest
from aliyunsdkvpc.request.v20160428 import DeleteVpcRequest
from aliyunsdkvpc.request.v20160428 import DescribeVpcAttributeRequest
from sdk_lib.exception import ExceptionHandler
from sdk_lib.check_status import CheckStatus
from sdk_lib.consts import *

class Vpc(object):
    def __init__(self, client):
        self.client = client

    def create_vpc(self):
        """
        create_vpc：创建vpc
        官网API参考链接: https://help.aliyun.com/document_detail/35737.html
        """
        try:
            request = CreateVpcRequest.CreateVpcRequest()
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # 判断Vpc状态是否可用
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_vpc_status,
                                        AVAILABLE, response_json['VpcId']):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def delete_vpc(self, params):
        """
        delete_vpc:删除vpc
        官网API参考链接: https://help.aliyun.com/document_detail/35738.html
        """
        try:
            request = DeleteVpcRequest.DeleteVpcRequest()
            # 要删除的VPC的ID
            request.set_VpcId(params['vpc_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_vpc_attribute(self, vpc_id):
        """
        describe_vpc_status: 查询指定地域已创建的vpc的状态
        官网API参考: https://help.aliyun.com/document_detail/94565.html
        """
        try:
            request = DescribeVpcAttributeRequest.DescribeVpcAttributeRequest()
            # 要查询的VPC ID
            request.set_VpcId(vpc_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_vpc_status(self, vpc_id):
        """
        describe_vpc_status: 查询指定地域已创建的vpc的状态
        官网API参考: https://help.aliyun.com/document_detail/94565.html
        """
        response = self.describe_vpc_attribute(vpc_id)
        return response["Status"]
