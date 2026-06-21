#!/usr/bin/env python3
"""
OpenBalance — macOS menu bar app
支持全部主流 LLM 厂商，大陆/海外 endpoint 已预设。
"""

import rumps, subprocess, json, os, threading, urllib.request, urllib.error
import ssl
from datetime import datetime
from Foundation import NSBlockOperation, NSOperationQueue

CONFIG_PATH = os.path.expanduser("~/.llm-balance/config.json")
APP_NAME = "OpenBalance"
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

# ─── All Providers ───────────────────────────────────────────────────────────
# (id, name, endpoint, balance_path, currency, decimals, note)

PROVIDERS = [
    # —— DeepSeek ——
    ("deepseek",      "DeepSeek",            "https://api.deepseek.com/user/balance",
     ["balance"], "¥", 2, "大陆"),

    # —— Kimi/Moonshot ——
    ("moonshot-cn",   "Kimi (月之暗面 大陆)", "https://api.moonshot.cn/v1/users/me/balance",
     ["data","available_balance"], "¥", 2, "国内版"),
    ("moonshot-intl", "Kimi (Moonshot 海外)", "https://api.moonshot.ai/v1/users/me/balance",
     ["data","available_balance"], "$", 2, "国际版"),

    # —— 智谱 ——
    ("zhipu",         "智谱 GLM",            "https://open.bigmodel.cn/api/llm/balance",
     [], "¥", 2, "balance_path 待确认"),

    # —— SiliconFlow ——
    ("siliconflow-cn","SiliconFlow 大陆",      "https://api.siliconflow.cn/v1/user/info",
     [], "¥", 2, "国内版"),
    ("siliconflow-us","SiliconFlow 海外",      "https://api.siliconflow.com/v1/user/info",
     [], "$", 2, "国际版"),

    # —— Qwen/通义千问 ——
    ("qwen-cn",       "通义千问 (Qwen 大陆)", "https://dashscope.aliyuncs.com/api/v1/services/billing/balance",
     [], "¥", 2, "国内版"),
    ("qwen-intl",     "通义千问 (Qwen 海外)", "https://dashscope-intl.aliyuncs.com/api/v1/services/billing/balance",
     [], "$", 2, "国际版"),

    # —— 百度 ——
    ("baidu",         "百度文心 (ERNIE)",     "https://aip.baidubce.com/rpc/2.0/billing/balance",
     [], "¥", 2, "POST + access_token"),

    # —— MiniMax ——
    ("minimax",       "MiniMax (海螺AI)",     "https://api.minimax.chat/v1/wallet/balance",
     [], "¥", 2, "endpoint 待确认"),

    # —— 百川 ——
    ("baichuan",      "百川 (Baichuan)",      "https://api.baichuan-ai.com/v1/user/balance",
     [], "¥", 2, "endpoint 待确认"),

    # —— 阶跃星辰 ——
    ("stepfun",       "阶跃星辰 (StepFun)",   "https://api.stepfun.com/v1/user/balance",
     [], "¥", 2, "endpoint 待确认"),

    # —— 零一万物 ——
    ("lingyi",        "零一万物 (Yi)",        "https://api.lingyiwanwu.com/v1/user/balance",
     [], "¥", 2, "endpoint 待确认"),

    # —— 腾讯混元 ——
    ("tencent",       "腾讯混元",             "https://api.hunyuan.cloud.tencent.com/v1/user/balance",
     [], "¥", 2, "endpoint 待确认"),

    # —— 讯飞星火 ——
    ("spark",         "讯飞星火",             "https://spark-api.xf-yun.com/v1/private/balance",
     [], "¥", 2, "需要签名认证"),

    # —— 豆包/火山引擎 ——
    ("doubao",        "豆包 (火山引擎)",      "https://open.volcengineapi.com/api/v1/billing/list_bill",
     [], "¥", 2, "需火山引擎签名"),

    # —— OpenRouter ——
    ("openrouter",    "OpenRouter",           "https://openrouter.ai/api/v1/auth/key",
     ["data","credits"], "$", 4, ""),

    # —— Groq ——
    ("groq",          "Groq",                 "https://api.groq.com/openai/v1/dashboard/billing/usage",
     [], "$", 4, "usage 数据"),

    # —— Together AI ——
    ("together",      "Together AI",          "https://api.together.xyz/v1/user/credits",
     ["total_credits_before_tax"], "$", 2, ""),

    # —— OpenAI ——
    ("openai",        "OpenAI",               "https://api.openai.com/v1/dashboard/billing/credit_grants",
     [], "$", 2, "后付费，可能无余额"),

    # —— Anthropic ——
    ("anthropic",     "Anthropic (Claude)",   "https://api.anthropic.com/v1/organizations",
     [], "$", 2, "后付费，无余额"),

    # —— Google ——
    ("google",        "Google Gemini",        "",
     [], "$", 2, "无余额 API"),

    # —— xAI ——
    ("xai",           "xAI (Grok)",           "",
     [], "$", 2, "无余额 API"),

    # —— Mistral ——
    ("mistral",       "Mistral AI",           "https://api.mistral.ai/v1/users/me",
     [], "$", 2, "endpoint 待确认"),

    # —— Perplexity ——
    ("perplexity",    "Perplexity",           "",
     [], "$", 2, "Pro 订阅，无余额"),

    # —— Cohere ——
    ("cohere",        "Cohere",               "https://api.cohere.ai/v1/account/balance",
     [], "$", 2, ""),

    # —— Replicate ——
    ("replicate",     "Replicate",            "https://api.replicate.com/v1/account",
     [], "$", 2, ""),

    # —— HuggingFace ——
    ("hf",            "HuggingFace",          "https://huggingface.co/api/whoami",
     [], "$", 2, "无余额"),

    # —— Fireworks ——
    ("fireworks",     "Fireworks AI",         "https://api.fireworks.ai/v1/user/balance",
     [], "$", 2, "endpoint 待确认"),
]

PROVIDER_MAP = {p[0]: p for p in PROVIDERS}

# ─── Keychain ────────────────────────────────────────────────────────────────

def kc_get(pid):
    r = subprocess.run(["security", "find-generic-password",
          "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}", "-w"],
          capture_output=True, text=True, timeout=5)
    return r.stdout.strip() if r.returncode == 0 else None

def kc_set(pid, key):
    subprocess.run(["security", "delete-generic-password",
          "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}"],
          capture_output=True, timeout=5)
    subprocess.run(["security", "add-generic-password",
          "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}",
          "-w", key, "-U"], capture_output=True, timeout=5)

def kc_del(pid):
    subprocess.run(["security", "delete-generic-password",
          "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}"],
          capture_output=True, timeout=5)

# ─── Config ──────────────────────────────────────────────────────────────────

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"enabled": [], "refresh_interval": 300}

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def load_custom_endpoints():
    ep_path = os.path.expanduser("~/.llm-balance/endpoints.json")
    if os.path.exists(ep_path):
        with open(ep_path) as f:
            return json.load(f)
    return {}

def save_custom_endpoints(eps):
    ep_path = os.path.expanduser("~/.llm-balance/endpoints.json")
    with open(ep_path, "w") as f:
        json.dump(eps, f, indent=2)

def get_endpoint(pid):
    """Get current endpoint: custom override > built-in default."""
    custom = load_custom_endpoints()
    if pid in custom:
        return custom[pid]
    p = PROVIDER_MAP.get(pid)
    return p[2] if p else ""

# ─── Fetch ───────────────────────────────────────────────────────────────────

def deep_get(d, path):
    for k in path:
        if isinstance(d, dict): d = d.get(k)
        elif isinstance(d, list) and isinstance(k, int) and k < len(d): d = d[k]
        else: return None
        if d is None: return None
    return d

def fetch_balance(pid, api_key):
    p = PROVIDER_MAP.get(pid)
    if not p:
        return None, "未知 provider"
    url = get_endpoint(pid)
    if not url:
        return None, "无 endpoint"
    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/json")
        ctx = ssl.create_default_context()
        r = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(r.read().decode())
        bp = p[3]
        if bp:
            val = deep_get(data, bp)
            if val is not None:
                return float(val), None
        return None, f"原始响应: {json.dumps(data, ensure_ascii=False)[:150]}"
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:150]
        if e.code in (401, 403): return None, "无效 key"
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"网络: {e.reason}"
    except Exception as e:
        return None, str(e)[:80]

# ─── UI ──────────────────────────────────────────────────────────────────────

def main_thread(fn):
    op = NSBlockOperation.alloc().init()
    op.addExecutionBlock_(fn)
    NSOperationQueue.mainQueue().addOperation_(op)

_UPDATE_TIME = None

class LLMBalanceApp(rumps.App):
    def __init__(self):
        super().__init__(APP_NAME, template=False)
        self.config = load_config()
        self.balances = {}
        self._busy = False
        self._build_menu()
        interval = self.config.get("refresh_interval", 300)
        self.timer = rumps.Timer(self._tick, interval)
        self.timer.start()
        threading.Thread(target=self._refresh, daemon=True).start()

    def _build_menu(self):
        self.menu.clear()
        enabled = self.config.get("enabled", [])
        self.title = self._title_str()

        if not enabled:
            self.menu.add(rumps.MenuItem("❌ 未配置任何 provider"))
            self.menu.add(rumps.separator)

        for pid in enabled:
            p = PROVIDER_MAP.get(pid)
            if not p: continue
            bal, err, _ = self.balances.get(pid, (None, None, None))
            if bal is not None:
                c, d = p[4], p[5]
                label = f"{p[1]}: {c}{bal:.{d}f}"
            elif err:
                label = f"{p[1]}: ⚠ {err[:22]}"
            else:
                label = f"{p[1]}: ⟳"
            item = rumps.MenuItem(label)
            item.set_callback(None)
            self.menu.add(item)

        if enabled:
            self.menu.add(rumps.separator)

        self.menu.add(rumps.MenuItem(f"🕐 {_UPDATE_TIME or '—'}"))
        interval = self.config.get("refresh_interval", 300)
        self.menu.add(rumps.MenuItem(f"⟳ 每 {interval//60} 分钟"))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("🔄 刷新", callback=self._do_refresh))
        self.menu.add(rumps.MenuItem("⚙ 配置", callback=self._do_config))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("🗑 卸载", callback=self._do_uninstall))
        self.menu.add(rumps.MenuItem("退出", callback=rumps.quit_application))

    def _title_str(self):
        enabled = self.config.get("enabled", [])
        vals = []
        for pid in enabled:
            v, _, _ = self.balances.get(pid, (None, None, None))
            if v is not None: vals.append(v)
        if not vals:
            return "💰 余额" if enabled else "💰 ⚙"
        total = sum(vals)
        if len(vals) == 1:
            p = PROVIDER_MAP.get(enabled[0], PROVIDERS[0])
            return f"💰 {p[4]}{total:.{p[5]}f}"
        return f"💰 ${total:.2f}"

    def _tick(self, _):
        if not self._busy:
            threading.Thread(target=self._refresh, daemon=True).start()

    def _refresh(self):
        self._busy = True
        global _UPDATE_TIME
        for pid in self.config.get("enabled", []):
            key = kc_get(pid)
            if not key:
                self.balances[pid] = (None, "未设 key", None)
                continue
            bal, err = fetch_balance(pid, key)
            self.balances[pid] = (bal, err, None)
        _UPDATE_TIME = datetime.now().strftime("%H:%M:%S")
        main_thread(self._build_menu)
        self._busy = False

    def _do_refresh(self, _):
        if not self._busy:
            threading.Thread(target=self._refresh, daemon=True).start()

    def _do_uninstall(self, _):
        """清理所有数据，然后提示拖入废纸篓。"""
        import shutil

        # 确认
        r = rumps.alert(
            title="卸载 OpenBalance",
            message=(
                "将清除以下数据：\n"
                "• 配置文件和日志 (~/.llm-balance/)\n"
                "• 钥匙串中所有 OpenBalance 的 API key\n"
                "• 应用本身 (/Applications/LLMBalance.app)\n\n"
                "确定要卸载吗？"
            ),
            ok="卸载",
            cancel="取消",
        )
        if r != 1:
            return

        # 1. 删除 keychain 条目
        for pid in PROVIDER_MAP:
            kc_del(pid)

        # 2. 删除配置文件目录
        data_dir = os.path.dirname(CONFIG_PATH)
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)

        # 3. 提示用户拖入废纸篓
        rumps.notification(APP_NAME, "数据已清除",
            "请将 /Applications/LLMBalance.app 拖入废纸篓完成卸载。")

        # 4. 退出
        rumps.quit_application()

    def _do_config(self, _):
        enabled = list(self.config.get("enabled", []))

        while True:
            lines = ["── 配置 ──",
                     "编号 = 切换开关",
                     "key <编号> <secret> = 存 key",
                     "ep <编号> <url> = 改 endpoint",
                     "remove <编号> = 删 key",
                     "refresh <秒> = 改间隔",
                     "all on / all off", ""]

            for i, p in enumerate(PROVIDERS, 1):
                pid, name, *_ = p
                mark = "✅" if pid in enabled else "⬜"
                has_key = "🔑" if kc_get(pid) else "  "
                ep = get_endpoint(pid)
                ep_short = ep[:40] + "…" if len(ep) > 40 else ep
                if not ep: ep_short = "(无)"
                note = p[6]
                tip = f"  {note}" if note else ""
                lines.append(f" {i:2d}. {mark}{has_key} {name}{tip}")

            win = rumps.Window(
                title="OpenBalance 配置",
                message="\n".join(lines) + "\n\n输入命令:",
                default_text="",
                ok="确定",
                cancel="取消",
            )
            r = win.run()
            if r.clicked != 1: break
            inp = r.text.strip()
            if not inp: break
            parts = inp.split()
            cmd = parts[0].lower()

            # Toggle number
            if cmd.isdigit():
                idx = int(cmd) - 1
                if 0 <= idx < len(PROVIDERS):
                    pid = PROVIDERS[idx][0]
                    if pid in enabled:
                        enabled.remove(pid)
                    else:
                        enabled.append(pid)
                    self.config["enabled"] = enabled
                    save_config(self.config)
                    main_thread(self._build_menu)
                continue

            # key <num> <secret>
            if cmd == "key" and len(parts) >= 3 and parts[1].isdigit():
                idx = int(parts[1]) - 1
                if 0 <= idx < len(PROVIDERS):
                    pid = PROVIDERS[idx][0]
                    kc_set(pid, " ".join(parts[2:]))
                    rumps.notification(APP_NAME, "Key 已保存", PROVIDERS[idx][1])
                continue

            # ep <num> <url> — 修改 endpoint
            if cmd == "ep" and len(parts) >= 3 and parts[1].isdigit():
                idx = int(parts[1]) - 1
                if 0 <= idx < len(PROVIDERS):
                    pid = PROVIDERS[idx][0]
                    url = " ".join(parts[2:])
                    custom = load_custom_endpoints()
                    custom[pid] = url
                    save_custom_endpoints(custom)
                    rumps.notification(APP_NAME, "Endpoint 已更新", PROVIDERS[idx][1])
                continue

            # remove <num>
            if cmd == "remove" and len(parts) >= 2 and parts[1].isdigit():
                idx = int(parts[1]) - 1
                if 0 <= idx < len(PROVIDERS):
                    pid = PROVIDERS[idx][0]
                    kc_del(pid)
                    rumps.notification(APP_NAME, "Key 已删除", PROVIDERS[idx][1])
                continue

            # refresh <sec>
            if cmd == "refresh" and len(parts) >= 2:
                try:
                    sec = int(parts[1])
                    self.config["refresh_interval"] = sec
                    save_config(self.config)
                    self.timer.stop()
                    self.timer = rumps.Timer(self._tick, sec)
                    self.timer.start()
                    rumps.notification(APP_NAME, "已更新", f"每 {sec//60} 分钟")
                except ValueError: pass
                continue

            # all on/off
            if cmd == "all" and len(parts) >= 2:
                if parts[1].lower() == "on": enabled = [p[0] for p in PROVIDERS]
                elif parts[1].lower() == "off": enabled = []
                self.config["enabled"] = enabled
                save_config(self.config)
                main_thread(self._build_menu)
                continue

            rumps.alert(title="帮助", message=(
                "编号         切换启用/停用\n"
                "key <n> <s>  存 API key\n"
                "ep <n> <url> 改 endpoint\n"
                "remove <n>   删 key\n"
                "refresh <s>  改刷新间隔\n"
                "all on/off   全部开/关\n\n"
                "示例:\n"
                "  3             切换智谱\n"
                "  key 1 sk-xxx  存 DeepSeek key\n"
                "  ep 2 https://xxx  改 Moonshot 海外 endpoint"
            ))


if __name__ == "__main__":
    LLMBalanceApp().run()
