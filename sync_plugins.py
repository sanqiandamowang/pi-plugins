#!/usr/bin/env python3
"""
sync_plugins.py — 依据 config.yml 同步 pi agent 插件安装状态

行为:
  1. 解析 config.yml 中声明的插件列表
  2. 读取 pi 当前已安装的包(`pi list`)
  3. 对 enabled=true 且未安装的执行 `pi install`
  4. 对 enabled=false 且已安装的执行 `pi remove`
  5. 未在 config.yml 中声明、但已安装的包:默认不动(打印警告),
     除非加 --purge 选项,则一并卸载(需确认)

用法:
  python3 sync_plugins.py            # 同步(只装/卸 config 中声明的)
  python3 sync_plugins.py --dry-run  # 仅打印将执行的动作,不实际执行
  python3 sync_plugins.py --purge    # 连同未声明的包也卸载(危险)
  python3 sync_plugins.py --yes      # 跳过所有确认提示
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    sys.exit("缺少 PyYAML,请先安装:pip install pyyaml")


CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"


@dataclass
class Plugin:
    name: str          # 形如 npm:pi-subagents
    enabled: bool
    category: str = ""
    desc: str = ""


# ─────────────────────────────── 解析 ──────────────────────────────

def load_config(path: Path) -> list[Plugin]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    plugins: list[Plugin] = []
    for item in data.get("plugins", []):
        plugins.append(Plugin(
            name=item["name"].strip(),
            enabled=bool(item.get("enabled", True)),
            category=item.get("category", ""),
            desc=item.get("desc", ""),
        ))
    return plugins


def run(cmd: list[str]) -> str:
    """运行命令,返回 stdout。失败时抛出。"""
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"命令失败: {' '.join(cmd)}\nstderr: {proc.stderr.strip()}"
        )
    return proc.stdout


def get_installed() -> set[str]:
    """从 `pi list` 输出中解析已安装的包名集合。"""
    if not shutil.which("pi"):
        sys.exit("未找到 pi 命令,请先安装 pi coding agent")

    out = run(["pi", "list"])
    installed: set[str] = set()
    # pi list 输出形如(缩进 2 空格):
    #   User packages:
    #     npm:pi-antigravity
    #       /path/to/...
    for line in out.splitlines():
        m = re.match(r"^\s{2,}(npm:[\S]+)", line)  # 至少缩进 2,但非更深路径
        if m and not line.lstrip().startswith("/"):
            installed.add(m.group(1))
    return installed


# ─────────────────────────────── 动作 ──────────────────────────────

def plan(plugins: list[Plugin], installed: set[str], purge: bool):
    """计算待安装/待卸载/未声明集合。"""
    declared = {p.name for p in plugins}
    to_install = [p for p in plugins if p.enabled and p.name not in installed]
    to_remove = [p for p in plugins if not p.enabled and p.name in installed]
    undeclared = sorted(installed - declared)
    return to_install, to_remove, undeclared


def confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    while True:
        ans = input(f"{prompt} [y/N] ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("", "n", "no"):
            return False


def execute(to_install: list[Plugin], to_remove: list[Plugin],
            undeclared: list[str], purge: bool, assume_yes: bool,
            dry_run: bool):
    """实际执行安装/卸载。"""
    actions: list[tuple[str, list[str]]] = []

    for p in to_install:
        actions.append(("安装", ["pi", "install", p.name]))
    for p in to_remove:
        actions.append(("卸载", ["pi", "remove", p.name]))
    if purge and undeclared:
        for name in undeclared:
            actions.append(("卸载(未声明)", ["pi", "remove", name]))

    if not actions:
        print("✅ 无需操作,已与 config.yml 一致")
        return

    print("\n📋 即将执行:")
    for label, cmd in actions:
        print(f"  [{label}] {' '.join(cmd)}")
    print()

    if dry_run:
        print("🔍 --dry-run 模式,未实际执行")
        return
    if not confirm("确认执行以上操作?", assume_yes):
        print("已取消")
        return

    for label, cmd in actions:
        print(f"▶ {' '.join(cmd)}")
        proc = subprocess.run(cmd)
        if proc.returncode != 0:
            print(f"  ⚠️  失败(exit {proc.returncode}),继续下一项", file=sys.stderr)
        else:
            print("  ✓ 完成")


# ─────────────────────────────── 主流程 ────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="依据 config.yml 同步 pi 插件")
    parser.add_argument("--dry-run", action="store_true", help="只打印动作,不执行")
    parser.add_argument("--purge", action="store_true",
                        help="连同未在 config 声明的包也卸载(危险)")
    parser.add_argument("--yes", "-y", action="store_true", help="跳过确认")
    args = parser.parse_args()

    if not CONFIG_PATH.exists():
        sys.exit(f"找不到配置文件:{CONFIG_PATH}")

    plugins = load_config(CONFIG_PATH)
    print(f"📄 已加载 config.yml:{len(plugins)} 个声明插件")

    print("🔍 读取 pi 已安装包...")
    installed = get_installed()
    print(f"   当前已安装 {len(installed)} 个:{', '.join(sorted(installed)) or '(无)'}")

    to_install, to_remove, undeclared = plan(plugins, installed, args.purge)

    print(f"\n  待安装 {len(to_install)} 个:" + (
        ", ".join(p.name for p in to_install) if to_install else " 无"))
    print(f"  待卸载 {len(to_remove)} 个:" + (
        ", ".join(p.name for p in to_remove) if to_remove else " 无"))

    if undeclared:
        note = "将一并卸载" if args.purge else "保留不动(用 --purge 可卸载)"
        print(f"  ⚠️ 未声明的已装包 {len(undeclared)} 个({note}):"
              + ", ".join(undeclared))

    execute(to_install, to_remove, undeclared, args.purge,
            args.yes, args.dry_run)


if __name__ == "__main__":
    main()
