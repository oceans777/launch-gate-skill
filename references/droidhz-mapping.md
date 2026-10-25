# 分类映射

公开文章《出海一周年，稳定万刀，网站出海内容整理》（droidHZ，@hezhiyan7）用这些类别整理出海经验：需求挖掘、SEO、开发、数据分析、支付、流量、外链、产品、部署、复盘。

本文件只做类别到检查 ID 的映射，方便门禁时不漏 P0、也不把经验帖整篇当成阻断清单。它不复述文章正文，不采纳其中的具体渠道做法作为必须执行的步骤。

| 类别 | 落到本技能 | 为什么是这个级别 |
| --- | --- | --- |
| 需求挖掘 | 不单列检查 | 上线前的产品研究，不是部署门禁。没有对应 P0。 |
| SEO | LG-SEO-01 为 P0；LG-GSC-01、LG-IDX-01 为 P1 | 误留 noindex、没有 robots 或 sitemap 方案会挡住公开上线。站长平台验证和 IndexNow 应该做，但没做不阻止部署。 |
| 开发 | LG-AUTH-01、LG-SEC-01、LG-AUTO-01 为 P0；LG-ERR-01 为 P1；LG-NA-DB-01 为 N/A | 登录客户端、密钥、已有的 doctor 和测试脚本失败要阻断。错误上报缺失只警告。Neon 等无关数据库建议不进门禁。 |
| 数据分析 | LG-ANA-01、LG-CAC-01 为 P1 | 分析和 cohort 或获客成本应该补。Clarity 经常缺失，记警告，不阻断。 |
| 支付 | LG-PROV-01、LG-BILL-01 为 P0；LG-NA-PAY-01 为 N/A | 生产却用 mock，或该接的商品和 webhook 没配，要阻断。没选 Creem 就不要把 Creem 当成缺口。生成链路里的入账和积分仍交给 audit-ai-generation-site。 |
| 流量 | LG-NA-GROWTH-01 为 N/A；客服见 LG-CHAT-01（P1） | 发帖节奏、build-in-public、AppSumo、银行卡不是部署条件。客服入口缺失只警告。 |
| 外链 | LG-LINK-01 为 P1 | 目录和外链积压是人工运营。购买链接不在本技能里，也不能升成 P0。 |
| 产品 | LG-LEGAL-01 为非 critical P0；LG-COPY-01、LG-ICON-01、LG-CHAT-01 为 P1 | 项目里已经要求的条款链接缺失要失败。法律适用查不到就保持未核实，不编造。内容地板和图标是警告。 |
| 部署 | LG-SITE-01 为 P0；LG-NA-HOST-01 为 N/A | 占位域名不能当生产。Vercel 账单技巧不是门禁，Workers 项目直接跳过。本技能不购买域名，也不开通付费 Cloudflare。 |
| 复盘 | 不单列检查 | 复盘不是上线开关。生成站点的深检使用 audit-ai-generation-site，不要把复盘清单复制成第二套阻断 ID。 |

若某条经验帖建议与目标仓库的技术栈冲突，以目标仓库为准，并把冲突项记为 `not-applicable`。不要为了对齐文章去更换数据库、支付商或托管。
