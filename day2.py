#目标：选取一张帧图片让视觉模型识别
import base64
import os
from openai import OpenAI

#建立客户端
client = OpenAI(
    api_key=os.environ.get("OPENROUTER_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

#图片二进制转为JSON
test_path = r"D:\GUIagent\frames\frame_27.png"
with open(test_path,"rb")as f:
    raw_bytes = f.read()
b64_string = base64.b64encode(raw_bytes).decode("utf-8")

#调用api
response = client.chat.completions.create(
    model = "qwen/qwen2.5-vl-72b-instruct",
    messages=[
        {
            "role":"user",
            "content":[
                #第一部分：图片
                {
                    "type":"image_url",
                    "image_url":{
                        "url":f"data:image/png;base64,{b64_string}"
                    }
                },
                #第二部分：文字内容
                {
                    "type":"text",
                    "text":"你是一个看电影的帧图片的agent，根据你看到的这幅图描述一下电影场面，人物，台词。"
                }
            ]
        }
    ],
    max_tokens=1000
)
print(response.choices[0].message.content)
