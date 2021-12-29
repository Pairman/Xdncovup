# Xddailyup

西电晨午晚检自动填报



## 免责声明

使用本程序即默认同意使用者承诺未感染新冠肺炎。使用本程序造成的任何后果由用户自行负责。



## 依赖

Python >= 3

requests



## 用法

若未安装 python ，请安装 python 3 及以上的版本。若未安装 requests 库，请安装。

将本程序下载到本地。

在 USERNAME 、PASSWORD 处填入自己的学号和密码。在 currentUploadMsg 处将填报信息改为信息表中对应的自己的信息，默认南校区。

若想程序在每次填报时将当次填报信息，即填报时间、填报类别（晨检/午检/晚检/其他）、填报状态（填报成功/已填报过/填报失败）推送到推送至 QQ ，请在 Qmsg 按手册注册，在本程序 QmsgKEY 处填入自己的 KEY ，并将 Qmsg 设为 True 开启推送功能。

保持运行本程序，本程序将自动在相应时段填报晨午晚检。



## 鸣谢

Qmsg酱（https://qmsg.zendee.cn/ ）

使用Github Aciton自动填写疫情通 (https://cnblogs.com/soowin/p/13461451.html )

西安电子科技大学疫情通、晨午晚检自动填报工具 (https://github.com/jiang-du/Auto-dailyup )

西安电子科技大学(包含广州研究院)晨午晚检自动填报工具 (https://github.com/HANYIIK/Auto-dailyup )

西安电子科技大学晨午晚检自动填报工具 (https://github.com/cunzao/ncov )



## 开源许可方式

GNU General Public License v3.0 (gpl-3.0)
