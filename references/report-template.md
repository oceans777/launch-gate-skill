# 上线门禁报告

<!-- 复制本骨架到目标项目。不要把个人机器的绝对路径写进报告。 -->

## 结论

- 报告路径：
- 结论：BLOCKED | READY_WITH_WARNINGS | READY
- production_go_live：true | false
- 目标根目录：
- 技术栈线索：
- 版本：commit 或等价标识；工作区是否干净

结论为 BLOCKED 时在这里列出阻断 ID。READY 不表示已经获准部署。

## 已运行的命令

| 命令 | 退出码 | 日志 |
| --- | --- | --- |
|  |  |  |

没有运行的脚本不要写进通过记录。

## 检查记录

状态只填 pass、fail、not-verified、not-applicable。N/A 档必须是 not-applicable 并写原因。

| id | tier | critical | status | 证据 | 原因或下一步 |
| --- | --- | --- | --- | --- | --- |
| LG-SITE-01 | P0 | yes |  |  |  |
| LG-PROV-01 | P0 | yes |  |  |  |
| LG-BILL-01 | P0 | yes |  |  |  |
| LG-AUTH-01 | P0 | yes |  |  |  |
| LG-SEO-01 | P0 | yes |  |  |  |
| LG-SEC-01 | P0 | yes |  |  |  |
| LG-AUTO-01 | P0 | yes |  |  |  |
| LG-LEGAL-01 | P0 | no |  |  |  |
| LG-GSC-01 | P1 | no |  |  |  |
| LG-IDX-01 | P1 | no |  |  |  |
| LG-ANA-01 | P1 | no |  |  |  |
| LG-CHAT-01 | P1 | no |  |  |  |
| LG-COPY-01 | P1 | no |  |  |  |
| LG-LINK-01 | P1 | no |  |  |  |
| LG-ERR-01 | P1 | no |  |  |  |
| LG-ICON-01 | P1 | no |  |  |  |
| LG-CAC-01 | P1 | no |  |  |  |
| LG-NA-DB-01 | N/A | no | not-applicable |  |  |
| LG-NA-PAY-01 | N/A | no | not-applicable |  |  |
| LG-NA-HOST-01 | N/A | no | not-applicable |  |  |
| LG-NA-GROWTH-01 | N/A | no | not-applicable |  |  |

## 未关闭项

P0 失败与生产上线时未核实的 critical P0 放在阻断。其余未关闭项放在警告。每条写谁来做、做完如何复核。

## 未执行的危险动作

本轮没有部署、没有购买域名、没有开通付费 Cloudflare、没有写入密钥、没有真实扣费。若用户另行授权了其中某一项，单列那一项和它的证据，不要并进门禁结论。
