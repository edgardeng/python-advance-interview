# Cron

## 一、安装

### 1、ubuntu安装cron

```
安装：apt-get install cron
启动：service cron start
重启：service cron restart
停止：service cron stop
检查状态：service cron status
查询cron可用的命令：service cron
检查Cronta工具是否安装：crontab -l

```
### 2、centOS安装：
centOSs安装cron：（1）vixie-cron 软件包是 cron 的主程序；（2）crontabs 软件包是用来安装、卸装、或列举用来驱动 cron 守护进程的表格的程序。

yum install vixie-cron
yum install crontabs
 
配置：

service crond start     //启动服务
service crond stop      //关闭服务
service crond restart   //重启服务
service crond reload    //重新载入配置
service crond status    //查看crontab服务状态
 
在CentOS系统中加入开机自动启动:

chkconfig --level 345 crond on