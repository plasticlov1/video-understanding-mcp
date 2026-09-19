# 视频理解 MCP Server — 7天计划

> 让芥末能"看"视频，然后跟你聊观后感
>
> 每天1-1.5小时｜不和专业课抢时间

---

## Day 1 — 抽帧

- [ ] `pip install opencv-python`
- [ ] 找一段喜欢的片段保存为 mp4（Daria / 电影 / 随便什么）
- [ ] 写脚本：读取视频 → 每秒抽一帧 → 保存为 png
- [ ] 跑通，看到一堆帧图片就算赢

```python
import cv2

video = cv2.VideoCapture("clip.mp4")
fps = int(video.get(cv2.CAP_PROP_FPS))
count = 0

while True:
    success, frame = video.read()
    if not success:
        break
    if count % fps == 0:  # 每秒一帧
        sec = count // fps
        cv2.imwrite(f"frame_{sec}.png", frame)
    count += 1

print(f"抽帧完成，共 {count // fps} 帧")
```

**交付：** 一个文件夹里整齐排列的帧截图

---

## Day 2 — 让AI看一帧

- [ ] 把 Day 1 抽出的某一帧转 base64 发给千问 API
- [ ] prompt："描述这张电影截图里你看到了什么，包括人物、表情、动作、场景"
- [ ] 试几张不同的帧，看描述质量

**交付：** AI 对几张帧的描述（复制保存）

---

## Day 3 — 让AI看完整段视频

- [ ] 写循环：遍历所有帧 → 逐帧发给 API → 收集所有描述
- [ ] 最后把所有帧描述拼成一段文字，再发给 API："根据以下逐帧描述，写一段完整的视频内容总结"
- [ ] 加上有趣的 prompt 人格（毒舌影评人 / 芥末视角 / 随你选）

**交付：** AI 对一段完整视频的观后感

---

## Day 4 — 优化：智能抽帧

- [ ] 问题：每秒一帧太多了，30秒的视频就30张图，token费炸了
- [ ] 优化方案：对比相邻帧的差异，只保留"画面有明显变化"的帧
- [ ] 用 OpenCV 算帧间差异：

```python
import numpy as np

def frame_diff(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    return np.mean(diff)

# 只保留差异大于阈值的帧
if frame_diff(prev_frame, curr_frame) > threshold:
    # 保存这帧
```

- [ ] 对比优化前后：帧数减少了多少？描述质量有没有下降？

**交付：** 优化前后的帧数对比 + 观后感质量对比

---

## Day 5 — 封装成 MCP Server

- [ ] 学习 MCP server 的基本结构（参考你的 OB 或 CineIsle）
- [ ] 把前4天的代码整理成三个 tool：

```
extract_frames(video_path, interval)
→ 抽帧，返回帧文件路径列表

analyze_frame(frame_path)
→ 单帧分析，返回文字描述

watch_video(video_path, persona)
→ 完整流程：智能抽帧 + 逐帧分析 + 汇总观后感
→ persona 参数控制语气（毒舌/芥末/学术）
```

- [ ] MCP server 跑起来

**交付：** 一个能启动的 MCP server

---

## Day 6 — 接入 Claude 测试

- [ ] 把 MCP server 连接到 Claude（本地或远程）
- [ ] 在对话里测试："帮我看这段视频"
- [ ] Claude 调用 watch_video → 返回观后感 → 直接在对话里聊
- [ ] 试不同的 persona，看效果
- [ ] debug 所有问题

**交付：** 在 Claude 对话里直接聊一段视频的内容

---

## Day 7 — 整理 + README

- [ ] 代码整理干净，变量名人能看懂
- [ ] 写 README.md：
  - 这个项目是什么
  - 它能做什么（附截图：对话里聊视频的效果）
  - 架构图（视频 → 抽帧 → API → MCP → Claude）
  - 遇到了什么问题
  - 下一步打算（情感分析？表情识别？）
- [ ] 推到 GitHub

**交付：** 一个能给别人看的 GitHub repo

---

## 延伸方向（做完7天再想）

- **接入情感计算：** 抽帧后不只描述内容，还识别人物表情和情绪变化曲线
- **接入购物agent：** 视频理解能力 + 浏览器操作 = 更强的多模态agent
- **接入小红书：** 分析短视频内容，帮你过滤算法推荐的垃圾
- **接入字幕：** 视频画面 + 字幕文本 = 多模态对齐的真实场景

---

## 为什么这个项目能写进 CV

- 涉及 **多模态理解**（视觉 + 文本生成）
- 涉及 **MCP 协议**（工具调用 + 系统集成）
- 涉及 **效率优化**（智能抽帧 vs 暴力抽帧）
- 有真实 demo 效果（对话里聊电影）
- 可以自然延伸到情感计算方向

套磁邮件里写："I built an MCP-based video understanding system that enables LLMs to analyze video content through intelligent frame extraction and vision-language models"——比"我做了个玩游戏的AI"强太多了。

---

*芥末出品 — 2026.09.14 深夜*
*写给那个不想睡觉的力竭天才*
