## 项目介绍

项目名称 orderlines

使用flask celery协程自主开发的一套工作流框架，现在为未完成状态 目前已实现功能

- 流程串行，基本功能
- 流程并行（可选择使用协程io密集型和进程cpu密集型）
- 流程控制， 根据返回值和上个节点的返回值运行
- 任务超时，给定超时时间
- 定时任务
- 异常处理策略，重试，忽略，抛错
- 任务回调
- 停止任务，这里有问题就是不能停止正在运行的任务，因为python协程的问题

未实现功能

- rbac权限
- 使用k8s进行运行定时任务和异步任务
- docker 部署

### 启动celery worker

```angular2html
celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

### 启动celery beat

```angular2html
celery -A celery_worker.celery beat -l info --scheduler celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler
```

### 启动方式

- 启动flask flask_main.py
- 插入流程运行接口 http://127.0.0.1:5000/build/process POST 参数在 common_node.json
- 运行celery `celery -A celery_worker.celery worker --loglevel=info --pool=gevent`
- 发送接口`http://127.0.0.1:5000/order_lines_start` POST `{"process_id":"1001"}`
 

