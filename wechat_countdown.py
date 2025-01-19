import os
import requests
from datetime import datetime, timedelta

# 获取微信公众平台的配置
APPID = os.getenv('WECHAT_APPID')
APPSECRET = os.getenv('WECHAT_APPSECRET')
TEMPLATE_ID = os.getenv('WECHAT_TEMPLATE_ID')
TOUSER = os.getenv('WECHAT_TOUSER')

def get_access_token(appid, appsecret):
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'
    response = requests.get(url)
    return response.json().get('access_token')

def send_template_message(access_token, touser, template_id, data):
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    payload = {
        "touser": touser,
        "template_id": template_id,
        "data": data
    }
    response = requests.post(url, json=payload)
    return response.json()

def main():
    # 计算春节的倒计时
    today = datetime.now() + timedelta(hours=8)  # 转换为北京时间
    new_year = datetime(today.year, 1, 1)
    if today > new_year:
        new_year = datetime(today.year + 1, 1, 1)
    countdown_days = (new_year - today).days

    # 准备模板消息的数据
    data = {
        "first": {
            "value": "春节倒计时",
            "color": "#173177"
        },
        "keyword1": {
            "value": f"{countdown_days} 天",
            "color": "#173177"
        },
        "remark": {
            "value": "提前祝你新年快乐！时间不等人，且行且珍惜",
            "color": "#173177"
        }
    }

    # 获取 access token
    access_token = get_access_token(APPID, APPSECRET)
    if not access_token:
        print("Failed to get access token")
        return

    # 发送模板消息
    result = send_template_message(access_token, TOUSER, TEMPLATE_ID, data)
    print(result)

if __name__ == '__main__':
    main()
