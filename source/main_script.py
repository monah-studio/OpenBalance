#!/usr/bin/env python3
"""
OpenBalance — macOS menu bar app.
Monitor all your LLM API balances in one click.
"""

import rumps, subprocess, json, os, threading, urllib.request, urllib.error
import ssl
from datetime import datetime
from Foundation import NSBlockOperation, NSOperationQueue

# ─── Constants ───────────────────────────────────────────────────────────────

CONFIG_PATH = os.path.expanduser("~/.llm-balance/config.json")
APP_NAME = "OpenBalance"
APP_VERSION = "1.1.0"
REFRESH_DEFAULT = 300  # 5 min
FETCH_TIMEOUT = 15
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

# ─── All Providers ───────────────────────────────────────────────────────────
# Each entry: (id, display_name, endpoint, balance_path, currency, decimals, note)
# balance_path = [] means path unknown — raw response shown instead

PROVIDERS = [
    # ——— China / 大陆 ———
    ("deepseek",      "DeepSeek",            "https://api.deepseek.com/user/balance",
     ["balance"], "¥", 2, ""),
    ("moonshot-cn",   "Kimi (月之暗面 大陆)", "https://api.moonshot.cn/v1/users/me/balance",
     ["data", "available_balance"], "¥", 2, ""),
    ("zhipu",         "智谱 GLM",            "https://open.bigmodel.cn/api/llm/balance",
     [], "¥", 2, "待确认"),
    ("siliconflow-cn","SiliconFlow 大陆",      "https://api.siliconflow.cn/v1/user/info",
     [], "¥", 2, ""),
    ("qwen-cn",       "通义千问 (Qwen 大陆)", "https://dashscope.aliyuncs.com/api/v1/services/billing/balance",
     [], "¥", 2, ""),
    ("baidu",         "百度文心 (ERNIE)",     "https://aip.baidubce.com/rpc/2.0/billing/balance",
     [], "¥", 2, "POST+access_token"),
    ("minimax",       "MiniMax (海螺AI)",     "https://api.minimax.chat/v1/wallet/balance",
     [], "¥", 2, "待确认"),
    ("baichuan",      "百川 (Baichuan)",      "https://api.baichuan-ai.com/v1/user/balance",
     [], "¥", 2, "待确认"),
    ("stepfun",       "阶跃星辰 (StepFun)",   "https://api.stepfun.com/v1/user/balance",
     [], "¥", 2, "待确认"),
    ("lingyi",        "零一万物 (Yi)",        "https://api.lingyiwanwu.com/v1/user/balance",
     [], "¥", 2, "待确认"),
    ("tencent",       "腾讯混元",             "https://api.hunyuan.cloud.tencent.com/v1/user/balance",
     [], "¥", 2, "待确认"),
    ("spark",         "讯飞星火",             "https://spark-api.xf-yun.com/v1/private/balance",
     [], "¥", 2, "需签名"),
    ("doubao",        "豆包 (火山引擎)",      "https://open.volcengineapi.com/api/v1/billing/list_bill",
     [], "¥", 2, "需签名"),

    # ——— International / 海外 ———
    ("moonshot-intl", "Kimi (Moonshot 海外)", "https://api.moonshot.ai/v1/users/me/balance",
     ["data", "available_balance"], "$", 2, ""),
    ("siliconflow-us","SiliconFlow 海外",      "https://api.siliconflow.com/v1/user/info",
     [], "$", 2, ""),
    ("qwen-intl",     "通义千问 (Qwen 海外)", "https://dashscope-intl.aliyuncs.com/api/v1/services/billing/balance",
     [], "$", 2, ""),
    ("openrouter",    "OpenRouter",           "https://openrouter.ai/api/v1/auth/key",
     ["data", "credits"], "$", 4, ""),
    ("groq",          "Groq",                 "https://api.groq.com/openai/v1/dashboard/billing/usage",
     [], "$", 4, "usage"),
    ("together",      "Together AI",          "https://api.together.xyz/v1/user/credits",
     [], "$", 2, "待确认"),
    ("openai",        "OpenAI",               "https://api.openai.com/v1/dashboard/billing/credit_grants",
     [], "$", 2, "后付费"),
    ("anthropic",     "Anthropic (Claude)",   "https://api.anthropic.com/v1/organizations",
     [], "$", 2, "后付费"),
    ("google",        "Google Gemini",        "",
     [], "$", 2, "无余额 API"),
    ("xai",           "xAI (Grok)",           "",
     [], "$", 2, "无余额 API"),
    ("mistral",       "Mistral AI",           "https://api.mistral.ai/v1/users/me",
     [], "$", 2, "待确认"),
    ("perplexity",    "Perplexity",           "",
     [], "$", 2, "无余额"),
    ("cohere",        "Cohere",               "https://api.cohere.ai/v1/account/balance",
     [], "$", 2, ""),
    ("replicate",     "Replicate",            "https://api.replicate.com/v1/account",
     [], "$", 2, ""),
    ("hf",            "HuggingFace",          "https://huggingface.co/api/whoami",
     [], "$", 2, "无余额"),
    ("fireworks",     "Fireworks AI",         "https://api.fireworks.ai/v1/user/balance",
     [], "$", 2, "待确认"),
]

PROVIDER_MAP = {p[0]: p for p in PROVIDERS}

# ─── Keychain Helpers ────────────────────────────────────────────────────────

def _kc_run(args):
    """Run a security(1) command, ignore errors."""
    subprocess.run(args, capture_output=True, timeout=5)

def kc_get(pid):
    r = subprocess.run(
        ["security", "find-generic-password",
         "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}", "-w"],
        capture_output=True, text=True, timeout=5)
    return r.stdout.strip() if r.returncode == 0 else None

def kc_set(pid, key):
    # Atomically replace: delete (may fail) then add
    _kc_run(["security", "delete-generic-password",
             "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}"])
    _kc_run(["security", "add-generic-password",
             "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}",
             "-w", key, "-U"])

def kc_del(pid):
    _kc_run(["security", "delete-generic-password",
             "-a", f"openbalance-{pid}", "-s", f"com.openbalance.{pid}"])

# ─── Config Helpers ──────────────────────────────────────────────────────────

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"enabled": [], "refresh_interval": REFRESH_DEFAULT}

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def load_custom_endpoints():
    p = os.path.expanduser("~/.llm-balance/endpoints.json")
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}

def save_custom_endpoints(eps):
    p = os.path.expanduser("~/.llm-balance/endpoints.json")
    with open(p, "w") as f:
        json.dump(eps, f, indent=2)

def get_endpoint(pid):
    custom = load_custom_endpoints()
    if pid in custom:
        return custom[pid]
    p = PROVIDER_MAP.get(pid)
    return p[2] if p else ""

# ─── API Fetcher ─────────────────────────────────────────────────────────────

def _deep_get(d, path):
    for k in path:
        if isinstance(d, dict):
            d = d.get(k)
        elif isinstance(d, list) and isinstance(k, int) and k < len(d):
            d = d[k]
        else:
            return None
        if d is None:
            return None
    return d

def fetch_balance(pid, api_key):
    """
    Returns (balance_float, error_string).
    One of them is None on success/failure.
    """
    p = PROVIDER_MAP.get(pid)
    if not p:
        return None, "未知 provider"
    url = get_endpoint(pid)
    if not url:
        return None, "未配置 endpoint"

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", f"OpenBalance/{APP_VERSION}")

        ctx = ssl.create_default_context()
        resp = urllib.request.urlopen(req, timeout=FETCH_TIMEOUT, context=ctx)
        data = json.loads(resp.read().decode())

        bp = p[3]  # balance_path
        if bp:
            val = _deep_get(data, bp)
            if val is not None:
                return float(val), None
        return None, f"解析: {json.dumps(data, ensure_ascii=False)[:150]}"

    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:150]
        if e.code in (401, 403):
            return None, "无效 key"
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"网络: {e.reason}"
    except json.JSONDecodeError:
        return None, "JSON 解析失败"
    except Exception as ex:
        return None, str(ex)[:80]

# ─── UI Threading Helper ─────────────────────────────────────────────────────

def main_thread(fn):
    """Dispatch a block to the main Cocoa thread for UI updates."""
    op = NSBlockOperation.alloc().init()
    op.addExecutionBlock_(fn)
    NSOperationQueue.mainQueue().addOperation_(op)

_UPDATE_TIME = None    # last-refresh timestamp string (written from bg thread)

# ─── Main App Class ──────────────────────────────────────────────────────────

class OpenBalanceApp(rumps.App):
    """macOS menu bar app that shows LLM API balances."""

    def __init__(self):
        super().__init__(APP_NAME, template=False)
        self.config = load_config()
        self.balances = {}          # pid → (value, error, timestamp)
        self._busy = False
        self._build_menu()

        interval = self.config.get("refresh_interval", REFRESH_DEFAULT)
        self._timer = rumps.Timer(self._tick, interval)
        self._timer.start()

        threading.Thread(target=self._refresh, daemon=True).start()

    # ──── Menu bar UI ───────────────────────────────────────────────────────

    def _build_menu(self):
        self.menu.clear()
        enabled = self.config.get("enabled", [])
        self.title = self._title_str()

        if not enabled:
            self.menu.add(rumps.MenuItem("❌ 未配置 provider"))
            self.menu.add(rumps.separator)

        for pid in enabled:
            p = PROVIDER_MAP.get(pid)
            if not p:
                continue
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

        # Status footer
        self.menu.add(rumps.MenuItem(f"🕐 {_UPDATE_TIME or '—'}"))
        interval = self.config.get("refresh_interval", REFRESH_DEFAULT)
        self.menu.add(rumps.MenuItem(f"⟳ 每 {interval // 60} 分钟"))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("🔄 刷新", callback=self._do_refresh))
        self.menu.add(rumps.MenuItem("⚙ 配置", callback=self._do_config))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("🗑 卸载", callback=self._do_uninstall))
        self.menu.add(rumps.MenuItem("退出", callback=rumps.quit_application))

    def _title_str(self):
        """Build the menu bar title string."""
        enabled = self.config.get("enabled", [])
        vals = []
        for pid in enabled:
            v, _, _ = self.balances.get(pid, (None, None, None))
            if v is not None:
                vals.append(v)

        if not vals:
            return "💰 ⚙" if enabled else "💰 ⚙"

        total = sum(vals)

        if len(vals) == 1:
            p = PROVIDER_MAP.get(enabled[0], PROVIDERS[0])
            return f"💰 {p[4]}{total:.{p[5]}f}"

        # Multiple providers — show total in $ but indicate multi
        return f"💰 ${total:.2f}"

    # ──── Timer & Refresh ───────────────────────────────────────────────────

    def _tick(self, _sender):
        if not self._busy:
            threading.Thread(target=self._refresh, daemon=True).start()

    def _refresh(self):
        """Fetch balances for all enabled providers (runs in bg thread)."""
        if self._busy:
            return
        self._busy = True
        global _UPDATE_TIME

        for pid in self.config.get("enabled", []):
            key = kc_get(pid)
            if not key:
                self.balances[pid] = (None, "未设 key", None)
                continue
            try:
                bal, err = fetch_balance(pid, key)
                self.balances[pid] = (bal, err, None)
            except Exception:
                self.balances[pid] = (None, "异常", None)

        _UPDATE_TIME = datetime.now().strftime("%H:%M:%S")
        main_thread(self._build_menu)
        self._busy = False

    def _do_refresh(self, _sender):
        if not self._busy:
            threading.Thread(target=self._refresh, daemon=True).start()

    # ──── Uninstall ─────────────────────────────────────────────────────────

    def _do_uninstall(self, _sender):
        import shutil

        r = rumps.alert(
            title="卸载 OpenBalance",
            message=(
                "将清除以下数据：\n"
                "• 配置文件和日志 (~/.llm-balance/)\n"
                "• 钥匙串中所有 OpenBalance 的 API key\n"
                "• 应用本身 (/Applications/OpenBalance.app)\n\n"
                "确认卸载吗？"
            ),
            ok="卸载",
            cancel="取消",
        )
        if r != 1:
            return

        # 1. Wipe Keychain entries
        for pid in PROVIDER_MAP:
            kc_del(pid)

        # 2. Wipe data directory
        data_dir = os.path.dirname(CONFIG_PATH)
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir, ignore_errors=True)

        # 3. Notify then quit
        rumps.notification(APP_NAME, "数据已清除",
                           "请将 /Applications/OpenBalance.app 拖入废纸篓。")
        rumps.quit_application()

    # ──── Configuration Dialog ───────────────────────────────────────────────

    def _do_config(self, _sender):
        enabled = list(self.config.get("enabled", []))

        while True:
            # Build the provider list — group into chunks to avoid message overflow
            lines = [
                "── OpenBalance 配置 ──",
                "编号=开关 | key <n> <s> | ep <n> <url>",
                "remove <n> | refresh <秒> | all on/off",
                "",
            ]

            for i, p in enumerate(PROVIDERS, 1):
                pid, name, *_ = p
                mark = "✅" if pid in enabled else "⬜"
                has_key = "🔑" if kc_get(pid) else "  "
                note = p[6]
                tip = f"  {note}" if note else ""
                lines.append(f" {i:2}. {mark}{has_key} {name}{tip}")

            win = rumps.Window(
                title="OpenBalance 配置",
                message="\n".join(lines) + "\n\n输入命令:",
                default_text="",
                ok="确定",
                cancel="取消",
            )
            r = win.run()
            if r.clicked != 1:
                break

            inp = r.text.strip()
            if not inp:
                break

            parts = inp.split()
            cmd = parts[0].lower()

            # ── Toggle by number ──
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

            # ── key <num> <secret> ──
            if cmd == "key" and len(parts) >= 3 and parts[1].isdigit():
                idx = int(parts[1]) - 1
                if 0 <= idx < len(PROVIDERS):
                    kc_set(PROVIDERS[idx][0], " ".join(parts[2:]))
                    rumps.notification(APP_NAME, "Key 已保存",
                                       PROVIDERS[idx][1])
                continue

            # ── ep <num> <url> ──
            if cmd == "ep" and len(parts) >= 3 and parts[1].isdigit():
                idx = int(parts[1]) - 1
                if 0 <= idx < len(PROVIDERS):
                    pid = PROVIDERS[idx][0]
                    url = " ".join(parts[2:])
                    custom = load_custom_endpoints()
                    custom[pid] = url
                    save_custom_endpoints(custom)
                    rumps.notification(APP_NAME, "Endpoint 已更新",
                                       PROVIDERS[idx][1])
                continue

            # ── remove <num> ──
            if cmd == "remove" and len(parts) >= 2 and parts[1].isdigit():
                idx = int(parts[1]) - 1
                if 0 <= idx < len(PROVIDERS):
                    kc_del(PROVIDERS[idx][0])
                    rumps.notification(APP_NAME, "Key 已删除",
                                       PROVIDERS[idx][1])
                continue

            # ── refresh <seconds> ──
            if cmd == "refresh" and len(parts) >= 2:
                try:
                    sec = int(parts[1])
                    if sec < 10:
                        sec = 10  # minimum 10 seconds
                    self.config["refresh_interval"] = sec
                    save_config(self.config)
                    self._timer.stop()
                    self._timer = rumps.Timer(self._tick, sec)
                    self._timer.start()
                    rumps.notification(APP_NAME, "已更新",
                                       f"每 {sec // 60} 分钟")
                except ValueError:
                    pass
                continue

            # ── all on / all off ──
            if cmd == "all" and len(parts) >= 2:
                if parts[1].lower() == "on":
                    enabled = [p[0] for p in PROVIDERS]
                elif parts[1].lower() == "off":
                    enabled = []
                self.config["enabled"] = enabled
                save_config(self.config)
                main_thread(self._build_menu)
                continue

            # ── Unknown — show help ──
            rumps.alert(title="帮助", message=(
                "编号          切换启用/停用\n"
                "key <n> <s>   存 API key 到钥匙串\n"
                "ep <n> <url>  修改 API endpoint\n"
                "remove <n>    删除 key\n"
                "refresh <s>   改刷新间隔(秒)\n"
                "all on / off  全部开/关\n\n"
                "示例:\n"
                "  1             启用 DeepSeek\n"
                "  key 1 sk-xxx  存 key\n"
                "  ep 2 https://xxx  改 Moonshot 大陆 endpoint"
            ))


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    OpenBalanceApp().run()
