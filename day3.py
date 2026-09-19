import base64
import time
import os
from openai import OpenAI

client = OpenAI(
    api_key= os.environ.get("OPENROUTER_KEY"),
    base_url= "https://openrouter.ai/api/v1"
)

description = []

#拿到文件夹里每张图片的路径进行读取
frames = sorted(os.listdir("frames"))
for filename in frames:
    path = os.path.join("frames",filename)
    with open(path,"rb") as f:
        raw_bytes = f.read()
    b64_string = base64.b64encode(raw_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model= "qwen/qwen2.5-vl-72b-instruct",
        messages=[
            {
                "role":"user",
                "content":[
                    #图片
                    {
                        "type":"image_url",
                        "image_url":{
                            "url":f"data:image/png;base64,{b64_string}"
                        }
                    },
                    #文字
                    {
                        "type":"text",
                        "text":"描述出这张截图里的画面，人物，场景和氛围。"
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    description.append(response.choices[0].message.content)
    time.sleep(3)

#最后一次总结
response = client.chat.completions.create(
    model="qwen/qwen2.5-vl-72b-instruct",
    messages=[
        {
            "role":"user",
            "content":[
                #only文字
                {
                    "type":"text",
                    "text":"以下是一段视频逐帧的描述，请写一段完整的观后感：\n" + "\n".join(description)
                }
            ]
        }
    ],
    max_tokens=1000
)
print(response.choices[0].message.content)