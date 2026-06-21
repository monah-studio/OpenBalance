<div align="center">
  <h1>⚖️ OpenBalance</h1>
  <p><strong>Monitor your LLM API balances from the macOS menu bar</strong></p>
  <p><strong>在菜单栏查看所有 LLM API 余额</strong></p>
  <p>
    <img src="https://img.shields.io/badge/macOS-13%2B-333?logo=apple" alt="macOS">
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs">
  </p>
  <p>
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-supported-providers">Providers</a> •
    <a href="#%EF%B8%8F-commands">Commands</a> •
    <a href="#-uninstall">Uninstall</a> •
    <a href="#-build-from-source">Build</a>
  </p>
</div>

---

## 🌟 Overview

OpenBalance is a lightweight macOS menu bar app that helps you **track API balances across all your LLM providers** at a glance. No more logging into 10 different dashboards to check your credits.

- **🔑 Secure** — API keys stored in macOS Keychain, never written to disk
- **🌏 Bilingual** — Supports both Chinese & international providers (DeepSeek, Kimi, Qwen, OpenRouter, Groq, Anthropic, etc.)
- **⚡ Real-time** — Auto-refresh every 5 minutes (configurable)
- **🧹 Clean uninstall** — Built-in uninstaller clears all data + Keychain entries
- **📦 One DMG** — Drag & drop install, drag to Trash to remove

---

## ⚡ Quick Start

### Install

```
1. Download OpenBalance.dmg
2. Open it → drag OpenBalance.app to Applications
3. Right-click → Open (first time only, Gatekeeper bypass)
4. Click 「💰 ⚙」in the menu bar
```

### Set up your first provider

Open **Terminal** and run:

```bash
# Store your DeepSeek API key in Keychain
security add-generic-password \
  -a 'openbalance-deepseek' \
  -s 'com.openbalance.deepseek' \
  -w 'sk-your-key-here' \
  -U
```

Then click the menu bar icon → **⚙ 配置** → type `1` (toggles DeepSeek on).  
The menu bar now shows `💰 ¥12.34` with your balance.

> 💡 See the [Commands](#%EF%B8%8F-commands) section for all available operations.

---

## 🗺 Supported Providers

31 providers pre-configured with **both China (大陆) and International (海外)** endpoints.

| # | Provider | Endpoint | Currency |
|---|----------|----------|----------|
| 1 | **DeepSeek** | `api.deepseek.com/user/balance` | ¥ |
| 2 | **Kimi (月之暗面 大陆)** | `api.moonshot.cn/v1/users/me/balance` | ¥ |
| 3 | **Kimi (Moonshot 海外)** | `api.moonshot.ai/v1/users/me/balance` | $ |
| 4 | **智谱 GLM** | `open.bigmodel.cn/api/llm/balance` | ¥ |
| 5 | **SiliconFlow 大陆** | `api.siliconflow.cn/v1/user/info` | ¥ |
| 6 | **SiliconFlow 海外** | `api.siliconflow.com/v1/user/info` | $ |
| 7 | **通义千问 (Qwen 大陆)** | `dashscope.aliyuncs.com/api/v1/services/billing/balance` | ¥ |
| 8 | **通义千问 (Qwen 海外)** | `dashscope-intl.aliyuncs.com/api/v1/services/billing/balance` | $ |
| 9 | **百度文心 (ERNIE)** | `aip.baidubce.com/rpc/2.0/billing/balance` | ¥ |
| 10 | **MiniMax (海螺AI)** | `api.minimax.chat/v1/wallet/balance` | ¥ |
| 11 | **百川 (Baichuan)** | `api.baichuan-ai.com/v1/user/balance` | ¥ |
| 12 | **阶跃星辰 (StepFun)** | `api.stepfun.com/v1/user/balance` | ¥ |
| 13 | **零一万物 (Yi)** | `api.lingyiwanwu.com/v1/user/balance` | ¥ |
| 14 | **腾讯混元** | `api.hunyuan.cloud.tencent.com/v1/user/balance` | ¥ |
| 15 | **讯飞星火** | `spark-api.xf-yun.com/v1/private/balance` | ¥ |
| 16 | **豆包 (火山引擎)** | `open.volcengineapi.com/api/v1/billing/list_bill` | ¥ |
| 17 | **OpenRouter** | `openrouter.ai/api/v1/auth/key` | $ |
| 18 | **Groq** | `api.groq.com/openai/v1/dashboard/billing/usage` | $ |
| 19 | **Together AI** | `api.together.xyz/v1/user/credits` | $ |
| 20 | **OpenAI** | `api.openai.com/v1/dashboard/billing/credit_grants` | $ |
| 21 | **Anthropic (Claude)** | `api.anthropic.com/v1/organizations` | $ |
| 22 | **Google Gemini** | _(no balance API)_ | $ |
| 23 | **xAI (Grok)** | _(no balance API)_ | $ |
| 24 | **Mistral AI** | `api.mistral.ai/v1/users/me` | $ |
| 25 | **Perplexity** | _(no balance API)_ | $ |
| 26 | **Cohere** | `api.cohere.ai/v1/account/balance` | $ |
| 27 | **Replicate** | `api.replicate.com/v1/account` | $ |
| 28 | **HuggingFace** | `huggingface.co/api/whoami` | $ |
| 29 | **Fireworks AI** | `api.fireworks.ai/v1/user/balance` | $ |

> ⚠️ Providers marked "待确认" have endpoints that are guessed from API patterns. If the default endpoint doesn't work, use `ep <number> <url>` to set a custom one.

---

## ⌨️ Commands

Open the menu bar → **⚙ 配置**, then type one of:

| Command | Example | Description |
|---------|---------|-------------|
| `<number>` | `3` | Toggle provider on/off |
| `key <n> <secret>` | `key 1 sk-xxx` | Store API key in Keychain |
| `remove <n>` | `remove 1` | Delete API key from Keychain |
| `ep <n> <url>` | `ep 3 https://xxx` | Override endpoint URL |
| `refresh <sec>` | `refresh 600` | Change refresh interval |
| `all on` | `all on` | Enable all providers |
| `all off` | `all off` | Disable all providers |

**Quick start example:**

```
1                    → enable DeepSeek
key 1 sk-abc123      → store DeepSeek key
17                   → also enable OpenRouter
key 17 sk-xyz456     → store OpenRouter key
refresh 600          → check every 10 minutes
```

---

## 🧹 Uninstall

OpenBalance has a **built-in uninstaller** that leaves no trace.

**Method 1 — Via menu bar (recommended):**

```
1. Click 「💰 ⚙」in menu bar
2. Click 「🗑 卸载」
3. Confirm → all data + keys are wiped
4. Drag OpenBalance.app from /Applications to Trash
```

**Method 2 — Manual clean (if app won't launch):**

```bash
# Kill the process
pkill -f "main_script"

# Remove app
rm -rf /Applications/OpenBalance.app

# Remove config
rm -rf ~/.llm-balance

# Remove all Keychain entries
for pid in deepseek moonshot-cn moonshot-intl zhipu siliconflow-cn siliconflow-us qwen-cn qwen-intl baidu minimax baichuan stepfun lingyi tencent spark doubao openrouter groq together openai anthropic google xai mistral perplexity cohere replicate hf fireworks; do
  security delete-generic-password -a "openbalance-$pid" -s "com.openbalance.$pid" 2>/dev/null
done
```

---

## 🔧 Architecture

```
OpenBalance.app/
├── Contents/
│   ├── Info.plist           # Bundle metadata
│   ├── MacOS/
│   │   └── OpenBalance      # Native launcher (compiled C, ~33KB)
│   └── Resources/
│       ├── main_script.py   # Python app (rumps + urllib)
│       └── applet.icns      # App icon
```

**Storage:**

| Data | Location |
|------|----------|
| Config | `~/.llm-balance/config.json` |
| Custom endpoints | `~/.llm-balance/endpoints.json` |
| API keys | macOS Keychain (`com.openbalance.*`) |
| Debug log | `~/.llm-balance/app.log` |

---

## 🔨 Build from Source

```bash
# Requirements
brew install python@3.11
pip3 install rumps pyobjc Pillow

# Clone
git clone https://github.com/your-org/OpenBalance.git
cd OpenBalance

# Build launcher
clang -O2 -o OpenBalance.app/Contents/MacOS/OpenBalance scripts/launcher.c

# Sign (ad-hoc)
codesign --force --deep --sign - OpenBalance.app

# Create DMG
mkdir -p /tmp/dmg-src
cp -R OpenBalance.app /tmp/dmg-src/
ln -s /Applications /tmp/dmg-src/Applications
hdiutil create -volname "OpenBalance" -srcfolder /tmp/dmg-src -ov -format UDZO -fs HFS+ OpenBalance.dmg
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  <p>Made with ❤️ for the LLM community</p>
  <p>
    <a href="https://github.com/your-org/OpenBalance/issues">Report Bug</a> •
    <a href="https://github.com/your-org/OpenBalance/pulls">Feature Request</a>
  </p>
</div>
