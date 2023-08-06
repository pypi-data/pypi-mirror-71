###  py-micro 已改名为micro-py

micro-py是一款python的grpc框架，用于与 [go-micro](https://github.com/micro/go-micro) 使用的工具，支持gRPC，go-micro 服务调用



### 功能

- 支持服务注册（目前只支持consul）
- 与go-micro无缝连接，并同时支持gPRC调用







### 入门

创建服务：

```python
server = py_micro.Service({
        "server_name": "go.micro.srv",# 服务名
        "server_port": 64436,#监听端口（不填默认随机）
        "registry": "consul",
        "registry_address": "127.0.0.1:8500",
},
py_micro.Flag(
        name="gp",
        default="cc",
) # 环境变量值

)
        
```



注册服务

```
user_srv_pb2_grpc.add_UserServicer_to_server(UserDemo(), server)
```



启动

```
 server.run()

```







### 案例



./examples/python 下





