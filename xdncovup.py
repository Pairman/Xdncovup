'''
# 西安电子科技大学核酸检测情况自动上报工具

# 作者

[Pairman](https://github.com/Pairman)

# 免责信息

本程序仅供学习交流使用，使用本程序造成的任何后果由用户自行负责。

# 依赖

```Python>=3``` , ```requests```

# 用法

```
用法：
    python3 xdncovup.py [参数]
参数：
    -h,--help                   输出帮助信息
    -u,--username <学号>        指定学号
    -p,--password <密码>        指定密码
    -l,--location <上报地址>    指定上报地址（格式：某国某省某市某县/区）
    -d,--debug                  进入调试模式
```

# 致谢

[使用Github Aciton自动填写疫情通](https://cnblogs.com/soowin/p/13461451.html)

[西安电子科技大学疫情通、晨午晚检自动上报工具](https://github.com/jiang-du/Auto-dailyup)

[西安电子科技大学(包含广州研究院)晨午晚检自动上报工具](https://github.com/HANYIIK/Auto-dailyup)

[西安电子科技大学晨午晚检自动上报工具](https://github.com/cunzao/ncov)

# 开源协议

GNU General Public License v3.0 (gpl-3.0)
'''

from datetime import datetime
from getopt import getopt
from random import randint
from requests import Session
from sys import argv
from time import sleep

opts=getopt(argv[1:],"hu:p:l:d",["help","username=","password=","location=","debug"])[0]

USERNAME,PASSWORD,LOCATION,DEBUG="","","中国陕西省西安市长安区",False

helpMsg="""Xdncovup - 西安电子科技大学核酸检测情况自动上报工具 1.4 (2022 Oct 23, Pairman)
本程序仅供学习交流使用，使用本程序造成的任何后果由用户自行负责。
用法：
    python3 %s [参数]
参数：
    -h,--help                   输出帮助信息
    -u,--username <学号>        指定学号
    -p,--password <密码>        指定密码
    -l,--location <上报地址>    指定上报地址（格式：某国某省某市某县/区，默认：中国陕西省西安市长安区）
    -d,--debug                  进入调试模式
"""%(argv[0])

if len(argv)==1:
    print(helpMsg)
    exit()

for opt,arg in opts:
    if opt in ("-h","--help"):
        print(helpMsg)
        exit()
    if opt in ("-u","--username"):
        USERNAME=arg
    if opt in ("-p","--password"):
        PASSWORD=arg
    if opt in ("-l","--location"):
        LOCATION=arg
    if opt in ("-d","--debug"):
        DEBUG=1

print("本程序仅供学习交流使用，使用本程序造成的任何后果由用户自行负责。")

if USERNAME=="":
    print("请指定学号！")
    exit()
if PASSWORD=="":
    print("请指定密码！")
    exit()

# 上报信息表
currentUploadMsg={
    "value[location_563_1]":LOCATION, # 地址
    "value[id]":"", # ID
    "value[date_563_2]":"", # 日期
    "formid":"563" # 表单ID
}

# 默认上报时间
upHour,upMinute=8,30

# 登录
conn=Session()
logined=False
for i in range(3):
    result=None
    try:
        result=conn.post(url="https://xxcapp.xidian.edu.cn/uc/wap/login/check",data={"username":USERNAME,"password":PASSWORD},verify=not DEBUG)
        if result.json()['e']==0:
            logined=True
            print("登录成功")
            break
        print("登录失败：",result.json()['m'])
    except:
        print("登录失败：异常")
    sleep(60)
if not logined:
    print("登录失败，正在退出")
    exit()

# 连续三次尝试上报核酸检测情况
def ncovUp():
    result=None
    for i in range(3):
        try:
            result=conn.post(url="https://xxcapp.xidian.edu.cn/forms/wap/default/get-info?formid=563",verify=not DEBUG)
            currentUploadMsg["value[id]"]=result.json()['d']['value']['id']
            currentUploadMsg["value[date_563_2]"]=str(datetime.now())[0:10]
            result=conn.post(url="https://xxcapp.xidian.edu.cn/forms/wap/default/save",data=currentUploadMsg,verify=not DEBUG)
            if result.json()['e']==0:
                print("上报成功")
                return 1
            elif result.json()['m']=="每日仅能提交一次":
                print("已上报过")
                return 2
            print("填报失败")
        except:
            pass
        sleep(60)
    print("连续三次填报失败")
    return 0

# 运行后立即尝试上报
ncovUp()

while True:
    currentTime=datetime.now()
    currentHour,currentMinute=int(str(currentTime)[11:13]),int(str(currentTime)[14:16])
    # 到上报时间时尝试上报
    timeDiff=3600*upHour+60*upMinute-3600*currentHour-60*currentMinute
    if timeDiff==0:
        print("今天是%s年%s月%s日"%(str(currentTime)[0:4],str(currentTime)[5:7],str(currentTime)[8:10]))
        ncovUp()
    # 其他时刻暂停上报
    elif timeDiff>300:
        timeDiff-=300
        sleep(86400+timeDiff)
    elif timeDiff<0:
        upMinute=randint(10,50)
        print("更新核酸检测情况上报时间成功！下一天上报的时间为:%02d时%02d分"%(upHour,upMinute))
        timeDiff=86100+3600*upHour+60*upMinute-3600*currentHour-60*currentMinute
        sleep(timeDiff)
    else:
        sleep(50)
