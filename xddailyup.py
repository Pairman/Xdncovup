'''
Author:
    Pairman (https://github.com/Pairman )
Disclaimer:
    使用本程序即默认同意使用者承诺未感染新冠肺炎，
    使用本程序造成的任何后果由用户自行负责。
Dependencies:
    Python >= 3
    requests
Usage:
    若未安装 python ，请安装 python 3 及以上的版本。
    若未安装 requests 库，请安装。
    将本程序下载到本地
    在 USERNAME 、 PASSWORD 处填入自己的学号和密码。
    在 currentUploadMsg 处将填报信息改为信息表中对应的自己的信息，默认南校区。
    保持运行本程序，本程序将自动在相应时段填报晨午晚检。
Credits:
    Qmsg酱（https://qmsg.zendee.cn/ ）
    使用Github Aciton自动填写疫情通 (hyyps://cnblogs.com/soowin/p/13461451.html )
    西安电子科技大学疫情通、晨午晚检自动填报工具 (https://github.com/jiang-du/Auto-dailyup )
    西安电子科技大学(包含广州研究院)晨午晚检自动填报工具 (https://github.com/HANYIIK/Auto-dailyup )
    西安电子科技大学晨午晚检自动填报工具 (https://github.com/cunzao/ncov )
Lisense:
    GNU General Public License v3.0 (gpl-3.0)
'''

# ------------------------------------------------ #

# 用户修改配置区域

# 登录学号和密码。修改以登录自己的账户
USERNAME = "7h1515y0uru53rn4m3"
PASSWORD = "7h1515y0ur9455w0r6"

# 通过 Qmsg 接口将填报状态推送至 QQ ，此功能默认关闭，填入自己的 QmsgKEY 并设为 True 以启用 
Qmsg = False
QmsgKEY = "7h1515y0ur70k3n"

# ------------------------------------------------ #

import datetime
import json
import random
import requests
import time

# 填报信息表
NORTH_UPLOAD_MSG = {
    "sfzx": "1",  # 是否在校(0->否, 1->是)
    "tw": "1",  # 体温 (36℃->0, 36℃到36.5℃->1, 36.5℃到36.9℃->2, 36.9℃到37℃.3->3, 37.3℃到38℃->4, 38℃到38.5℃->5,
    # 38.5℃到39℃->6, 39℃到40℃->7, 40℃以上->8)
    "sfcyglq": "0",  # 是否处于隔离期? (0->否, 1->是)
    "sfyzz": "0",  # 是否出现乏力、干咳、呼吸困难等症状？ (0->否, 1->是)
    "qtqk": "",  # 其他情况 (文本)
    "askforleave": "0",  # 是否请假外出? (0->否, 1->是)
    "geo_api_info": "{\"type\":\"complete\",\"info\":\"SUCCESS\",\"status\":1,\"VDa\":\"jsonp_324977_\","
                    "\"position\":{\"Q\":34.23254,\"R\":108.91516000000001,\"lng\":108.91802,\"lat\":34.23231},"
                    "\"message\":\"Get ipLocation success.Get address success.\",\"location_type\":\"ip\","
                    "\"accuracy\":null,\"isConverted\":true,\"addressComponent\":{\"citycode\":\"029\","
                    "\"adcode\":\"610113\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\","
                    "\"building\":\"\",\"buildingType\":\"\",\"street\":\"白沙路\",\"streetNumber\":\"238号\","
                    "\"country\":\"中国\",\"province\":\"陕西省\",\"city\":\"西安市\",\"district\":\"雁塔区\","
                    "\"township\":\"电子城街道\"},\"formattedAddress\":\"陕西省西安市雁塔区电子城街道西安电子科技大学北校区\",\"roads\":[],"
                    "\"crosses\":[],\"pois\":[]}",
    "area": "陕西省 西安市 雁塔区",  # 地区
    "city": "西安市",  # 城市
    "province": "陕西省",  # 省份
    "address": "陕西省西安市雁塔区电子城街道西安电子科技大学北校区"  # 实际地址
}

# 0 - 南校区
SOUTH_UPLOAD_MSG = {
    "sfzx": "1",  # 是否在校(0->否, 1->是)
    "tw": "1",
    # 体温 (36℃->0, 36℃到36.5℃->1, 36.5℃到36.9℃->2, 36.9℃到37℃.3->3, 37.3℃到38℃->4, 38℃到38.5℃->5, 38.5℃到39℃->6, 39℃到40℃->7,
    # 40℃以上->8)
    "sfcyglq": "0",  # 是否处于隔离期? (0->否, 1->是)
    "sfyzz": "0",  # 是否出现乏力、干咳、呼吸困难等症状？ (0->否, 1->是)
    "qtqk": "",  # 其他情况 (文本)
    "askforleave": "0",  # 是否请假外出? (0->否, 1->是)
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":34.121994628907,\"R\":108.83715983073,"
                    "\"lng\":108.83716,\"lat\":34.121995},\"location_type\":\"html5\",\"message\":\"Get ipLocation "
                    "failed.Get geolocation success.Convert Success.Get address success.\",\"accuracy\":65,"
                    "\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"029\","
                    "\"adcode\":\"610116\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\","
                    "\"building\":\"\",\"buildingType\":\"\",\"street\":\"雷甘路\",\"streetNumber\":\"264号\","
                    "\"country\":\"中国\",\"province\":\"陕西省\",\"city\":\"西安市\",\"district\":\"长安区\","
                    "\"township\":\"兴隆街道\"},\"formattedAddress\":\"陕西省西安市长安区兴隆街道西安电子科技大学长安校区办公辅楼\",\"roads\":[],"
                    "\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "陕西省 西安市 长安区",  # 地区
    "city": "西安市",  # 城市
    "province": "陕西省",  # 省份
    "address": "陕西省西安市长安区兴隆街道西安电子科技大学长安校区行政辅楼",  # 实际地址
}

# 2 - 广州研究院 (测试)
GZ_UPLOAD_MSG = {
    "sfzx": "1",  # 是否在校(0->否, 1->是)
    "tw": "1",
    # 体温 (36℃->0, 36℃到36.5℃->1, 36.5℃到36.9℃->2, 36.9℃到37℃.3->3, 37.3℃到38℃->4, 38℃到38.5℃->5, 38.5℃到39℃->6, 39℃到40℃->7,
    # 40℃以上->8)
    "sfcyglq": "0",  # 是否处于隔离期? (0->否, 1->是)
    "sfyzz": "0",  # 是否出现乏力、干咳、呼吸困难等症状？ (0->否, 1->是)
    "qtqk": "",  # 其他情况 (文本)
    "askforleave": "0",  # 是否请假外出? (0->否, 1->是)
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":23.327658,\"R\":113.54548,"
                    "\"lng\":113.54548,\"lat\":23.327658},\"location_type\":\"html5\",\"message\":\"Get ipLocation "
                    "failed.Get geolocation success.Convert Success.Get address success.\",\"accuracy\":65,"
                    "\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"020\","
                    "\"adcode\":\"510555\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\","
                    "\"building\":\"\",\"buildingType\":\"\",\"street\":\"九龙大道\",\"streetNumber\":\"海丝知识中心\","
                    "\"country\":\"中国\",\"province\":\"广东省\",\"city\":\"广州市\",\"district\":\"黄埔区\","
                    "\"township\":\"九龙街道\"},\"formattedAddress\":\"广东省广州市黄埔区九龙大道海丝知识中心\",\"roads\":[],"
                    "\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "广东省 广州市 黄埔区",  # 地区
    "city": "广州市",  # 城市
    "province": "广东省",  # 省份
    "address": "广东省广州市黄埔区九龙大道海丝知识中心",  # 实际地址
}

# 3 - 杭州研究院 (预留)
HZ_UPLOAD_MSG = {
    "sfzx": "1",  # 是否在校(0->否, 1->是)
    "tw": "1",
    # 体温 (36℃->0, 36℃到36.5℃->1, 36.5℃到36.9℃->2, 36.9℃到37℃.3->3, 37.3℃到38℃->4, 38℃到38.5℃->5, 38.5℃到39℃->6, 39℃到40℃->7,
    # 40℃以上->8)
    "sfcyglq": "0",  # 是否处于隔离期? (0->否, 1->是)
    "sfyzz": "0",  # 是否出现乏力、干咳、呼吸困难等症状？ (0->否, 1->是)
    "qtqk": "",  # 其他情况 (文本)
    "askforleave": "0",  # 是否请假外出? (0->否, 1->是)
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":30.261994621906,\"R\":120.19715981072,"
                    "\"lng\":120.19715,\"lat\":30.26199},\"location_type\":\"html5\",\"message\":\"Get ipLocation "
                    "failed.Get geolocation success.Convert Success.Get address success.\",\"accuracy\":65,"
                    "\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"0571\","
                    "\"adcode\":\"310000\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\","
                    "\"building\":\"\",\"buildingType\":\"\",\"street\":\"龙井路\",\"streetNumber\":\"1号\","
                    "\"country\":\"中国\",\"province\":\"浙江省\",\"city\":\"杭州市\",\"district\":\"西湖区\","
                    "\"township\":\"西湖街道\"},\"formattedAddress\":\"浙江省杭州市西湖区西湖街道龙井路1号杭州西湖风景名胜区\",\"roads\":[],"
                    "\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "浙江省 杭州市 西湖区",  # 地区
    "city": "杭州市",  # 城市
    "province": "浙江省",  # 省份
    "address": "浙江省杭州市西湖区西湖街道龙井路1号杭州西湖风景名胜区",  # 实际地址
}

# 4 - 备用(出差)
BAK_UPLOAD_MSG = {
    "sfzx": "1",  # 是否在校(0->否, 1->是)
    "tw": "1",
    # 体温 (36℃->0, 36℃到36.5℃->1, 36.5℃到36.9℃->2, 36.9℃到37℃.3->3, 37.3℃到38℃->4, 38℃到38.5℃->5, 38.5℃到39℃->6, 39℃到40℃->7,
    # 40℃以上->8)
    "sfcyglq": "0",  # 是否处于隔离期? (0->否, 1->是)
    "sfyzz": "0",  # 是否出现乏力、干咳、呼吸困难等症状？ (0->否, 1->是)
    "qtqk": "",  # 其他情况 (文本)
    "askforleave": "0",  # 是否请假外出? (0->否, 1->是)
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":31.142927,\"R\":121.81332,"
                    "\"lng\":121.81332,\"lat\":31.142927},\"location_type\":\"html5\",\"message\":\"Get ipLocation "
                    "failed.Get geolocation success.Convert Success.Get address success.\",\"accuracy\":65,"
                    "\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"021\","
                    "\"adcode\":\"200120\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\","
                    "\"building\":\"\",\"buildingType\":\"\",\"street\":\"迎宾大道\",\"streetNumber\":\"6000号\","
                    "\"country\":\"中国\",\"province\":\"上海市\",\"city\":\"上海市\",\"district\":\"浦东新区\","
                    "\"township\":\"祝桥镇\"},\"formattedAddress\":\"上海市浦东新区祝桥镇迎宾大道6000号浦东国际机场T2航站楼\",\"roads\":[],"
                    "\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "上海市 浦东新区",  # 地区
    "city": "上海市",  # 城市
    "province": "上海市",  # 省份
    "address": "上海市浦东新区祝桥镇迎宾大道6000号浦东国际机场T2航站楼",  # 实际地址
}

#填报哪个信息？默认南校区，修改以切换信息
currentUploadMsg = SOUTH_UPLOAD_MSG

# 定义程序上报的时间，初始值为 7:15, 12:05, 18:10
time_lib = [7, 15, 12, 5, 18, 10]

# 获取当前时间
def getCurrentTime():
    currentTime = datetime.datetime.now()
    hour = int(str(currentTime)[11:13])
    minute = int(str(currentTime)[14:16])
    second = int(str(currentTime)[17:19])
    return hour, minute, second

# 随机更新下一天填报时间
def updateTimeLib(time_lib):

    assert len(time_lib) == 6
    new_time = time_lib
    new_time[1] = random.randint(2,59)
    new_time[3] = random.randint(2,59)
    new_time[5] = random.randint(2,59)
    print("更新晨午晚检上报时间成功！下一天自动上报的时间为:")
    print("晨检%02d时%02d分，午检%02d时%02d分，晚检%02d时%02d分" % tuple(new_time))
    return new_time

# 判断当前是否需要上报
def checkTime(time_lib):

    currentHour, currentMinute, currentSecond = getCurrentTime()
    if currentHour == time_lib[0] and currentMinute == time_lib[1]:
        # 晨检
        currentState = 1
    elif currentHour == time_lib[2] and currentMinute == time_lib[3]:
        # 午检
        currentState = 2
    elif currentHour == time_lib[4] and currentMinute == time_lib[5]:
        # 晚检
        currentState = 3
    elif currentHour == 23 and currentMinute == 55:
        # 夜间模式
        currentState = 4
    elif not currentMinute:
        # 整点时刻
        currentState = 5
    else:
        currentState = 0
    if currentState:
        print("当前系统时间  %02d:%02d:%02d" % (currentHour, currentMinute, currentSecond))
    return currentState

# 登录
conn = requests.Session()
result = conn.post(url = "https://xxcapp.xidian.edu.cn/uc/wap/login/check", data = {'username': USERNAME, 'password': PASSWORD})
loginTries = 0
while True:
    if loginTries == 5:
        msg = "登录失败，正在退出"
    if result.status_code == 200:
        msg = "登录成功"
        break
    elif loginTries < 5:
        msg = "错误信息: {}".format(result.status_code)
print(msg)
if(msg == "登录失败，正在退出"):
    exit()

# 填报晨午晚检
def dailyUp():
    result = conn.post(url = "https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save", data = currentUploadMsg)
    if result.json()['e'] == 0:
        print("填报成功")
        success = 1
    else:
        state = result.json()['m']
        if state == "您已上报过":
            print("已填报过")
            success = 2
        else:
            print("填报错误")
            success = 0
    return success

# Qmsg 消息推送
def QmsgPush(currentState,success):
    if Qmsg == False:
        return 0
    QmsgURL = "https://qmsg.zendee.cn/send/{}".format(QmsgKEY)
    if currentState == 1:
        msgState = "晨检"
    elif currentState == 2:
        msgState = "午检"
    elif currentState == 3:
        msgState = "晚检"
    else:
        msgState = "其他"
    if success == 1:
        msgSuccess = "填报成功"
    elif success == 2:
        msgSuccess = "已填报过"
    else:
        msgSuccess = "填报失败"
    requests.post(QmsgURL, data = {'msg': '[自动填报]\n时间: {}\n类别: {}\n状态: {}'.format(datetime.datetime.now(),msgState,msgSuccess)})

# 登录后立即上报一次
success = dailyUp()
QmsgPush(checkTime(time_lib),success)

while True:
    currentState = checkTime(time_lib)
    # 晨、午、晚填报，填报失败则重试两次
    if currentState in (1, 2, 3):
        success = dailyUp()
        QmsgPush(currentState,success)
        if success == 0:
            time.sleep(90)
            success = dailyUp()
            QmsgPush(currentState,success)
            if success == 0:
                time.sleep(180)
                success = dailyUp()
                QmsgPush(currentState,success)
                if success == 0:
                    print("连续三次填报失败")
    # 上报结束后冷却时间
        time.sleep(180)
    elif currentState == 4:
        # 每天23点55分，更新下一天上报的随机时刻
        time_lib = updateTimeLib(time_lib)
        print("程序夜间进入休眠")
        # 夜间暂停6小时
        time.sleep(6*60*60)
        print("早上好")
    elif currentState == 5:
        # 整点报时
        time.sleep(60)
    else:
        time.sleep(30)
