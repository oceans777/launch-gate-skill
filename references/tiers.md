# 检查表

逐项填写。状态只允许 `pass`、`fail`、`not-verified`、`not-applicable`。

- `pass`：有本轮命令输出、文件位置或可复核的确认。没有证据不能标通过。
- `fail`：查到了不符合项。
- `not-verified`：还没查到，或只有口头说法。
- `not-applicable`：必须写原因。技术栈不符、功能不存在，或该项被规定为非门禁。

P0 的 `critical: yes` 表示：本次要求生产上线时，`not-verified` 也阻断。`critical: no` 的 P0 只有 `fail` 才阻断。P1 的 `fail` 与 `not-verified` 是未关闭警告，不阻断。N/A 档永远 `not-applicable`，禁止升为 P0 或 P1。

不要复用 `audit-ai-generation-site` 的检查 ID。本表 ID 都以 `LG-` 开头。

## LG-SITE-01

- id: LG-SITE-01
- category: 部署
- tier: P0
- critical: yes
- verify: 找出站点规范域名、canonical 和品牌配置。生产配置里不得还是 example.com、example.org、TODO(site)、空的 SITE_URL，或其他占位域名。
- evidence: 配置文件路径和实际非占位域名。不要粘贴密钥。
- pass: 生产所用身份已是真实域名，且文件证据在本轮读到。
- fail: 声称生产、付费 Cloudflare 或自定义域名时，身份仍是占位或为空。
- not-verified: 还没找到站点身份配置。
- not-applicable: 仓库不是对外站点，且用户没有要求站点上线。

## LG-PROV-01

- id: LG-PROV-01
- category: 支付
- tier: P0
- critical: yes
- verify: 若本次声称生产，确认支付和图片或视频供应商没有切在 mock、sandbox 冒充生产，或本地假供应商上。只记录供应商名字和配置位置。
- evidence: 配置或环境来源的路径，以及当前选择的供应商名。不记录密钥值。
- pass: 生产声称下，支付与生成供应商都不是 mock。没有生成供应商时只核对应存在的那一类。
- fail: 生产声称下仍启用 mock 支付或 mock 生成供应商。
- not-verified: 有生产声称，但没找到供应商开关。
- not-applicable: 本次不声称生产，或项目既没有支付也没有生成供应商。

## LG-BILL-01

- id: LG-BILL-01
- category: 支付
- tier: P0
- critical: yes
- verify: 对已经选定的支付商，核对其 live 或 test 商品标识，以及 webhook 路径已经配置。商品标识可以只证明非空、非占位。
- evidence: 支付商名称、商品配置位置、webhook 路径来源。不记录签名密钥。
- pass: 所选支付商的商品与 webhook 路径均已配置，且与当前环境（live 或 test）一致。
- fail: 收费在范围内，但商品缺失、仍是占位，或 webhook 路径缺失。
- not-verified: 还不知道支付商，或没打开过对应配置。
- not-applicable: 用户明确这是上线前的预览，收费不在本次范围。

## LG-AUTH-01

- id: LG-AUTH-01
- category: 开发
- tier: P0
- critical: yes
- verify: 若付费流程需要登录，检查 OAuth 或 One Tap 的客户端标识已经配置且不是占位。不把客户端密钥写进报告。
- evidence: 登录方式、配置文件路径、客户端标识是否非空。
- pass: 付费登录所需的客户端已经配置。
- fail: 付费必须登录，但客户端标识为空或仍是占位。
- not-verified: 还不能判断付费是否需要登录，或没核对客户端配置。
- not-applicable: 付费流程不需要登录，或项目没有登录。

## LG-SEO-01

- id: LG-SEO-01
- category: SEO
- tier: P0
- critical: yes
- verify: 确认生产环境有 robots 与 sitemap 的可达方案，且没有把 noindex 或同等禁止索引指令误留在生产配置、响应头或元标记里。站点还没部署时，核源码和配置，不要为了检查而去部署。
- evidence: robots 与 sitemap 的源码或 URL，以及索引指令的位置。若做了只读请求，记录命令和状态码。
- pass: 索引策略明确允许生产被索引，或有意保持 noindex 且用户确认这次还不是公开上线。robots 与 sitemap 在源码或线上可追溯。
- fail: 生产上线配置仍禁止索引，或公开上线却没有 robots 与 sitemap 方案。
- not-verified: 没读到索引策略。
- not-applicable: 项目不是公开网站，不需要被搜索引擎索引。

## LG-SEC-01

- id: LG-SEC-01
- category: 开发
- tier: P0
- critical: yes
- verify: 确认密钥没有提交进仓库。优先用项目自带的检查；没有的话做保守检索，发现疑似密钥时只记路径，不记值。若仓库有 doctor 或同类 fail-closed 脚本，本轮必须运行。
- evidence: 检索命令或 doctor 命令、退出码、日志路径。doctor 未登录远端时，按脚本自身的离线说明运行，并写明哪些远端项因此未核实。
- pass: 未发现已提交的密钥；存在 doctor 类脚本时，该命令退出码为 0。
- fail: 发现已跟踪的密钥，或 doctor 类脚本失败。
- not-verified: 没做密钥检索，或 doctor 类脚本存在但本轮没运行。
- not-applicable: 不适用整项。没有 doctor 脚本时，只对 doctor 这一半记 not-applicable，密钥检索仍然要做。两项合并时取更差的状态：fail 差于 not-verified，not-verified 差于 pass。

## LG-AUTO-01

- id: LG-AUTO-01
- category: 开发
- tier: P0
- critical: yes
- verify: 查找并运行仓库里已经存在的 typecheck、test、build、seo 或 seo:check、smoke 脚本。不要编造不存在的 npm script。每个实际运行的命令分开记录。
- evidence: 命令、退出码、日志路径。
- pass: 每一个已发现的脚本都在本轮运行且退出码为 0。
- fail: 任一已发现的脚本退出码非 0。
- not-verified: 发现了脚本但本轮没有运行。
- not-applicable: 仓库没有这些脚本。

## LG-LEGAL-01

- id: LG-LEGAL-01
- category: 产品
- tier: P0
- critical: no
- verify: 只核目标项目里已经存在的同意、条款或隐私链接。产品涉及用户上传人像时，记录这些链接是否出现。判断不了适用法规时记 not-verified，不要发明法律义务。
- evidence: 页面、页脚或路由的文件路径。
- pass: 项目自己要求的同意、条款或隐私链接存在且指向有效页面。
- fail: 项目自己的页面或清单要求这些链接，但链接缺失或是空锚点。
- not-verified: 还没找到项目要求，也不能从产品形态判断是否需要。
- not-applicable: 没有用户内容、没有账号，且仓库没有既定的法律页面要求。

## LG-GSC-01

- id: LG-GSC-01
- category: SEO
- tier: P1
- critical: no
- verify: Google Search Console 与 Bing Webmaster 已验证，并且 sitemap 已提交。只有验证元标记不能当成已提交。
- evidence: 用户确认记录，或控制台截图说明的日期与属性。没有控制台权限时不要猜。
- pass: 两个站长平台都已验证，且 sitemap 已提交。
- fail: 已确认至少一处未验证或未提交 sitemap。
- not-verified: 没有控制台权限，也没有用户确认。
- not-applicable: 项目不是公开可索引网站。

## LG-IDX-01

- id: LG-IDX-01
- category: SEO
- tier: P1
- critical: no
- verify: IndexNow 密钥文件是否已配置。线上只读检查时，确认密钥 URL 返回成功且正文与配置一致。报告里不必抄下整段密钥。
- evidence: 配置位置，以及只读请求的状态。未向 IndexNow 提交 URL 不算失败，提交动作需用户另行授权。
- pass: 密钥文件在仓库或线上可核对。
- fail: 项目声明启用了 IndexNow，但密钥文件缺失或不匹配。
- not-verified: 没查找密钥配置。
- not-applicable: 项目明确不使用 IndexNow。

## LG-ANA-01

- id: LG-ANA-01
- category: 数据分析
- tier: P1
- critical: no
- verify: 检查 GA4、Cloudflare Web Analytics、Clarity 三者的配置。Clarity 缺失时记未关闭警告，即使另一项分析已经存在。
- evidence: 配置或片段所在文件。测量 ID 可以记录，密钥类字段不要记录。
- pass: GA4 或 Cloudflare Web Analytics 至少有一项，并且 Clarity 也已配置。
- fail: 已确认没有任何分析工具，或分析工具存在但 Clarity 缺失。
- not-verified: 没查找这些片段。
- not-applicable: 用户明确本轮不做流量分析，且这不是对外营销站的上线验收。

## LG-CHAT-01

- id: LG-CHAT-01
- category: 产品
- tier: P1
- critical: no
- verify: 对外站点是否有客服聊天入口，例如 Crisp 或其他已选定的组件。
- evidence: 组件所在文件或页面位置。
- pass: 已接入选定的客服聊天。
- fail: 对外营销站确认没有客服入口。
- not-verified: 没查找聊天组件。
- not-applicable: 纯接口或内部工具，没有对外支持页面。

## LG-COPY-01

- id: LG-COPY-01
- category: 产品
- tier: P1
- critical: no
- verify: 对照内容地板指引清点现有文章：约 1 篇支柱加 4 到 6 篇配套。这是警告阈值，不是部署阻断，也不为了凑数制造文章。
- evidence: 内容目录路径和篇数。
- pass: 已达到该指引。
- fail: 对外内容站低于该指引。
- not-verified: 没清点内容。
- not-applicable: 产品没有博客或落地内容层。

## LG-LINK-01

- id: LG-LINK-01
- category: 外链
- tier: P1
- critical: no
- verify: 把外链和目录提交的人工积压记成警告。不要购买链接，不要把购买链接写成门禁动作。
- evidence: 现有积压清单的路径，或用户确认还没有清单。
- pass: 积压已列出负责人，且没有把它当成部署阻断。
- fail: 对外上线仍没有任何外链或目录计划。这只是 P1 警告。
- not-verified: 没问到也没找到积压记录。
- not-applicable: 用户把增长运营排除在本轮之外。

## LG-ERR-01

- id: LG-ERR-01
- category: 开发
- tier: P1
- critical: no
- verify: 错误上报是否已配置。Sentry 只核 DSN 是否存在，不把 DSN 写进报告。已有其他错误上报工具时记明工具名。
- evidence: 配置键所在文件，以及值是否非空。
- pass: Sentry 或其他错误上报已配置。
- fail: 确认没有任何错误上报。
- not-verified: 没查找错误上报配置。
- not-applicable: 静态无脚本站点，且没有服务端运行时。

## LG-ICON-01

- id: LG-ICON-01
- category: 产品
- tier: P1
- critical: no
- verify: 除了 SVG 图标外，是否还有 favicon.ico。
- evidence: 公共目录中的文件路径。
- pass: svg 与 favicon.ico 都存在，或项目只有 ico 且页面引用正确。
- fail: 只有 svg，或两者都没有。
- not-verified: 没查看图标文件。
- not-applicable: 没有网页前端。

## LG-CAC-01

- id: LG-CAC-01
- category: 数据分析
- tier: P1
- critical: no
- verify: 是否有 cohort 或获客成本的记录方式。没有工具时记警告，不要临时接一套新分析平台。
- evidence: 看板、表或文档的位置。
- pass: 已有 cohort 或获客成本的记录位置。
- fail: 对外商业站确认没有这类记录。
- not-verified: 没查找。
- not-applicable: 尚未收费，且用户把增长指标排除在本轮之外。

## LG-NA-DB-01

- id: LG-NA-DB-01
- category: 开发
- tier: N/A
- critical: no
- verify: 不要因为数据库选型建议阻断上线。项目使用 D1 或其他库时，Neon 不适用。项目已经使用 Neon 时，也不要把它改写成门禁失败。
- evidence: 实际数据库线索，写进跳过原因即可。
- pass: 本项没有 pass。它不是可通过的门禁。
- fail: 本项没有 fail。禁止因 Neon 或同类选型建议判失败。
- not-verified: 不要把本项留在 not-verified。
- not-applicable: 始终使用。原因写明实际数据存储，或写明这不是部署门禁。

## LG-NA-PAY-01

- id: LG-NA-PAY-01
- category: 支付
- tier: N/A
- critical: no
- verify: Creem 不在项目已选支付商列表中时，不要要求接入 Creem。真正的支付配置走 LG-BILL-01 和 LG-PROV-01。
- evidence: 已选支付商名称，写入跳过原因。
- pass: 本项没有 pass。
- fail: 本项没有 fail。
- not-verified: 不要把本项留在 not-verified。
- not-applicable: 始终使用。未选用 Creem 时写明未选用。已选用时仍保持 not-applicable，并说明收费配置由 LG-BILL-01 覆盖。

## LG-NA-HOST-01

- id: LG-NA-HOST-01
- category: 部署
- tier: N/A
- critical: no
- verify: Vercel 账单技巧不是上线门禁。项目在 Cloudflare Workers 或其他非 Vercel 托管上时更不适用。不要为了这条去改托管。
- evidence: 识别到的托管线索，写入跳过原因。
- pass: 本项没有 pass。
- fail: 本项没有 fail。
- not-verified: 不要把本项留在 not-verified。
- not-applicable: 始终使用。

## LG-NA-GROWTH-01

- id: LG-NA-GROWTH-01
- category: 流量
- tier: N/A
- critical: no
- verify: Reddit 或 X 的发帖节奏、build-in-public、AppSumo、香港银行卡和购买外链都是人工增长或商务事项，不是部署门禁。不要执行这些动作，也不要把它写成 P0。外链积压若需要跟踪，使用 LG-LINK-01，仍然只是 P1。
- evidence: 跳过原因中点名本轮看到的增长建议类别即可，不必展开做法。
- pass: 本项没有 pass。
- fail: 本项没有 fail。
- not-verified: 不要把本项留在 not-verified。
- not-applicable: 始终使用。
