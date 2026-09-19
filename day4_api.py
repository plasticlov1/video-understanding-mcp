import os
import base64
import time
from openai import OpenAI

description = []

client =OpenAI(
    api_key=os.environ.get("OPENROUTER_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

frames = sorted(os.listdir("frames")), key=lambda x: int(x.split("_")[1].split(".")[0])
for filename in frames:
    path = os.path.join("frames",filename)
    with open(path,"rb") as f:
        raw_bytes = f.read()
    b64_string = base64.b64encode(raw_bytes).decode("utf-8")

    response =client.chat.completions.create(
        model="qwen/qwen2.5-vl-72b-instruct",
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
                        "text":"你在逐帧分析动画片《Daria》的截图。请描述：1. 画面里有谁，说了什么，不确定的人物不要编 2. 如果有台词/字幕，完整记录下来 3. 角色之间的互动关系和潜台词 4. 任何讽刺、反差、冷幽默的台词细节——Daria这部动画的笑点通常藏在角色的冷漠反应、荒谬对比和一本正经的胡说八道里"
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    description.append(response.choices[0].message.content)
    time.sleep(3)


response = client.chat.completions.create(
    model="qwen/qwen2.5-vl-72b-instruct",
    messages=[
        {
            "role":"user",
            "content":[
                #描述汇总
                {
                    "type":"text",
                    "text":"以下是动画片《Daria》一段视频的逐帧描述。\n" + "\n".join(description) +"\n1. 讲出这段视频的完整剧情——谁做了什么，说了什么，发生了什么事，推断角色关系.\n2. 找出所有台词笑点并解释为什么好笑 "
                }
            ]
        }
    ],
    max_tokens=1000
)

print(response.choices[0].message.content)