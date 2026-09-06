# Pi Agent 插件管理

依据 [pi-agent插件推荐清单.md](./pi-agent插件推荐清单.md) 管理你的 pi coding agent 插件,通过 `config.yml` 声明期望状态,用 `sync_plugins.py` 一键同步到本机。

## 文件说明

| 文件 | 作用 |
| ------ | ------ |
| `pi-agent插件推荐清单.md` | 插件调研清单(下载量、说明、分类),供挑选参考 |
| `config.yml` | 插件期望状态声明(enabled 控制是否安装) |
| `sync_plugins.py` | 同步脚本:对比 config 与 `pi list` 实际状态,执行安装/卸载 |

## 前置依赖

```bash
# 1. 已安装 pi coding agent(提供 pi 命令)
pi --version

# 2. Python 3.8+ 与 PyYAML
pip install pyyaml
```

## 快速开始

```bash
# 1. 预演:看看会装/卸什么,不实际执行
python3 sync_plugins.py --dry-run

# 2. 实际同步(会二次确认)
python3 sync_plugins.py

# 3. 跳过确认直接执行
python3 sync_plugins.py --yes
```

## 命令选项

| 命令 | 说明 |
| ------ | ------ |
| `python3 sync_plugins.py` | 同步 config 声明的插件,安装缺失、卸载多余 |
| `python3 sync_plugins.py --dry-run` | 仅打印将执行的动作,不实际执行 |
| `python3 sync_plugins.py --yes` / `-y` | 跳过所有确认提示 |
| `python3 sync_plugins.py --purge` | 连同未在 config 声明的已装包也卸载(危险,会单独确认) |

## config.yml 说明

每个插件用 `enabled: true/false` 控制是否安装:

```yaml
plugins:
  - name: "npm:pi-subagents"          # 包名(带 npm: 前缀)
    category: "核心能力增强"            # 分类(仅注释用)
    enabled: true                      # true=应安装并保留;false=应卸载
    desc: "多代理委派 + 脚本化工作流"    # 说明(仅注释用)
```

**开启某个插件**:把对应项的 `enabled` 改为 `true`,再跑一次 `sync_plugins.py`。

**关闭某个插件**:改为 `false`,再跑一次脚本即可卸载。

### 当前状态

**config.yml 声明(12 个)**

| 状态 | 插件 |
|------|------|
| ✅ 启用(7) | pi-subagents、pi-web-access、pi-background-tasks、@juicesharp/rpiv-todo、@juicesharp/rpiv-ask-user-question、pi-lens、@tian.zuo/pi-antigravity |
| ⬜ 关闭(5) | @narumitw/pi-plan-mode、@narumitw/pi-btw、pi-powerline-footer、pi-web-ui、pi-markdown-preview |

**本机实际安装(7 个)**:与上方启用项完全一致(已清理重复的旧版 `pi-antigravity`)。

> ℹ️ `pi-antigravity`(旧版)已卸载,统一用 `@tian.zuo/pi-antigravity`。若日后想换回,把后者 `enabled` 改 `false`,再加回前者并设 `true`。

## 同步规则

脚本对比 **config.yml 声明** 与 **`pi list` 实际安装**,按下表处理:

| 情况 | 行为 |
| ------ | ------ |
| `enabled: true` 且未安装 | 执行 `pi install` |
| `enabled: false` 且已安装 | 执行 `pi remove` |
| 未在 config 声明但已安装 | 默认保留并打印警告;加 `--purge` 才卸载 |

> 💡 `--purge` 设计为保守:只动 config 里声明的包,避免误删你手动装的其它插件。若想把手动装的包也纳入管理,把它加进 `config.yml` 即可。

## 常见操作

```bash
# 只想加一个插件?直接 pi install,再把它加进 config.yml 保持声明同步
pi install npm:pi-markdown-preview

# 更新所有已装插件到最新
pi update --extensions

# 查看当前已装
pi list

# 查看某插件详情
pi list | grep <包名>
```

## 目录结构

```
pi-plugins/
├── README.md                      # 本文件
├── pi-agent插件推荐清单.md         # 调研清单(参考用)
├── config.yml                     # 期望状态声明
└── sync_plugins.py                # 同步脚本
```

## 故障排查

| 问题 | 解决 |
| ------ | ------ |
| `未找到 pi 命令` | 未安装 pi,参考 [pi 官方文档](https://pi.dev) |
| `缺少 PyYAML` | `pip install pyyaml` |
| `pi install 失败` | 多为网络问题,检查 npm registry 或代理;重试即可,已装的不会重复装 |
| `pi list 解析不到包` | 确认 settings.json 的 `packages` 字段格式正确 |
| 想完全重置 | `python3 sync_plugins.py --purge --yes` 卸载全部声明包 |

## ⚠️ 安全提示

Pi 包拥有完整系统权限,扩展可执行任意代码。安装第三方包前请审查源码。本仓库只列出包名,不负责其内容安全。
