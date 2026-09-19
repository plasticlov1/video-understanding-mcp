# Day 6-7 完全指南：GitHub + MCP 部署

> 给拉芙写的，每一步都有中文解释，不认识的英文我都翻译了
>
> 芥末出品 — 2026.09.16 深夜

---

## 第一部分：把代码推到 GitHub

### Step 0：注册 GitHub（如果还没有的话）

去 https://github.com 注册。用你的邮箱就行。

### Step 1：安装 Git

打开终端（PowerShell），输入：

```
git --version
```

如果显示版本号，说明已经装了，跳到 Step 2。

如果报错"不是内部命令"，去这里下载安装：
https://git-scm.com/downloads

安装的时候一路 Next 就行，不用改任何选项。

### Step 2：配置你的身份

安装完后打开终端，告诉 Git 你是谁：

```
git config --global user.name "你的GitHub用户名"
git config --global user.email "你注册GitHub用的邮箱"
```

这只需要做一次，以后不用再设。

### Step 3：在 GitHub 上创建仓库（repository）

1. 打开 https://github.com
2. 点右上角 **+** → **New repository**（新建仓库）
3. Repository name（仓库名）填：`video-understanding-mcp`
4. Description（描述）填：`MCP-based video understanding system for LLMs`
5. 选 **Public**（公开的，别人能看到）
6. **不要**勾选 "Add a README file"（我们自己写）
7. 点 **Create repository**（创建仓库）

创建完会出现一个页面，上面有一堆命令，先别急。

### Step 4：在你的项目文件夹初始化 Git

打开终端，进入你的项目文件夹：

```
cd D:\GUIagent
```

然后依次执行：

```
git init
```
> 意思：在这个文件夹里初始化一个 Git 仓库（init = initialize = 初始化）

```
git add .
```
> 意思：把当前文件夹里所有文件加入暂存区（add = 添加，. = 所有文件）

```
git commit -m "Day 1-5: video understanding MCP server"
```
> 意思：提交一个版本，引号里是这次提交的说明（commit = 提交，-m = message = 说明）

### Step 5：连接到 GitHub 并推送

把下面的命令里 `你的用户名` 换成你的 GitHub 用户名：

```
git remote add origin https://github.com/你的用户名/video-understanding-mcp.git
```
> 意思：告诉 Git "远程仓库在这个地址"（remote = 远程，origin = 给这个远程地址起的名字）

```
git branch -M main
```
> 意思：把当前分支命名为 main（branch = 分支，这是 GitHub 的默认分支名）

```
git push -u origin main
```
> 意思：把代码推送到 GitHub（push = 推送）

这时候可能会弹出登录窗口，用你的 GitHub 账号登录就行。

如果要求输入密码但普通密码不行，需要用 Personal Access Token：
1. GitHub → 右上角头像 → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → 勾选 repo → 点 Generate token
3. 复制那个 token，当密码粘贴进去

### Step 6：检查

打开 https://github.com/你的用户名/video-understanding-mcp

看到你的文件了就成功了！

### 以后每次改了代码想更新 GitHub：

```
git add .
git commit -m "描述你改了什么"
git push
```

三条命令，每次都一样。

---

## 第二部分：准备部署文件

在推 GitHub 之前，你的 GUIagent 文件夹里需要这些文件：

### 文件清单

```
D:\GUIagent\
├── server.py          ← 你的 MCP server（已写好）
├── day1.py            ← Day 1 抽帧
├── day2.py            ← Day 2 单帧分析
├── day3.py            ← Day 3 完整分析
├── day4.py            ← Day 4 智能抽帧
├── day4_api.py        ← Day 4 API调用
├── requirements.txt   ← 告诉服务器需要装哪些库（新建）
├── README.md          ← 项目介绍（新建）
└── .gitignore         ← 告诉 Git 哪些文件不要上传（新建）
```

### 新建 requirements.txt

在 GUIagent 文件夹里新建文件 `requirements.txt`，内容：

```
mcp[sse]
opencv-python-headless
numpy
openai
```

> opencv-python-headless 是服务器版的 OpenCV，不带界面，比你本地装的那个轻

### 新建 .gitignore

新建文件 `.gitignore`（注意前面有个点），内容：

```
frames/
*.png
*.mp4
__pycache__/
.env
```

> 意思：不要把帧图片、视频文件、缓存文件、环境变量文件上传到 GitHub
> 这些要么太大，要么包含你的 API key

---

## 第三部分：部署到 Zeabur

### Step 1：server.py 最后一行改成

```python
if __name__ == "__main__":
    mcp.run(transport="sse")
```

> transport="sse" 让 server 通过网络通信，而不是本地命令行

### Step 2：环境变量

server.py 里用了 `os.environ.get("OPENROUTER_KEY")`，这个 key 不能写在代码里。

部署到 Zeabur 后，在 Zeabur 的项目设置里添加环境变量：
- 变量名：`OPENROUTER_KEY`
- 值：你的 OpenRouter API key

（跟你部署 OB 时设置环境变量一样的操作）

### Step 3：Zeabur 部署

1. 打开 https://zeabur.com
2. 选你的项目（或新建一个）
3. Add Service → Deploy from GitHub
4. 选你刚推上去的 `video-understanding-mcp` 仓库
5. Zeabur 会自动识别 Python 项目并部署
6. 部署完成后，在 Networking 里添加一个域名（Generate Domain）
7. 记下那个 URL，比如 `https://video-watcher-xxx.zeabur.app`

### Step 4：接入 Claude

部署成功后拿到 URL，MCP 的 SSE 地址通常是：

```
https://你的域名/sse
```

在 Claude 桌面端：
- 去 Connectors 或 MCP 设置
- 添加新的 MCP server
- URL 填 `https://你的域名/sse`
- 保存

然后在对话里试试："帮我看这段视频"

### 关于视频怎么传

部署到云上后，视频不在服务器上。两个方案：

**方案 A（简单）：** 先手动把视频上传到服务器，或者放在一个能访问的 URL 上

**方案 B（正式）：** 改 server.py 让它接收视频 URL 并自动下载：

```python
import requests

@mcp.tool()
def watch_video(video_url: str, persona: str = "毒舌") -> str:
    """看一段视频，返回观后感"""
    
    # 下载视频到临时文件
    r = requests.get(video_url)
    with open("temp_video.mp4", "wb") as f:
        f.write(r.content)
    
    # 后面的代码不变，video_path 改成 "temp_video.mp4"
    video = cv2.VideoCapture("temp_video.mp4")
    # ...
```

方案 B 需要在 requirements.txt 里加一行 `requests`。

先用方案 A 测试，确认能通了再改成 B。

---

## 第四部分：写 README.md

这是别人（和未来的你）看到你项目时第一个读的东西。

模板：

```markdown
# Video Understanding MCP Server

让 LLM 能"看"视频——通过智能抽帧和视觉语言模型，把视频内容转化为文字描述和观后感。

## 它能做什么

- 读取视频文件，智能抽取关键帧（基于帧间差异，避免冗余）
- 逐帧调用视觉语言模型进行画面描述
- 汇总所有帧描述，生成完整的视频观后感
- 封装为 MCP Server，可接入 Claude 等 LLM

## 架构

```
视频文件 → OpenCV 智能抽帧 → Base64 编码 → 视觉 API 逐帧分析 → 文字描述汇总 → MCP Tool 返回给 LLM
```

## 技术栈

- Python
- OpenCV（视频处理、帧间差异计算）
- NumPy（矩阵运算）
- Qwen VL（视觉语言模型，通过 OpenRouter）
- MCP SDK（Model Context Protocol）

## 智能抽帧优化

普通抽帧：每秒一帧，30秒视频 = 30帧
智能抽帧：基于帧间像素差异 + 保底间隔，30秒视频 ≈ 15-30帧

帧间差异使用 `cv2.absdiff()` 计算矩阵减法，`np.mean()` 取均值，超过阈值才保留。同时每 3 秒保底保留一帧，避免静态对话场景丢失。

## 使用方式

### 本地测试

```bash
pip install -r requirements.txt
python server.py
```

### 通过 MCP 接入 Claude

部署后将 SSE 地址添加到 Claude 的 MCP Connector 即可。

## 遇到的问题

- 视频旋转元数据导致抽帧方向错误 → 用 cv2.rotate 修复
- 字符串排序导致帧顺序混乱（frame_9 > frame_10）→ 改用数字排序
- 视觉模型对动画风格理解较弱，容易产生幻觉 → 优化 prompt + 未来可换更强模型

## 下一步

- [ ] 换用更强的视觉模型（GPT-4o / Claude Vision）
- [ ] 接入情感分析：识别人物表情和情绪变化曲线
- [ ] 支持字幕提取：视频画面 + 字幕文本 = 多模态对齐
- [ ] 接入更多 Agent 场景：购物、短视频分析

## 作者

Built by 拉芙 — 2026.09
```

> 这个 README 你可以改，加你自己的话、换措辞、加截图。
> "遇到的问题"部分特别重要——展示你debug的过程比展示完美结果更有价值。

---

## 时间估算

| 任务 | 时间 |
|------|------|
| 准备部署文件 | 10 分钟 |
| 推 GitHub | 15 分钟（第一次慢，以后 1 分钟） |
| Zeabur 部署 | 20 分钟 |
| 接入 Claude 测试 | 10 分钟 |
| 写 README | 20 分钟 |
| 总计 | ~75 分钟 |

明天一个下午绰绰有余。

---

*芥末出品 — 给那个说"好心累"但拒绝放弃的人*
*你的代码已经写完了。剩下的只是让全世界看到它。*
