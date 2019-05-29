#encoding=utf-8
from aliyunsdkvpc.request.v20160428 import CreateCommonBandwidthPackageRequest
from aliyunsdkvpc.request.v20160428 import AddCommonBandwidthPackageIpRequest
from aliyunsdkvpc.request.v20160428 import DescribeCommonBandwidthPackagesRequest
from aliyunsdkvpc.request.v20160428 import RemoveCommonBandwidthPackageIpRequest
from aliyunsdkvpc.request.v20160428 import DeleteCommonBandwidthPackageRequest
from sdk_lib.sdk_eip import *

class CommonBandwidthPackage(object):
    def __init__(self, client):
        self.client = client

    def create_common_bandwidth_package(self, params):
        """
        create_common_bandwidth_package: 创建共享带宽
        官网API参考: https://help.aliyun.com/document_detail/55930.html
        """
        try:
            request = CreateCommonBandwidthPackageRequest.CreateCommonBandwidthPackageRequest()
            # 共享带宽的带宽峰值，单位为Mbps
            request.set_Bandwidth(params['bandwidth'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            if CheckStatus.check_status(TIME_DEFAULT_OUT, DEFAULT_TIME,
                                        self.describe_cbwp_status,
                                        AVAILABLE, response_json["BandwidthPackageId"]):
                return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def add_common_bandwidth_packageIp(self, params):
        """
        add_common_bandwidth_packageIp: 添加EIP到共享带宽中
        官网API参考: https://help.aliyun.com/document_detail/55989.html
        """
        try:
            request = AddCommonBandwidthPackageIpRequest.AddCommonBandwidthPackageIpRequest()
            # EIP实例的ID
            request.set_IpInstanceId(params['ip_instance_id'])
            # 共享带宽的ID
            request.set_BandwidthPackageId(params['bandwidth_package_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_cbwp(self, cbwp_id):
        """
        describe_cbwp: 查询共享带宽实例信息
        官网API参考: https://help.aliyun.com/document_detail/55997.html
        """
        try:
            request = DescribeCommonBandwidthPackagesRequest.DescribeCommonBandwidthPackagesRequest()
            # 共享带宽实例的ID
            request.set_BandwidthPackageId(cbwp_id)
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)

    def describe_cbwp_status(self, cbwp_id):
        """
        describe_cbwp_status: 查询共享带宽实例状态
        官网API参考: https://help.aliyun.com/document_detail/55997.html
        """
        # 共享带宽实例的ID
        response = self.describe_cbwp(cbwp_id)
        return response["CommonBandwidthPackages"]["CommonBandwidthPackage"][0]["Status"]


    def remove_common_bandwidth_packageIp(self, params):
        """
        remove_common_bandwidth_packageIp: 移除共享带宽中的EIP
        官网API参考: https://help.aliyun.com/document_detail/55995.html
        """
        try:
            request = RemoveCommonBandwidthPackageIpRequest.RemoveCommonBandwidthPackageIpRequest()
            # EIP实例的ID
            request.set_IpInstanceId(params['ip_instance_id'])
            # 共享带宽实例的ID
            request.set_BandwidthPackageId(params['bandwidth_package_id'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)


    def delete_common_bandwidth_package(self, params):
        """
        delete_common_bandwidth_package: 删除共享带宽包
        官网API参考: https://help.aliyun.com/document_detail/56000.html
        """
        try:
            request = DeleteCommonBandwidthPackageRequest.DeleteCommonBandwidthPackageRequest()
            # 共享带宽实例的ID
            request.set_BandwidthPackageId(params['bandwidth_package_id'])
            # 是否强制删除共享带宽实例
            request.set_Force(params['force'])
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            ExceptionHandler.server_exception(e)
        except ClientException as e:
            ExceptionHandler.client_exception(e)