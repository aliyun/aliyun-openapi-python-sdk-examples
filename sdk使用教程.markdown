
# 阿里云python sdk使用


## 可以帮到您什么

* 快速掌握阿里云负载均衡Slb和Vpc产品SDK的使用方式
* 场景化的学习和使用阿里云产品SDK，参考文档：[slb官网文档](https://help.aliyun.com/product/27537.html) 以及 [vpc官网文档](https://help.aliyun.com/product/27706.html)

## 您需要准备什么

*  请确保您有AccessKey ID和AccessKey Secret，[点此查看确认ak、sk](https://usercenter.console.aliyun.com/#/manage/ak)
* 请确保您的账户金额不少于100元(人民币)
* python版本 Python 2.7
* 下载[github](https://github.com/aliyun/aliyun-openapi-python-sdk-examples)仓库代码

```
git clone https://github.com/aliyun/aliyun-openapi-python-sdk-examples
```

* [从阿里云官网下载](https://github.com/aliyun/aliyun-openapi-python-sdk-examples)

## sdk安装与配置


* 命令行sdk核心库安装指令：`pip install aliyun-python-sdk-core`
* 命令行slb sdk安装指令：`pip install aliyun-python-sdk-slb`
* 命令行vpc sdk安装指令：`pip install aliyun-python-sdk-vpc`
* 命令行云监控 sdk安装指令：`pip install aliyun-python-sdk-cms`
* [阿里云官网python sdk下载地址](https://developer.aliyun.com/tools/sdk?spm=5176.11122631.962077.5.361e38015KUJdL#/python)
* [配置slb常见问题](https://help.aliyun.com/document_detail/29863.html)


## examples环境初始化


```
执行 python setup.py install 命令添加路径配置
```

* client参数配置

```
from aliyunsdkcore.client import AcsClient

client = AcsClient(
    # 用户访问秘钥对中的 AccessKeyId。
    'ABCDEFG',
    # 用户访问秘钥对中的 AccessKeySecret。
    'HIGKLMN',
    # 使用sdk的regionId。
    'cn-hangzhou'
)
```

## 使用限制

* 支持python版本 Python 2.7
* [SLB使用限制文档](https://help.aliyun.com/document_detail/32459.html)
* [EIP使用限制文档](https://help.aliyun.com/document_detail/54479.html)
* [VPC使用限制文档](https://help.aliyun.com/document_detail/27750.html)
* [NAT网关使用限制文档](https://help.aliyun.com/document_detail/32382.html)

## sdk examples目录结构

* `sdk_examples`
  - `examples` 场景示例存于examples目录下
  - `sdk_lib` 接口封装成的sdk_lib
* `sdk使用教程`

## sdk examples场景介绍

* SLB
  - `slb_quick_start.py` 创建一个按量付费的SLB实例并查看实例的带宽、规格等信息
  - `slb_create_tcp_listener.py` 创建TCP监听，添加删除后端服务器
  - `slb_monitor.py` 监控实例的带宽、连接数、QPS等指标，并配置告警
  - `upload_server_certificate` 批量更新HTTPS证书
  - `configration_clone` 实例配置克隆
  
## 开源 LICENSE

* Apache License 2.0

