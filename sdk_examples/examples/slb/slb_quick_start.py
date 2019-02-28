# encoding=utf-8
import sys
import json

# 调用AcsClient参数进行身份验证
from aliyunsdkcore.client import AcsClient

# 使用阿里云官方sdk的异常处理模块
from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException

# 调用创建SLB实例API
from aliyunsdkslb.request.v20140515 import CreateLoadBalancerRequest

# 调用删除SLB实例API
from aliyunsdkslb.request.v20140515 import DeleteLoadBalancerRequest

# 异常处理逻辑
from sdk_lib.exception import ExceptionHandler

# 命令行打印日志
from sdk_lib.common_util import CommonUtil

# 用户身份验证参数配置
ACS_CLIENT = AcsClient(
    'your-access-key-id',  # your-access-key-id
    'your-access-key-secret',  # your-access-key-secret
    'cn-zhangjiakou',  # your-region-id
)
'''
创建slb实例->删除slb实例
'''


def create_load_balancer(params):
    '''
    create_load_balancer：创建slb实例
    官网API参考链接：https://help.aliyun.com/document_detail/27577.html
    '''
    try:
        # 设置调用参数
        request = CreateLoadBalancerRequest.CreateLoadBalancerRequest()
        request.set_MasterZoneId(params["master_zone_id"])
        request.set_SlaveZoneId(params["slave_zone_id"])
        request.set_LoadBalancerName(params["load_balancer_name"])
        request.set_PayType(params["pay_balancer_type"])
        request.set_LoadBalancerSpec(params["load_balancer_spec"])
        request.set_Bandwidth(params["balancer_listener_bandwith"])
        # 发送调用请求并接收返回数据
        response = ACS_CLIENT.do_action_with_exception(request)
        response_json = json.loads(response)
        # 返回结果
        return response_json
    except ServerException as e:
        ExceptionHandler.server_exception(e)
    except ClientException as e:
        ExceptionHandler.client_exception(e)


def delete_load_balancer(load_balancer_id):
    '''
    delete_load_balancer：删除slb实例
    官网API参考链接：https://help.aliyun.com/document_detail/27579.html
    '''
    try:
        request = DeleteLoadBalancerRequest.DeleteLoadBalancerRequest()
        # 负载均衡实例的ID
        request.set_LoadBalancerId(load_balancer_id)
        response = ACS_CLIENT.do_action_with_exception(request)
        response_json = json.loads(response)
        return response_json
    except ServerException as e:
        ExceptionHandler.server_exception(e)
    except ClientException as e:
        ExceptionHandler.client_exception(e)


def main():
    # 设置创建SLB的实例参数值
    params = {}
    # 设置新建SLB实例的主可用区为cn-zhangjiakou-a
    params["master_zone_id"] = "cn-zhangjiakou-a"
    # 设置新建SLB实例的主可用区为cn-zhangjiakou-b
    params["slave_zone_id"] = "cn-zhangjiakou-b"
    # 设置新建SLB实例的名称为SLB1
    params["load_balancer_name"] = "SLB1"
    # 设置新建SLB实例的计费类型为按量计费
    params["pay_balancer_type"] = "PayOnDemand"
    # 设置新建SLB实例的规格为slb.s1.small
    params["load_balancer_spec"] = "slb.s1.small"
    # 监听的带宽峰值为6Mbps
    params["balancer_listener_bandwith"] = "1"

    # 创建slb实例
    # 获取create_load_balancer函数返回值，load_balancer_json为结果的json串
    load_balancer_json = create_load_balancer(params)
    # 打印 load_balancer_json结果，其中"create_load_balancer"是对json串起的名字
    CommonUtil.log("create_load_balancer", load_balancer_json)

    # 删除slb实例
    # 删除返回的LoadBalancerId对应的SLB实例
    load_balancer_json = delete_load_balancer(load_balancer_json["LoadBalancerId"])
    # 打印 load_balancer_json结果
    CommonUtil.log("delete_load_balancer", load_balancer_json)


if __name__ == "__main__":
    sys.exit(main())