'''
# Author

[Pairman](https://github.com/Pairman)

# Disclaimer

本程序仅供学习交流使用，使用本程序造成的任何后果由用户自行负责。

# Dependencies

```Python>=3``` , ```requests```

# Usage

将本程序( ```.py``` )下载到本地，在用户配置修改区域填入自己的学号、密码及上报地址，保持运行本程序，本程序将自动在相应时段上报核酸检测情况。

# Credits

[使用Github Aciton自动填写疫情通](https://cnblogs.com/soowin/p/13461451.html)

[西安电子科技大学疫情通、晨午晚检自动上报工具](https://github.com/jiang-du/Auto-dailyup)

[西安电子科技大学(包含广州研究院)晨午晚检自动上报工具](https://github.com/HANYIIK/Auto-dailyup)

[西安电子科技大学晨午晚检自动上报工具](https://github.com/cunzao/ncov)

# Lisense

GNU General Public License v3.0 (gpl-3.0)

'''

# ------------------------------------------------ #

# 用户配置修改区域

# 登录学号和密码，在引号内修改
USERNAME=""
PASSWORD=""

# 上报地址，如某国某省某市某县/区，在引号内修改
LOCATION=""

# 调试用，不懂勿动
NOTDEBUG=True

# ------------------------------------------------ #

from asyncio.windows_events import NULL
import datetime
import random
import requests
import time

# 上报信息表
currentUploadMsg={
    "value[location_563_1]":LOCATION, # 地址
    "value[id]":"", # ID
    "value[date_563_2]":"", # 日期
    "formid":"563" # 表单ID
}

# 默认上报时间
upHour,upMinute=8,30

print("核酸检测情况自动上报")

# 登录
conn=requests.Session()
logined=0
for i in range(3):
    result=NULL
    try :
        result=conn.post(url="https://xxcapp.xidian.edu.cn/uc/wap/login/check",data={"username":USERNAME,"password":PASSWORD},verify=NOTDEBUG)
        if result.json()['e']==0:
            logined=1
            print("登录成功")
            break
        print("登录失败：",result.json()['m'])
    except:
        print("登录失败：异常")
if not logined:
    print("登录失败，正在退出")
    exit()

# 连续三次尝试上报核酸检测情况
def ncovUp():
    result=NULL
    for i in range(3):
        try:
            result=conn.post(url="https://xxcapp.xidian.edu.cn/forms/wap/default/get-info?formid=563",verify=NOTDEBUG)
            currentUploadMsg["value[id]"]=result.json()['d']['value']['id']
            result=conn.post(url="https://xxcapp.xidian.edu.cn/forms/wap/default/save",data=currentUploadMsg,verify=NOTDEBUG)
            if result.json()['e']==0:
                print("上报成功")
                return 1
            elif result.json()['m']=="每日仅能提交一次":
                print("已上报过")
                return 2
            print("填报失败")
        except:
            pass
    print("连续三次填报失败")
    return 0

# 运行后立即尝试上报
ncovUp()

while True:
    currentTime=datetime.datetime.now()
    currentHour,currentMinute=int(str(currentTime)[11:13]),int(str(currentTime)[14:16])
    # 到上报时间时尝试上报
    if currentHour==upHour and currentMinute==upMinute:
        currentUploadMsg["value[date_563_2]"]=str(datetime.datetime.now())[0:10]
        ncovUp()
    # 其他时刻暂停上报
    elif currentHour<upHour or (currentHour==upHour and currentMinute<upMinute-10):
        time.sleep(29340-3600*currentHour-60*currentMinute)
    elif currentHour>upHour or (currentHour==upHour and currentMinute>upMinute):
        upMinute=random.randint(10,50)
        print("更新核酸检测情况上报时间成功！下一天上报的时间为:%02d时%02d分"%(upHour,upMinute))
        print("程序进入休眠")
        # halt till 8:09 next day
        time.sleep(86100+3600*upHour-3600*currentHour+60*upMinute-60*currentMinute)
    else:
        time.sleep(60)
