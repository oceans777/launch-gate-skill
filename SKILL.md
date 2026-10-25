---
name: launch-gate-skill
description: "当用户说上线门禁、上线前检测、launch gate、go-live check、能不能上线或上线前全部检查时使用。按 P0 阻断、P1 警告、N/A 跳过做分级门禁；「全部」只覆盖 P0。增长、外链、发帖和无关技术栈不得当成部署阻断。默认只检查出报告，不部署、不买域名、不写密钥、不真实扣费。"
---

# 上线门禁

把出海站点的上线检查分成三级，并写出带证据的结论。

- **P0**：生产、付费 Cloudflare 或自定义域名上线前必须通过。失败会阻断。
- **P1**：应该尽快修。不阻断部署。
- **N/A**：技术栈不对或不属于部署门禁。必须写跳过原因。

用户说「上线前全部检查」时，「全部」只表示全部 P0。不要把增长、营销或别的技术栈清单升成阻断项。

## 何时使用

用户表达以下意图时使用本技能：

- 上线门禁
- 上线前检测
- launch gate
- go-live check
- 能不能上线
- 上线前全部检查

只读讨论某个检查项的含义时，直接回答，不要假装已经跑完门禁。

## 默认模式

默认是 **inspect-only / fail-closed report**：只检查、只出报告。调用本技能本身不部署、不购买、不写密钥、不产生真实扣费。

1. 确定目标项目根目录和技术栈线索（例如 Cloudflare Workers、Cloudflare Pages、Next.js、Vercel、静态托管或其他）。根目录不明确时先列出候选并停止，不要扫无关仓库。
2. 项目里已经有的自动化检查才运行，例如 `npm run doctor`、`npm run seo:check`、typecheck、test、build、smoke。命令、退出码和日志路径写入报告。没有该脚本就记 `not-applicable` 或 `not-verified`（见 `references/tiers.md`），不要编造成通过。宿主仓库自己的上线脚本是该仓库的执行器；本技能是跨栈门禁规格，不替代那些脚本。
3. 按 `references/tiers.md` 逐项填写。状态只允许 `pass`、`fail`、`not-verified`、`not-applicable`。
4. 给出结论，规则见下文。可用 `python scripts/gate_verdict.py` 核对，输入格式见脚本说明。脚本和本文不一致时，以本文为准并先改脚本。
5. 不要部署，不要购买域名，不要开通付费 Cloudflare 产品，不要写入密钥，不要发起真实扣费或真实退款。这些动作只有用户在同一轮里另行明确授权时才做，而且不属于本技能的默认结果。
6. 回复时先写报告路径和结论，再写阻断项与警告。

没有命令输出、文件位置或可复核的人工确认，就不能标 `pass`。跳过、没访问权限、只看到 mock，都不是 `pass`。

## 结论

先判断这次是不是在问生产上线。下面任一情况视为要求生产上线：用户问能不能上线、要求上线前检测或上线前全部检查、要求生产发布、绑定自定义域名，或开通付费 Cloudflare。只看预览或测试环境时，在报告里写明 `production_go_live: false`。

| 结论 | 条件 |
| --- | --- |
| `BLOCKED` | 任一 P0 为 `fail`；或本次要求生产上线，且任一 critical P0 为 `not-verified` |
| `READY_WITH_WARNINGS` | 没有形成 `BLOCKED`，并且仍有未关闭项：P1 为 `fail` 或 `not-verified`，或非 critical 的 P0 为 `not-verified`，或不要求生产上线时的 critical P0 `not-verified` |
| `READY` | 每个 P0 都是 `pass` 或带原因的 `not-applicable`，且没有未关闭的 P1 |

`not-applicable` 必须写原因。没有原因时保持 `not-verified`，不要把它当成通过。

P1 的 `fail` 和 `not-verified` 是未关闭警告。P1 的 `pass` 和带原因的 `not-applicable` 算关闭。

`READY` 和 `READY_WITH_WARNINGS` 只表示门禁结论。它们不授权部署、购买或写密钥。

critical 与否以 `references/tiers.md` 的 `critical` 字段为准。当前 critical P0 是站点身份、生产环境不得使用 mock 支付或 mock 生成供应商、所选支付配置、付费登录所需的 OAuth 或 One Tap、robots 与 sitemap 及 noindex、密钥与已有的 doctor 类 fail-closed 脚本、仓库里已经存在的 typecheck、test、build、seo、smoke 脚本。法律链接项是 P0，但不是 critical：查不到适用要求时记 `not-verified`，不要编造法律结论，也不要仅因未核实就阻断。

## 与生成链路检查的关系

付费 AI 图片或视频的生成链路深检（上传、付款、积分、异步任务、交付）另装并运行 [audit-ai-generation-site](https://github.com/oceans777/audit-ai-generation-site)。不要复制或改写它的检查 ID。本技能的 ID 一律使用 `LG-` 前缀。

本技能负责上线与运维门禁：域名与站点身份、搜索控制台、分析、支付是 live 还是 mock、doctor 类 fail-closed、内容地板，以及明确不属于门禁的项。

## 明确不要当成阻断的事项

下列事项保持 N/A，或最多作为 P1 的人工积压。禁止把它们升为 P0：

- Reddit、X 或其他社媒发帖节奏，build-in-public
- 购买外链、目录站提交积压（积压本身是 P1 人工项，不是部署阻断）
- AppSumo、香港银行卡、开户教程
- 项目没用到的数据库或支付商建议，例如用了 D1 还要求 Neon，支付商列表里没有 Creem 还要求接 Creem
- 托管在 Cloudflare Workers 上时的 Vercel 账单技巧

类别怎么落到检查 ID，见 [droidHZ 映射](references/droidhz-mapping.md)。那只是分类对照，不是文章复述，也不是第二份阻断清单。

## 输出

报告骨架使用 [报告模板](references/report-template.md)。放在目标项目已有的文档或临时目录约定下。没有约定时使用 `docs/launch-gate/<YYYY-MM-DD>/report.md`。不要把某个个人机器的绝对路径写进通用步骤。

回复的第一屏只包含：

1. 报告路径
2. 结论：`BLOCKED`、`READY_WITH_WARNINGS` 或 `READY`
3. 若是 `BLOCKED`，列出阻断的检查 ID

然后用简短列表给出未关闭的 P1、未核实项，以及你实际运行过的命令。不要把未运行的检查写成通过。
