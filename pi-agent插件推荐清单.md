# Pi Agent 必装插件推荐清单

> 数据来源:npm 关键词 `pi-package` 检索 + 近一周下载量(2025 年统计)
> 安装命令:`pi install <npm:包名>`

---

## 🔧 核心能力增强

| 插件 | 下载/周 | 说明 |
|------|---------|------|
| **pi-subagents** | 12.2万 | 单代理委派 + 脚本化多代理工作流,支持并行子任务 |
| **pi-web-access** | 13.2万 | 网页搜索、URL 抓取、GitHub 克隆、PDF/YouTube/视频分析(支持 Brave/Tavily/Jina 等多源) |
| **pi-background-tasks** | 2.7万 | 持久后台 shell 任务、只读委派代理,通过子 pi 进程跑工作流 |

## 👀 交互与体验

| 插件 | 下载/周 | 说明 |
|------|---------|------|
| **@juicesharp/rpiv-todo** | 3.7万 | 实时待办清单浮层,跨 `/reload` 和压缩持久化 |
| **@juicesharp/rpiv-ask-user-question** | 4.5万 | 结构化提问,模型不再瞎猜,用选项代替自由文本回复 |
| **@narumitw/pi-plan-mode** | 1万 | Codex 风格只读 `/plan` 协作模式 |
| **@narumitw/pi-btw** | 8千 | `/btw` 旁路提问命令,不打断主流程 |
| **pi-powerline-footer** | 8千 | Powerline 风格状态栏 |

## 🛡️ 安全与代码质量

| 插件 | 下载/周 | 说明 |
|------|---------|------|
| **pi-lens** | 1.9万 | 实时 LSP / linter / formatter / 类型检查反馈 |

## 🌐 集成与扩展

| 插件 | 下载/周 | 说明 |
|------|---------|------|
| **pi-web-ui** | 6.8千 | 一键启动 Web 聊天界面,支持 Docker/systemd 部署 |
| **@tian.zuo/pi-antigravity** | 1.5千 | 接入 Google Antigravity (agy) 模型,通过 agy stream-json RPC,以 pi 作为 UI 使用 Gemini |
| **pi-markdown-preview** | 2.9千 | 渲染 Markdown + LaTeX,支持终端/浏览器/PDF 输出 |

---

## 💡 精简推荐 Top 5(覆盖大多数场景)

1. **pi-subagents** — 多代理并行,复杂任务必备
2. **pi-web-access** — 联网能力,几乎每个项目都用得上
3. **@juicesharp/rpiv-ask-user-question** — 减少模型瞎猜,提升协作质量
4. **pi-lens** — 实时代码反馈,改完立刻知道对不对
5. **@juicesharp/rpiv-todo** — 实时待办浮层,任务跟踪不丢

---

## 📌 安装示例

```bash
# 单个安装
pi install npm:@juicesharp/rpiv-ask-user-question

# 一次性安装 Top 5
pi install npm:pi-subagents
pi install npm:pi-web-access
pi install npm:@juicesharp/rpiv-ask-user-question
pi install npm:pi-lens

# 查看/管理
pi list                 # 已安装的包
pi remove npm:pi-lens   # 卸载
pi update --extensions  # 更新所有包
```

> ⚠️ **安全提示**:Pi 包拥有完整系统权限,扩展可执行任意代码。安装第三方包前请审查源码。
