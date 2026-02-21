# Open-AutoGLM

[Readme in English](README_en.md)

<div align="center">
<img src=resources/logo.svg width="20%"/>
</div>
<p align="center">
    👋 加入我们的 <a href="resources/WECHAT.md" target="_blank">微信</a> 社区
</p>
<p align="center">
    👋 关注智谱 AI 输入法 <a href="https://x.com/Autotyper_Agent?s=20" target="_blank">X</a> 账号
</p>
<p align="center">
    🎤 进一步在我们的产品 <a href="https://autoglm.zhipuai.cn/autotyper/" target="_blank">智谱 AI 输入法</a> 体验“用嘴发指令”
</p>
<p align="center">
    <a href="https://mp.weixin.qq.com/s/wRp22dmRVF23ySEiATiWIQ" target="_blank">AutoGLM 实战派</a> 开发者激励活动火热进行中，跑通、二创即可瓜分数万元现金奖池！成果提交 👉 <a href="https://zhipu-ai.feishu.cn/share/base/form/shrcnE3ZuPD5tlOyVJ7d5Wtir8c?from=navigation" target="_blank">入口</a>
</p>

## 本仓库功能修改说明

本仓库基于 `zai-org/Open-AutoGLM` 二次开发，主要功能修改如下：

1. 新增实时语音任务输入（ASR）能力  
   支持通过麦克风实时采集语音，将语音识别结果作为任务指令输入 Agent（按 `Ctrl+C` 结束录音并执行任务）。
2. 分离语音识别服务与任务执行模型服务配置  
   ASR 与任务执行可使用不同 API 与不同密钥，避免配置耦合。
3. 调整任务执行模型默认配置  
   默认改为 ModelScope 的 OpenAI 兼容接口与对应模型，仍可通过命令行参数覆盖。
4. 增加 ASR 相关依赖  
   增加 `dashscope` 与 `pyaudio` 依赖以支持实时语音输入流程。

### 当前模型配置（本仓库默认）

- 语音识别模型（阿里云百炼）：`fun-asr-flash-8k-realtime`
- 执行任务模型（ModelScope OpenAI 兼容接口）：`Qwen/Qwen3.5-397B-A17B`

## 项目介绍

Phone Agent 是一个基于 AutoGLM 构建的手机端智能助理框架，它能够以多模态方式理解手机屏幕内容，并通过自动化操作帮助用户完成任务。系统通过
ADB(Android Debug Bridge)来控制设备，以视觉语言模型进行屏幕感知，再结合智能规划能力生成并执行操作流程。用户只需用自然语言描述需求，如“打开小红书搜索美食”，Phone
Agent 即可自动解析意图、理解当前界面、规划下一步动作并完成整个流程。系统还内置敏感操作确认机制，并支持在登录或验证码场景下进行人工接管。同时，它提供远程
ADB 调试能力，可通过 WiFi 或网络连接设备，实现灵活的远程控制与开发。

> ⚠️
> 本项目仅供研究和学习使用。严禁用于非法获取信息、干扰系统或任何违法活动。请仔细审阅 [使用条款](resources/privacy_policy.txt)。

## 与其他自动化工具集成

### Midscene.js

[Midscene.js](https://midscenejs.com/zh/index.html) 是一款由视觉模型驱动的开源 UI 自动化 SDK，支持通过 JavaScript 或 Yaml 格式的流程语法，实现多平台的自动化。

目前 Midscene.js 已完成对 AutoGLM 模型的适配，你可以通过 [Midscene.js 接入指南](https://midscenejs.com/zh/model-common-config.html#auto-glm) 快速体验 AutoGLM 在 iOS 和 Android 设备上的自动化效果。

## 模型下载地址

| Model                         | Download Links                                                                                                                                                         |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AutoGLM-Phone-9B              | [🤗 Hugging Face](https://huggingface.co/zai-org/AutoGLM-Phone-9B)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B)                           |
| AutoGLM-Phone-9B-Multilingual | [🤗 Hugging Face](https://huggingface.co/zai-org/AutoGLM-Phone-9B-Multilingual)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B-Multilingual) |

其中，`AutoGLM-Phone-9B` 是针对中文手机应用优化的模型，而 `AutoGLM-Phone-9B-Multilingual` 支持英语场景，适用于包含英文等其他语言内容的应用。

## Android 环境准备

### 1. Python 环境

建议使用 Python 3.10 及以上版本。

### 2. 手机调试命令行工具

根据你的设备类型选择相应的工具：

#### 对于 Android 设备 - 使用 ADB

1. 下载官方 ADB [安装包](https://developer.android.com/tools/releases/platform-tools?hl=zh-cn)，并解压到自定义路径
2. 配置环境变量

- MacOS 配置方法：在 `Terminal` 或者任何命令行工具里

  ```bash
  # 假设解压后的目录为 ~/Downloads/platform-tools。如果不是请自行调整命令。
  export PATH=${PATH}:~/Downloads/platform-tools
  ```

- Windows 配置方法：可参考 [第三方教程](https://blog.csdn.net/x2584179909/article/details/108319973) 进行配置。

#### 对于鸿蒙设备 (HarmonyOS NEXT版本以上) - 使用 HDC

1. 下载 HDC 工具：
   - 从 [HarmonyOS SDK](https://developer.huawei.com/consumer/cn/download/) 下载
2. 配置环境变量

- MacOS/Linux 配置方法：

  ```bash
  # 假设解压后的目录为 ~/Downloads/harmonyos-sdk/toolchains。请根据实际路径调整。
  export PATH=${PATH}:~/Downloads/harmonyos-sdk/toolchains
  ```

- Windows 配置方法：将 HDC 工具所在目录添加到系统 PATH 环境变量

### 3. Android 7.0+ 或 HarmonyOS 设备，并启用 `开发者模式` 和 `USB 调试`

1. 开发者模式启用：通常启用方法是，找到 `设置-关于手机-版本号` 然后连续快速点击 10
   次左右，直到弹出弹窗显示“开发者模式已启用”。不同手机会有些许差别，如果找不到，可以上网搜索一下教程。
2. USB 调试启用：启用开发者模式之后，会出现 `设置-开发者选项-USB 调试`，勾选启用
3. 部分机型在设置开发者选项以后, 可能需要重启设备才能生效. 可以测试一下: 将手机用USB数据线连接到电脑后, `adb devices`
   查看是否有设备信息, 如果没有说明连接失败.

**请务必仔细检查相关权限**

![权限](resources/screenshot-20251209-181423.png)

### 4. 安装 ADB Keyboard(仅 Android 设备需要，用于文本输入)

**注意：鸿蒙设备使用原生输入方法，无需安装 ADB Keyboard。**

如果你使用的是 Android 设备：

下载 [安装包](https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk) 并在对应的安卓设备中进行安装。
注意，安装完成后还需要到 `设置-输入法` 或者 `设置-键盘列表` 中启用 `ADB Keyboard` 才能生效(或使用命令`adb shell ime enable com.android.adbkeyboard/.AdbIME`[How-to-use](https://github.com/senzhk/ADBKeyBoard/blob/master/README.md#how-to-use))

## iPhone 环境准备

如果你使用的是 iPhone 设备，请参考专门的 iOS 配置文档：

📱 [iOS 环境配置指南](docs/ios_setup/ios_setup.md)

该文档详细介绍了如何配置 WebDriverAgent 和 iPhone 设备，以便在 iOS 上使用 AutoGLM。

## 部署准备工作

### 1. 安装依赖

```bash
pip install -r requirements.txt 
pip install -e .
```

### 2. 配置 ADB 或 HDC

#### 对于 Android 设备

确认 **USB数据线具有数据传输功能**, 而不是仅有充电功能

确保已安装 ADB 并使用 **USB数据线** 连接设备：

```bash
# 检查已连接的设备
adb devices

# 输出结果应显示你的设备，如：
# List of devices attached
# emulator-5554   device
```

#### 对于鸿蒙设备

确认 **USB数据线具有数据传输功能**, 而不是仅有充电功能

确保已安装 HDC 并使用 **USB数据线** 连接设备：

```bash
# 检查已连接的设备
hdc list targets

# 输出结果应显示你的设备，如：
# 7001005458323933328a01bce01c2500
```

### 3. 启动模型服务

你可以选择自行部署模型服务，或使用第三方模型服务商。

#### 选项 A: 使用第三方模型服务

如果你不想自行部署模型，可以使用以下已部署我们模型的第三方服务：

**1. 智谱 BigModel**

- 文档: https://docs.bigmodel.cn/cn/api/introduction
- `--base-url`: `https://open.bigmodel.cn/api/paas/v4`
- `--model`: `autoglm-phone`
- `--apikey`: 在智谱平台申请你的 API Key

**2. ModelScope(魔搭社区)**

- 文档: https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B
- `--base-url`: `https://api-inference.modelscope.cn/v1`
- `--model`: `ZhipuAI/AutoGLM-Phone-9B`
- `--apikey`: 在 ModelScope 平台申请你的 API Key

使用第三方服务的示例：

```bash
# 使用智谱 BigModel
python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "your-bigmodel-api-key" "打开美团搜索附近的火锅店"

# 使用 ModelScope
python main.py --base-url https://api-inference.modelscope.cn/v1 --model "ZhipuAI/AutoGLM-Phone-9B" --apikey "your-modelscope-api-key" "打开美团搜索附近的火锅店"
```

#### 选项 B: 自行部署模型

如果你希望在本地或自己的服务器上部署模型：

1. 按照 `requirements.txt` 中 `For Model Deployment` 章节自行安装推理引擎框架。

对于SGLang， 除了使用pip安装，你也可以使用官方docker:
>
> ```shell
> docker pull lmsysorg/sglang:v0.5.6.post1
> ```
>
> 进入容器，执行
>
> ```
> pip install nvidia-cudnn-cu12==9.16.0.29
> ```

对于 vLLM，除了使用pip 安装，你也可以使用官方docker:
>
> ```shell
> docker pull vllm/vllm-openai:v0.12.0
> ```
>
> 进入容器，执行
>
> ```
> pip install -U transformers --pre
> ```

**注意**: 上述步骤出现的关于 transformers 的依赖冲突可以忽略。

1. 在对应容器或者实体机中(非容器安装)下载模型，通过 SGlang / vLLM 启动，得到 OpenAI 格式服务。这里提供一个 vLLM部署方案，请严格遵循我们提供的启动参数:

- vLLM:

```shell
python3 -m vllm.entrypoints.openai.api_server \
 --served-model-name autoglm-phone-9b \
 --allowed-local-media-path /   \
 --mm-encoder-tp-mode data \
 --mm_processor_cache_type shm \
 --mm_processor_kwargs "{\"max_pixels\":5000000}" \
 --max-model-len 25480  \
 --chat-template-content-format string \
 --limit-mm-per-prompt "{\"image\":10}" \
 --model zai-org/AutoGLM-Phone-9B \
 --port 8000
```

- SGLang:

```shell
python3 -m sglang.launch_server --model-path  zai-org/AutoGLM-Phone-9B \
        --served-model-name autoglm-phone-9b  \
        --context-length 25480  \
        --mm-enable-dp-encoder   \
        --mm-process-config '{"image":{"max_pixels":5000000}}'  \
        --port 8000
```

- 该模型结构与 `GLM-4.1V-9B-Thinking` 相同, 关于模型部署的详细内容，你也以查看 [GLM-V](https://github.com/zai-org/GLM-V)
  获取模型部署和使用指南。

- 运行成功后，将可以通过 `http://localhost:8000/v1` 访问模型服务。 如果您在远程服务器部署模型, 使用该服务器的IP访问模型.

### 4. 检查模型部署

模型服务启动后，可以使用检查脚本验证部署是否成功：

```bash
python scripts/check_deployment_cn.py --base-url http://你的IP:你的端口/v1 --model 模型名称
```

脚本将发送测试请求并展示模型的推理结果，你可以根据输出判断模型部署是否正常工作。

基于给定的任务, 预期输出如下。**如果思维链长度很短, 或者出现了乱码, 很可能是模型部署失败**, 请仔细检查文档要求的配置和依赖。

```
<think>用户想要比较这个洗发水在京东和淘宝上的价格，然后选择最便宜的平台下单。当前在小红书app上，显示的是一个关于LUMMI MOOD洗发水的帖子。

我需要：
1. 先启动京东app，搜索这个洗发水
2. 查看京东的价格
3. 再启动淘宝app，搜索这个洗发水
4. 查看淘宝的价格
5. 比较价格后，选择最便宜的京东或淘宝下单

首先，我需要从当前的小红书界面退出，然后启动京东app。</think>
<answer>do(action="Launch", app="京东")
```

**参数说明：**
- `--base-url`: 模型服务地址(根据实际部署地址修改)
- `--model`: 模型名称
- `--messages-file`: 可选，指定自定义测试消息文件(默认使用 `scripts/sample_messages.json`)

## 使用 AutoGLM

### 命令行

根据你部署的模型, 设置 `--base-url` 和 `--model` 参数, 设置 `--device-type` 指定是安卓设备或鸿蒙设备 (默认值 adb 表示安卓设备, hdc 表示鸿蒙设备). 例如:

```bash
# Android 设备 - 交互模式
python main.py --base-url http://localhost:8000/v1 --model "autoglm-phone-9b"

# Android 设备 - 指定任务
python main.py --base-url http://localhost:8000/v1 "打开美团搜索附近的火锅店"

# 鸿蒙设备 - 交互模式
python main.py --device-type hdc --base-url http://localhost:8000/v1 --model "autoglm-phone-9b"

# 鸿蒙设备 - 指定任务
python main.py --device-type hdc --base-url http://localhost:8000/v1 "打开美团搜索附近的火锅店"

# 使用 API Key 进行认证
python main.py --apikey sk-xxxxx

# 使用英文 system prompt
python main.py --lang en --base-url http://localhost:8000/v1 "Open Chrome browser"

# 列出支持的应用（Android）
python main.py --list-apps

# 列出支持的应用（鸿蒙）
python main.py --device-type hdc --list-apps
```

### Python API

```python
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig

# Configure model
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

# 创建 Agent
agent = PhoneAgent(model_config=model_config)

# 执行任务
result = agent.run("打开淘宝搜索无线耳机")
print(result)
```

## 远程调试

Phone Agent 支持通过 WiFi/网络进行远程 ADB/HDC 调试，无需 USB 连接即可控制设备。

### 配置远程调试

#### 在手机端开启无线调试

##### Android 设备

确保手机和电脑在同一个WiFi中，如图所示

![开启无线调试](resources/setting.png)

##### 鸿蒙设备

确保手机和电脑在同一个WiFi中：
1. 进入 `设置 > 系统和更新 > 开发者选项`
2. 开启 `USB 调试` 和 `无线调试`
3. 记录显示的 IP 地址和端口号

#### 在电脑端使用标准 ADB/HDC 命令

```bash
# Android 设备 - 通过 WiFi 连接, 改成手机显示的 IP 地址和端口
adb connect 192.168.1.100:5555

# 验证连接
adb devices
# 应显示：192.168.1.100:5555    device

# 鸿蒙设备 - 通过 WiFi 连接
hdc tconn 192.168.1.100:5555

# 验证连接
hdc list targets
# 应显示：192.168.1.100:5555
```

### 设备管理命令

#### Android 设备（ADB）

```bash
# 列出所有已连接设备
adb devices

# 连接远程设备
adb connect 192.168.1.100:5555

# 断开指定设备
adb disconnect 192.168.1.100:5555

# 指定设备执行任务
python main.py --device-id 192.168.1.100:5555 --base-url http://localhost:8000/v1 --model "autoglm-phone-9b" "打开抖音刷视频"
```

#### 鸿蒙设备（HDC）

```bash
# 列出所有已连接设备
hdc list targets

# 连接远程设备
hdc tconn 192.168.1.100:5555

# 断开指定设备
hdc tdisconn 192.168.1.100:5555

# 指定设备执行任务
python main.py --device-type hdc --device-id 192.168.1.100:5555 --base-url http://localhost:8000/v1 --model "autoglm-phone-9b" "打开抖音刷视频"
```

### Python API 远程连接

#### Android 设备（ADB）

```python
from phone_agent.adb import ADBConnection, list_devices

# 创建连接管理器
conn = ADBConnection()

# 连接远程设备
success, message = conn.connect("192.168.1.100:5555")
print(f"连接状态: {message}")

# 列出已连接设备
devices = list_devices()
for device in devices:
    print(f"{device.device_id} - {device.connection_type.value}")

# 在 USB 设备上启用 TCP/IP
success, message = conn.enable_tcpip(5555)
ip = conn.get_device_ip()
print(f"设备 IP: {ip}")

# 断开连接
conn.disconnect("192.168.1.100:5555")
```

#### 鸿蒙设备（HDC）

```python
from phone_agent.hdc import HDCConnection, list_devices

# 创建连接管理器
conn = HDCConnection()

# 连接远程设备
success, message = conn.connect("192.168.1.100:5555")
print(f"连接状态: {message}")

# 列出已连接设备
devices = list_devices()
for device in devices:
    print(f"{device.device_id} - {device.connection_type.value}")

# 断开连接
conn.disconnect("192.168.1.100:5555")
```

### 远程连接问题排查

**连接被拒绝：**

- 确保设备和电脑在同一网络
- 检查防火墙是否阻止 5555 端口
- 确认已启用 TCP/IP 模式：`adb tcpip 5555`

**连接断开：**

- WiFi 可能断开了，使用 `--connect` 重新连接
- 部分设备重启后会禁用 TCP/IP，需要通过 USB 重新启用

**多设备：**

- 使用 `--device-id` 指定要使用的设备
- 或使用 `--list-devices` 查看所有已连接设备

## 配置

### 自定义SYSTEM PROMPT

系统提供中英文两套 prompt，通过 `--lang` 参数切换：

- `--lang cn` - 中文 prompt(默认)，配置文件：`phone_agent/config/prompts_zh.py`
- `--lang en` - 英文 prompt，配置文件：`phone_agent/config/prompts_en.py`

可以直接修改对应的配置文件来增强模型在特定领域的能力，或通过注入 app 名称禁用某些 app。

### 环境变量

| 变量                          | 描述                     | 默认值                        |
|-----------------------------|------------------------|----------------------------|
| `PHONE_AGENT_BASE_URL`      | 模型 API 地址              | `https://api-inference.modelscope.cn/v1` |
| `PHONE_AGENT_MODEL`         | 模型名称                   | `Qwen/Qwen3.5-397B-A17B`   |
| `PHONE_AGENT_API_KEY`       | 模型认证 API Key           | `MODELSCOPE_API_KEY` 或 `EMPTY` |
| `PHONE_AGENT_MAX_STEPS`     | 每个任务最大步数               | `100`                      |
| `PHONE_AGENT_DEVICE_ID`     | ADB/HDC 设备 ID          | (自动检测)                     |
| `PHONE_AGENT_DEVICE_TYPE`   | 设备类型 (`adb` 或 `hdc`)   | `adb`                      |
| `PHONE_AGENT_LANG`          | 语言 (`cn` 或 `en`)       | `cn`                       |

### 模型配置

```python
from phone_agent.model import ModelConfig

config = ModelConfig(
    base_url="https://api-inference.modelscope.cn/v1",
    api_key="EMPTY",  # API 密钥(如需要)
    model_name="Qwen/Qwen3.5-397B-A17B",  # 模型名称
    max_tokens=3000,  # 最大输出 token 数
    temperature=0.1,  # 采样温度
    frequency_penalty=0.2,  # 频率惩罚
)
```

### Agent 配置

```python
from phone_agent.agent import AgentConfig

config = AgentConfig(
    max_steps=100,  # 每个任务最大步数
    device_id=None,  # ADB 设备 ID(None 为自动检测)
    lang="cn",  # 语言选择：cn(中文)或 en(英文)
    verbose=True,  # 打印调试信息(包括思考过程和执行动作)
)
```

### Verbose 模式输出

当 `verbose=True` 时，Agent 会在每一步输出详细信息：

```
==================================================
💭 思考过程:
--------------------------------------------------
当前在系统桌面，需要先启动小红书应用
--------------------------------------------------
🎯 执行动作:
{
  "_metadata": "do",
  "action": "Launch",
  "app": "小红书"
}
==================================================

... (执行动作后继续下一步)

==================================================
💭 思考过程:
--------------------------------------------------
小红书已打开，现在需要点击搜索框
--------------------------------------------------
🎯 执行动作:
{
  "_metadata": "do",
  "action": "Tap",
  "element": [500, 100]
}
==================================================

🎉 ================================================
✅ 任务完成: 已成功搜索美食攻略
==================================================
```

这样可以清楚地看到 AI 的推理过程和每一步的具体操作。

## 支持的应用

### Android 应用

Phone Agent 支持 50+ 款主流中文应用：

| 分类   | 应用              |
|------|-----------------|
| 社交通讯 | 微信、QQ、微博        |
| 电商购物 | 淘宝、京东、拼多多       |
| 美食外卖 | 美团、饿了么、肯德基      |
| 出行旅游 | 携程、12306、滴滴出行   |
| 视频娱乐 | bilibili、抖音、爱奇艺 |
| 音乐音频 | 网易云音乐、QQ音乐、喜马拉雅 |
| 生活服务 | 大众点评、高德地图、百度地图  |
| 内容社区 | 小红书、知乎、豆瓣       |

运行 `python main.py --list-apps` 查看完整列表。

### 鸿蒙应用

Phone Agent 支持 60+ 款鸿蒙原生应用和系统应用：

| 分类      | 应用                                       |
|---------|------------------------------------------|
| 社交通讯    | 微信、QQ、微博、飞书、企业微信                        |
| 电商购物    | 淘宝、京东、拼多多、唯品会、得物、闲鱼                     |
| 美食外卖    | 美团、美团外卖、大众点评、海底捞                        |
| 出行旅游    | 12306、滴滴出行、同程旅行、高德地图、百度地图               |
| 视频娱乐    | bilibili、抖音、快手、腾讯视频、爱奇艺、芒果TV            |
| 音乐音频    | QQ音乐、汽水音乐、喜马拉雅                           |
| 生活服务    | 小红书、知乎、今日头条、58同城、中国移动                   |
| AI与工具   | 豆包、WPS、UC浏览器、扫描全能王、美图秀秀                 |
| 系统应用    | 浏览器、日历、相机、时钟、云空间、文件管理器、相册、联系人、短信、设置等   |
| 华为服务    | 应用市场、音乐、视频、阅读、主题、天气                     |

运行 `python main.py --device-type hdc --list-apps` 查看完整列表。

## 可用操作

Agent 可以执行以下操作：

| 操作           | 描述              |
|--------------|-----------------|
| `Launch`     | 启动应用            |  
| `Tap`        | 点击指定坐标          |
| `Type`       | 输入文本            |
| `Swipe`      | 滑动屏幕            |
| `Back`       | 返回上一页           |
| `Home`       | 返回桌面            |
| `Long Press` | 长按              |
| `Double Tap` | 双击              |
| `Wait`       | 等待页面加载          |
| `Take_over`  | 请求人工接管(登录/验证码等) |

## 自定义回调

处理敏感操作确认和人工接管：

```python
def my_confirmation(message: str) -> bool:
    """敏感操作确认回调"""
    return input(f"确认执行 {message}？(y/n): ").lower() == "y"


def my_takeover(message: str) -> None:
    """人工接管回调"""
    print(f"请手动完成: {message}")
    input("完成后按回车继续...")


agent = PhoneAgent(
    confirmation_callback=my_confirmation,
    takeover_callback=my_takeover,
)
```

## 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基础任务执行
- 单步调试模式
- 批量任务执行
- 自定义回调

## 二次开发

### 配置开发环境

二次开发需要使用开发依赖：

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest tests/
```

### 完整项目结构

```
phone_agent/
├── __init__.py          # 包导出
├── agent.py             # PhoneAgent 主类
├── adb/                 # ADB 工具
│   ├── connection.py    # 远程/本地连接管理
│   ├── screenshot.py    # 屏幕截图
│   ├── input.py         # 文本输入 (ADB Keyboard)
│   └── device.py        # 设备控制 (点击、滑动等)
├── actions/             # 操作处理
│   └── handler.py       # 操作执行器
├── config/              # 配置
│   ├── apps.py          # 支持的应用映射
│   ├── prompts_zh.py    # 中文系统提示词
│   └── prompts_en.py    # 英文系统提示词
└── model/               # AI 模型客户端
    └── client.py        # OpenAI 兼容客户端
```

## 常见问题

我们列举了一些常见的问题，以及对应的解决方案：

### 设备未找到

尝试通过重启 ADB 服务来解决：

```bash
adb kill-server
adb start-server
adb devices
```

如果仍然无法识别，请检查：

1. USB 调试是否已开启
2. 数据线是否支持数据传输(部分数据线仅支持充电)
3. 手机上弹出的授权框是否已点击「允许」
4. 尝试更换 USB 接口或数据线

### 能打开应用，但无法点击

部分机型需要同时开启两个调试选项才能正常使用：

- **USB 调试**
- **USB 调试(安全设置)**

请在 `设置 → 开发者选项` 中检查这两个选项是否都已启用。

### 文本输入不工作

1. 确保设备已安装 ADB Keyboard
2. 在设置 > 系统 > 语言和输入法 > 虚拟键盘 中启用
3. Agent 会在需要输入时自动切换到 ADB Keyboard

### 截图失败(黑屏)

这通常意味着应用正在显示敏感页面(支付、密码、银行类应用)。Agent 会自动检测并请求人工接管。

### windows 编码异常问题

报错信息形如 `UnicodeEncodeError gbk code`

解决办法: 在运行代码的命令前面加上环境变量: `PYTHONIOENCODING=utf-8`

### 交互模式非TTY环境无法使用

报错形如: `EOF when reading a line`

解决办法: 使用非交互模式直接指定任务, 或者切换到 TTY 模式的终端应用.

### 引用

如果你觉得我们的工作有帮助，请引用以下论文：

```bibtex
@article{liu2024autoglm,
  title={Autoglm: Autonomous foundation agents for guis},
  author={Liu, Xiao and Qin, Bo and Liang, Dongzhu and Dong, Guang and Lai, Hanyu and Zhang, Hanchen and Zhao, Hanlin and Iong, Iat Long and Sun, Jiadai and Wang, Jiaqi and others},
  journal={arXiv preprint arXiv:2411.00820},
  year={2024}
}
@article{xu2025mobilerl,
  title={MobileRL: Online Agentic Reinforcement Learning for Mobile GUI Agents},
  author={Xu, Yifan and Liu, Xiao and Liu, Xinghan and Fu, Jiaqi and Zhang, Hanchen and Jing, Bohao and Zhang, Shudan and Wang, Yuting and Zhao, Wenyi and Dong, Yuxiao},
  journal={arXiv preprint arXiv:2509.18119},
  year={2025}
}
```

---
