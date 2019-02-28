#encoding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception import error_code, error_msg

SERVICE_ERROR_CODE = ["ServiceUnavailable", "InternalError"]
CLIENT_ERROR_CODE = [error_code.SDK_INVALID_REQUEST]

#client参数配置
ACS_CLIENT = AcsClient(
    'your-access-key-id',  # your-access-key-id
    'your-access-key-secret',  # your-access-key-secret
    'cn-zhangjiakou',  # your-region-id
)

#通用
TIME_DEFAULT_OUT = 15

DEFAULT_TIME = 1

TRY_TIME = 3


# 带宽
BANDWIDTH_50 = 50

BANDWIDTH_10 = 10

BANDWIDTH_NOT_LIMITED = -1

# 状态
AVAILABLE = "Available"

InUse = "InUse"

STATUS = "Status"


# EIP相关
EIP_NEW_NAME = "EIP_NEW_NAME"

PAY_BY_TRAFFIC = "PayByTraffic"

# ENI相关
PAY_ON_DEMAND = "PayOnDemand"

# 地域
REGION = "cn-hangzhou"

ZONE_ID = "cn-hangzhou-b"

