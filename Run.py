#ส่วนหัวรวมโมดูลและไลบรารี Library
from linepy import *
from datetime import datetime
from liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
import time, sys, os, akad, json, re, ast, pytz, requests
import threading
import random
import qrcode

#โค้ดส่วนนี้ใช้ล็อกอินบอท
appName = "DESKTOPMAC\t9.2.0\tMAC\t12.6"
line = LINE('ใส่อีเมล์', 'รหัสอีเมล์', appName=appName)
token = line.authToken
print(f"โทเค่น {token}") 

#ส่วนนี้คือกำหนดแอดมินที่สั่งบอทได้
creator = ['uc7deef31bd21ce96d4ec90b3b6856053']
lineMID = line.getProfile().mid
lineProfile = line.getProfile()
botshi = OEPoll(line)

def bcTemplate(gr, data): #เกี่ยวกับการส่งข้อความผ่านapi
    teambotmax1 = LiffChatContext(gr)
    teambotmax2 = LiffContext(chat=teambotmax1)
    teambotmax3 = LiffViewRequest("ใส่ลิฟไอดีของอันไหนก็ได้", teambotmax2)
    token = line.liff.issueLiffView(teambotmax3)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))

def shido15(to, text): #ข้อความ FLEX ไลน์
    true = True
    data = {
        "type": "flex",
        "altText": "คำสั่งของชิโด้ ʕ •ᴥ•ʔ",
        "contents": {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "size": "full",
                        "aspectRatio": "21:21",
                        "aspectMode": "cover",
                        "url": "https://img2.pic.in.th/pic/1709219692698-ezgif.com-gif-to-apng-converter.png",
                        "animated": true
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🐥SHIDO🐥",
                                "wrap": true,
                                "weight": "bold",
                                "size": "xl",
                                "color": "#FFFFFF",
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": text,
                                "color": "#66CCFF",
                                "weight": "bold",
                                "size": "md",  # สามารถปรับขนาดตามต้องการ
                                "align": "center",
                                "wrap": true  # ให้ wrap เป็น true เพื่อให้แสดงผลอย่างเต็มที่
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "button",
                                        "color": "#FF1493",
                                        "style": "primary",
                                        "action": {
                                            "type": "clipboard",
                                            "label": "คัดลอกข้อความ",
                                            "clipboardText": text,
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    "styles": {
                        "body": {
                            "backgroundColor": "#000000"
                        }
                    }
                }
            ]
        }
    }
    bcTemplate(to, data)                  
    time.sleep(1)

#ฟังก์ชั่นสำหรับรับค่าคำสั่งบอท
def DevBOTSHI(op):
    global msg
    try:
    	
        if op.type == 25 or op.type == 26: #op.type 25 คือตัวเองส่ง 26คือ คนอื่นส่งมา
            msg = op.message #คือรวมทุกอย่างที่ได้จากข้อมูลที่ไลน์ส่งมา
            to = msg.to #to คือห้องที่ส่ง
            sender = msg._from #sender คือไอดีที่ส่งมา
            msg_id = msg.id #msg_id คือไอดีข้อความ
            
            if msg.text is not None:
                text = msg.text.lower() #การรับข้อความtext
                
                if text == "บอท" and sender in creator: #ถ้าข้อความ=บอทและผู้สั่งคือแอดมิน
                   line.sendMessage(to, "ว่าไงสกีบีดี้!!") #ส่งข้อความไปห้องที่ถูกสั่งว่า สกีบีดี้

                if text.startswith("ค้น "): #ถ้าข้อความ=คำว่า ค้น และมีข้อความต่อหลังค้น
                	data = msg.text #ดึงข้อมูลข้อความนั้น
                	headers = {
				        'Content-Type': 'application/json',
                	} #ส่วนหัวสำหรับส่ง requests
                	params = {
				        'key': 'ใส่โทเค่นgenmini',
                	} #คีย์ API สำหรับส่ง requests
                	json_data = {
				        'contents': [
				            {
				                'parts': [
				                    {
				                        'text': data, #ข้อมูลที่ดึงมาข้างต้น
				                    },
				                ],
				            },
				        ],
                	} #ส่งข้อมูลแบบ json 
                	response = requests.post(
				        'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',
				        params=params,
				        headers=headers,
				        json=json_data,
                	) #ส่งโดยการ post
                	data = response.json() #รับค่าการตอบกลับจากapiที่ส่งก่อนหน้า
                	line.sendMessage(to, f"ตอบกลับ : " + data["candidates"][0]["content"]["parts"][0]["text"]) #ส่งข้อความไปที่ห้องแชท
				                                                                                 
                elif text.startswith("/ทำ\n") and sender in creator: #โค้ดแยกสำหรับสั่งข้อความที่ไปทำงานบนVPS
                    try:
                        code = msg.text.replace("/ทำ\n", "")
                        exec(code)
                    except Exception as error:
                        line.sendMessage(to, "เออเร่อ : {}".format(error))
               
        if op.type == 26: #รับค่าข้อความที่ผู้ใช้อื่นส่งมา
           msg = op.message  #ดึงข้อมูลทั้งหมดที่ถูกส่งมา
           if msg.contentType == 15: #ถ้าข้อความที่ส่งมาคือข้อมูล ตำแหน่งที่ตั้ง
              if hasattr(msg, 'location') and msg.location is not None: #ตรวจสอบว่ามีข้อมูล ตำแหน่งหรือไม่
                 #print(msg.location.address, msg.location.latitude, msg.location.longitude)
                 url = f'https://api.openweathermap.org/data/2.5/weather?lat={msg.location.latitude}&lon={msg.location.longitude}&appid=ใส่ไอดีตัวเอง&units=metric'
                 try:
                     temp = requests.get(url).json()['main']['temp'] #ดึงข้อมูลอุณภูมิจากurl
                     text = f"{msg.location.address}\nอุณหภูมิ: {temp}°C" #ตัวแปรสำหรับเก็บข้อมูล
                     shido15(to, text) #ส่งข้อมูลเป็นรูปแบบ Flex Message
                 except Exception as e:
                     line.sendMessage(to, "เกิดข้อผิดพลาด😵‍💫")
                                
    except Exception as e:
        print(e) 

def run(): #ฟังก์ชั้นลูปสำหรับทำงานบอทตลอดเวลาที่รัน
    while True:
        try:
            ops = botshi.singleTrace(count=50)
            if ops is not None:
                for op in ops:
                    DevBOTSHI(op)
                    botshi.setRevision(op.revision)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    run()
