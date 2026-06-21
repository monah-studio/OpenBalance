<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/dynamic/json?color=fff&label=&prefix=%E2%9A%96%EF%B8%8F%20OpenBalance%20v&query=tag_name&url=https%3A%2F%2Fapi.github.com%2Frepos%2FMonah-Limited%2FOpenBalance%2Freleases%2Flatest&style=for-the-badge&logo=appstore">
    <img src="https://img.shields.io/badge/⚖️_OpenBalance-1.1.0-1a1a2e?style=for-the-badge" alt="OpenBalance">
  </picture>
</p>

<p align="center">
  <b>Monitor your LLM API balances from the macOS menu bar</b><br>
  <b>在菜单栏查看所有 LLM API 余额 · 一键管理 31 个厂商</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/macOS-13%2B-000?logo=apple&logoColor=white" alt="macOS">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs">
  <img src="https://img.shields.io/github/stars/Monah-Limited/OpenBalance?style=flat" alt="Stars">
  <img src="https://img.shields.io/github/downloads/Monah-Limited/OpenBalance/total?color=blue" alt="Downloads">
</p>

<p align="center">
  <a href="#-supported-providers--支持厂商"><b>Providers</b></a> •
  <a href="#-quick-start--快速开始"><b>Quick Start</b></a> •
  <a href="#%EF%B8%8F-commands--命令参考"><b>Commands</b></a> •
  <a href="#-uninstall--卸载"><b>Uninstall</b></a> •
  <a href="#-build-from-source--从源码构建"><b>Build</b></a>
</p>

---

<br>

<p align="center">
  <i>"Install once, check all balances in one click."</i><br>
  <i>「一次安装，全部余额一目了然」</i>
</p>

<br>

# 🌟 Overview / 概述

<table>
<tr>
<td width="50%">

**OpenBalance** is a lightweight macOS menu bar app that tracks API balances across all your LLM providers. No more logging into 10 dashboards.

- 🔑 **Secure** — Keys in macOS Keychain, never on disk
- 🌏 **31 providers** — DeepSeek, Kimi, Qwen, OpenRouter, Groq...
- ⚡ **Auto-refresh** — Default every 5 minutes, adjustable
- 🧹 **Clean uninstall** — Built-in uninstaller wipes all traces

</td>
<td width="50%">

**OpenBalance** 是一款轻量级 macOS 菜单栏应用，让你在一个地方查看所有 LLM API 余额。再也不用登录 10 个后台去查余额。

- 🔑 **安全** — API key 存于 macOS 钥匙串，不会保存到本地文件
- 🌏 **31 个厂商** — DeepSeek、Kimi、Qwen、OpenRouter、Groq...
- ⚡ **自动刷新** — 默认每 5 分钟刷新，可调整
- 🧹 **彻底卸载** — 内建卸载器，清除所有数据 + 钥匙串条目

</td>
</tr>
</table>

<br>

# 🗺 Supported Providers / 支持厂商

<p align="center"><b>31 providers pre-configured with China (大陆) & International (海外) endpoints</b></p>
<p align="center"><b>31 个厂商已预设，大陆/海外 endpoint 都已配置</b></p>

<table>
<tr>
<th>#</th><th>Provider</th><th>EndPoint</th><th>¥/$</th><th>Status</th>
</tr>
<tr><td>1</td><td><b>DeepSeek</b></td><td><code>/user/balance</code></td><td>¥</td><td>✅</td></tr>
<tr><td>2</td><td><b>Kimi (月之暗面 大陆)</b></td><td><code>moonshot.cn/v1/users/me/balance</code></td><td>¥</td><td>✅</td></tr>
<tr><td>3</td><td><b>Kimi (Moonshot 海外)</b></td><td><code>moonshot.ai/v1/users/me/balance</code></td><td>$</td><td>✅</td></tr>
<tr><td>4</td><td><b>智谱 GLM</b></td><td><code>open.bigmodel.cn/api/llm/balance</code></td><td>¥</td><td>✅</td></tr>
<tr><td>5</td><td><b>SiliconFlow 大陆</b></td><td><code>siliconflow.cn/v1/user/info</code></td><td>¥</td><td>✅</td></tr>
<tr><td>6</td><td><b>SiliconFlow 海外</b></td><td><code>siliconflow.com/v1/user/info</code></td><td>$</td><td>✅</td></tr>
<tr><td>7</td><td><b>通义千问 (Qwen 大陆)</b></td><td><code>dashscope.aliyuncs.com/.../balance</code></td><td>¥</td><td>✅</td></tr>
<tr><td>8</td><td><b>通义千问 (Qwen 海外)</b></td><td><code>dashscope-intl.aliyuncs.com/.../balance</code></td><td>$</td><td>✅</td></tr>
<tr><td>9</td><td><b>百度文心 (ERNIE)</b></td><td><code>aip.baidubce.com/rpc/2.0/billing/balance</code></td><td>¥</td><td>✅</td></tr>
<tr><td>10</td><td><b>MiniMax (海螺AI)</b></td><td><code>api.minimax.chat/v1/wallet/balance</code></td><td>¥</td><td>⚠️</td></tr>
<tr><td>11</td><td><b>百川 (Baichuan)</b></td><td><code>api.baichuan-ai.com/v1/user/balance</code></td><td>¥</td><td>⚠️</td></tr>
<tr><td>12</td><td><b>阶跃星辰 (StepFun)</b></td><td><code>api.stepfun.com/v1/user/balance</code></td><td>¥</td><td>⚠️</td></tr>
<tr><td>13</td><td><b>零一万物 (Yi)</b></td><td><code>api.lingyiwanwu.com/v1/user/balance</code></td><td>¥</td><td>⚠️</td></tr>
<tr><td>14</td><td><b>腾讯混元</b></td><td><code>api.hunyuan.cloud.tencent.com/...</code></td><td>¥</td><td>⚠️</td></tr>
<tr><td>15</td><td><b>讯飞星火</b></td><td><code>spark-api.xf-yun.com/v1/private/balance</code></td><td>¥</td><td>⚠️</td></tr>
<tr><td>16</td><td><b>豆包 (火山引擎)</b></td><td><code>open.volcengineapi.com/.../list_bill</code></td><td>¥</td><td>⚠️</td></tr>
<tr><td>17</td><td><b>OpenRouter</b></td><td><code>openrouter.ai/api/v1/auth/key</code></td><td>$</td><td>✅</td></tr>
<tr><td>18</td><td><b>Groq</b></td><td><code>api.groq.com/.../dashboard/billing/usage</code></td><td>$</td><td>✅</td></tr>
<tr><td>19</td><td><b>Together AI</b></td><td><code>api.together.xyz/v1/user/credits</code></td><td>$</td><td>✅</td></tr>
<tr><td>20</td><td><b>OpenAI</b></td><td><code>api.openai.com/.../billing/credit_grants</code></td><td>$</td><td>✅</td></tr>
<tr><td>21</td><td><b>Anthropic (Claude)</b></td><td><code>api.anthropic.com/v1/organizations</code></td><td>$</td><td>—</td></tr>
<tr><td>22</td><td><b>Google Gemini</b></td><td><i>no balance API</i></td><td>$</td><td>—</td></tr>
<tr><td>23</td><td><b>xAI (Grok)</b></td><td><i>no balance API</i></td><td>$</td><td>—</td></tr>
<tr><td>24</td><td><b>Mistral AI</b></td><td><code>api.mistral.ai/v1/users/me</code></td><td>$</td><td>⚠️</td></tr>
<tr><td>25</td><td><b>Perplexity</b></td><td><i>no balance API</i></td><td>$</td><td>—</td></tr>
<tr><td>26</td><td><b>Cohere</b></td><td><code>api.cohere.ai/v1/account/balance</code></td><td>$</td><td>✅</td></tr>
<tr><td>27</td><td><b>Replicate</b></td><td><code>api.replicate.com/v1/account</code></td><td>$</td><td>✅</td></tr>
<tr><td>28</td><td><b>HuggingFace</b></td><td><code>huggingface.co/api/whoami</code></td><td>$</td><td>✅</td></tr>
<tr><td>29</td><td><b>Fireworks AI</b></td><td><code>api.fireworks.ai/v1/user/balance</code></td><td>$</td><td>⚠️</td></tr>
</table>

> ✅ = confirmed endpoint exists · ⚠️ = endpoint guessed, may need `ep <n> <url>` to set · — = no balance API available

> ✅ = endpoint 已验证 · ⚠️ = endpoint 为推测，可能需要 `ep <编号> <链接>` 手动设置 · — = 该厂商无余额 API

<br>

# ⚡ Quick Start / 快速开始

<table>
<tr>
<td width="50%">

### Install / 安装

```
1. Download OpenBalance.dmg
2. Open it → drag to Applications
3. Right-click → Open (first time)
```

👇 Then click **💰 ⚙** in the menu bar

</td>
<td width="50%">

### Set API Key / 设置密钥

```bash
security add-generic-password \
  -a 'openbalance-deepseek' \
  -s 'com.openbalance.deepseek' \
  -w 'sk-your-key-here' \
  -U
```

👇 Then type `1` in Configure to toggle DeepSeek on

</td>
</tr>
</table>

<br>

# ⌨️ Commands / 命令参考

<p align="center">
  Open the menu bar → <b>⚙ 配置</b> → type one of:
</p>
<p align="center">
  打开菜单栏 → <b>⚙ 配置</b> → 输入以下命令:
</p>

| Command / 命令 | Example / 示例 | Description / 说明 |
|---|---|---|
| `<number>` | `3` | Toggle provider on/off · 开关 provider |
| `key <n> <secret>` | `key 1 sk-xxx` | Store API key · 存入钥匙串 |
| `remove <n>` | `remove 1` | Delete API key · 删除钥匙串 |
| `ep <n> <url>` | `ep 3 https://...` | Override endpoint · 修改 API 地址 |
| `refresh <sec>` | `refresh 600` | Change interval · 改刷新间隔 |
| `all on / off` | `all on` | Enable/disable all · 全部开/关 |

**Quick example / 快速示例:**

```
1               → enable DeepSeek · 开启 DeepSeek
key 1 sk-xxx    → store key · 存入密钥
17              → also enable OpenRouter · 再开启 OpenRouter
refresh 600     → check every 10min · 每 10 分钟刷新
```

<br>

# 🧹 Uninstall / 卸载

<table>
<tr>
<td width="50%">

### ✅ Method 1: Built-in / 内建卸载 (推荐)

```
1. Click 「💰 ⚙」→ 「🗑 卸载」
2. Confirm → all keys + config wiped
3. Drag OpenBalance.app to Trash
```

</td>
<td width="50%">

### 🔧 Method 2: Manual / 手动清理

```bash
pkill -f "main_script"                # kill process
rm -rf /Applications/OpenBalance.app   # remove app
rm -rf ~/.llm-balance                  # remove config

# Remove all Keychain entries / 删除所有钥匙串条目
for pid in deepseek moonshot-cn moonshot-intl zhipu \
  siliconflow-cn siliconflow-us qwen-cn qwen-intl baidu \
  minimax baichuan stepfun lingyi tencent spark doubao \
  openrouter groq together openai anthropic google xai \
  mistral perplexity cohere replicate hf fireworks; do
  security delete-generic-password \
    -a "openbalance-$pid" -s "com.openbalance.$pid" 2>/dev/null
done
```

</td>
</tr>
</table>

<br>

# 🔧 Architecture / 架构

<table>
<tr>
<td width="50%">

### App Structure / 应用结构

```
OpenBalance.app/
├── Contents/
│   ├── Info.plist
│   ├── MacOS/
│   │   └── OpenBalance    ← C launcher (33KB)
│   └── Resources/
│       ├── main_script.py ← Python app
│       └── applet.icns    ← Icon
```

</td>
<td width="50%">

### Data Storage / 数据存储

| Data / 数据 | Location / 位置 |
|---|---|
| Config / 配置 | `~/.llm-balance/config.json` |
| Custom endpoints / 自定义 endpoint | `~/.llm-balance/endpoints.json` |
| API Keys | macOS Keychain `com.openbalance.*` |
| Debug log / 日志 | `~/.llm-balance/app.log` |

</td>
</tr>
</table>

<br>

# 🔨 Build from Source / 从源码构建

```bash
# Requirements / 前置条件
pip3 install rumps pyobjc Pillow

# Clone / 克隆
git clone https://github.com/Monah-Limited/OpenBalance.git
cd OpenBalance

# Build launcher / 编译启动器
clang -O2 -o OpenBalance.app/Contents/MacOS/OpenBalance scripts/launcher.c

# Sign ad-hoc / 签名
codesign --force --deep --sign - OpenBalance.app

# Package DMG / 打包
mkdir -p /tmp/dmg-src
cp -R OpenBalance.app /tmp/dmg-src/
ln -s /Applications /tmp/dmg-src/Applications
hdiutil create -volname "OpenBalance" -srcfolder /tmp/dmg-src \
  -ov -format UDZO -fs HFS+ OpenBalance.dmg
```

<br>

# 📄 License / 许可证

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT"></a>
</p>

<p align="center">
  MIT — Free to use, modify, and distribute.<br>
  MIT 许可证 — 自由使用、修改、分发。
</p>

<br>

<hr>

<p align="center">
  Made with ❤️ by <a href="https://github.com/Monah-Limited">Monah Limited</a>
  <br><br>
  <a href="https://github.com/Monah-Limited/OpenBalance/issues">🐛 Report Bug / 报告问题</a>
  ·
  <a href="https://github.com/Monah-Limited/OpenBalance/pulls">✨ Feature Request / 功能建议</a>
  ·
  <a href="https://github.com/orgs/Monah-Limited/projects">📋 Roadmap / 路线图</a>
</p>
