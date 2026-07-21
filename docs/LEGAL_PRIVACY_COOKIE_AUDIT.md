# 网站法律信息、隐私与 Cookie 审计

更新日期：2026-07-21

本审计基于以下资料与代码：

- `docs/extracted/acoeurs-presentation.txt`
- `docs/extracted/enterprise-service-toolkit.txt`
- `docs/PDF_CONTENT_AUDIT.md`
- `config/settings.py`
- `config/urls.py`
- `website/models.py`
- `website/views.py`
- `website/urls.py`
- `website/admin.py`
- `templates/base.html`
- `templates/includes/header.html`
- `templates/includes/footer.html`
- `templates/website/placeholder.html`
- `static/js/main.js`
- `requirements.txt`
- `render.yaml`
- `build.sh`

说明：

- 本轮未修改任何网站代码。
- `website/forms.py` 当前不存在。
- `.env.example` 当前不存在。
- 本报告只记录代码和资料中**已确认**的信息；不能确认的内容统一标记为“待用户确认”。

## 1. 公司与网站主体信息审计

### 1.1 当前可以确认的信息

#### 品牌名称

- `Acoeurs Consulting`
- 中文品牌展示：`艾克斯咨询`

来源：

- `docs/extracted/acoeurs-presentation.txt`
- `templates/includes/footer.html`
- `templates/includes/header.html`

#### 当前展示的公司名称

代码和资料里出现了两类写法：

- `Acoeurs Consulting 艾克斯咨询`
- `艾克斯咨询有限公司`

来源：

- Footer：`Acoeurs Consulting 艾克斯咨询`
- 宣发 PDF 第 1、10 页：`艾克斯咨询有限公司`

结论：

- 当前**品牌展示名称**明确；
- 但**官网应公开的法定主体全称**仍需用户确认。

#### 当前网站域名

- `acoeursconsulting.com`
- `www.acoeursconsulting.com`
- 代码中还预留了：
  - `staging.acoeursconsulting.com`

来源：

- `README.md`
- `config/settings.py`
- `render.yaml`
- Footer 文本 `www.acoeursconsulting.com`

#### 邮箱

- `contact@acoeursconsulting.com`

来源：

- Footer
- 宣发 PDF 联系方式

#### 电话

- 中国热线：`400-606-0685`
- 法国电话：`+33 (0)9 72 96 05 73`

来源：

- Footer
- 宣发 PDF 联系方式

#### 地址

当前代码中只明确看到：

- 巴黎地址：`32 AV. Kléber 75116 Paris`

来源：

- `templates/includes/footer.html`

注意：

- PDF 只提到办公地点“巴黎 / 上海 / 香港”，未给出完整地址。
- 上海、香港地址在当前代码中未出现。

#### 当前 Footer 中的公司信息

- 品牌：`Acoeurs Consulting 艾克斯咨询`
- 标语：`您在法国及欧洲市场的战略与执行伙伴`
- 电话、邮箱、巴黎地址、网站域名

#### 当前部署平台 / 托管方式

可以确认：

- 应用部署平台：`Render`
- Web 服务运行：`Gunicorn`
- 静态文件处理：`WhiteNoise`
- 数据库：本地开发默认 `SQLite`，生产按配置为 `Render PostgreSQL`

来源：

- `README.md`
- `render.yaml`
- `config/settings.py`
- `requirements.txt`
- `build.sh`

#### 当前域名或 DNS 服务商

- **待用户确认**

代码中只能确认：

- 预期生产域名与 staging 子域名
- 没有找到 Cloudflare、Route53、阿里云 DNS、腾讯云 DNS、Gandi 等明确配置

#### 当前网站内容发布主体

- **待用户确认**

目前只能确认品牌展示主体为：

- `Acoeurs Consulting / 艾克斯咨询`

但不能仅凭品牌名称推定法律上的 publication/publisher 主体。

### 1.2 法律声明仍缺少的关键信息

以下项目当前代码和资料都无法完整确认，建议上线前由用户/法务补齐：

- 完整法定公司名称
- 法律形式（如 SAS / SARL / Ltd / 有限公司等）
- 注册资本
- SIREN
- SIRET
- RCS 所在城市与号码
- 法国 TVA 号码
- publication director / directeur de la publication
- 托管商完整名称
- 托管商地址
- 托管商电话
- 网站内容与知识产权主体
- 适用的受监管活动与牌照信息（如有）

## 2. 网站数据收集与处理审计

## 2.1 当前是否存在公开数据收集功能

### 联系表单 / 咨询表单

- 当前不存在已实现的公开表单
- `/consultation/` 仍是占位页
- 模板中没有 `form`、`method="post"`、`csrf_token`、`textarea`、`email` 输入框

来源：

- `website/urls.py`
- `templates/website/placeholder.html`
- 全模板搜索

结论：

- 当前公开站点**不收集咨询表单数据**

### 用户账户

- 没有面向公众的注册、登录、个人账户功能
- 但存在 Django admin 路由：`/admin/`

来源：

- `config/urls.py`

结论：

- 公开站点无用户账户
- 后台存在管理员/员工账户体系（Django admin）

### Django Admin 数据

- admin 已启用：`django.contrib.admin`
- 后台登录页存在
- 后台使用 Django 默认认证、Session、CSRF 机制

结论：

- 若后台被实际使用，将处理管理员账户相关数据与登录元数据

### 邮箱、电话、公司名称、留言内容

- 当前页面只展示联系邮箱和电话
- 没有公开表单，因此不会通过网站前端采集这些字段

### IP 地址 / User-Agent / 服务器日志

代码层面可以合理确认：

- 任何 HTTP 请求都会在 Django / Gunicorn / Render 基础设施层产生访问日志可能性
- 代码中没有自定义日志处理器、没有自建访客画像、没有错误监控 SDK

结论：

- **存在服务器层面的访问日志可能**
- 可能包含：
  - IP 地址
  - User-Agent
  - 请求路径
  - 时间戳
  - 状态码
- 具体日志保留时间：**待用户确认 / 待托管平台确认**

### Session

- 已启用 `SessionMiddleware`
- 当前公开页面访问测试中：
  - `/`
  - `/about/`
  - `/consultation/`
  都**未实际下发 `sessionid` Cookie**

结论：

- Session 机制已启用
- 但当前匿名公开浏览路径下**未观察到 session cookie 实际落地**
- 若将来使用 admin 登录、消息机制、登录态或表单工作流，`sessionid` 可能出现

### CSRF

- 已启用 `CsrfViewMiddleware`
- 公开页面当前未观察到 `csrftoken` Cookie
- `/admin/login/` GET 时实际下发：
  - `csrftoken`
  - `SameSite=Lax`
  - `Max-Age=31449600`（约 1 年）

结论：

- CSRF 保护机制已启用
- 但当前公开营销页访问时不一定下发
- 后台登录页已真实下发 `csrftoken`

### 语言偏好

- Django 默认 `LANGUAGE_CODE='zh-hans'`
- `LocaleMiddleware` 未启用
- 未观察到 `django_language` Cookie

结论：

- 当前没有语言偏好 Cookie 的实际使用

### Analytics / 错误监控 / 外部嵌入 / 营销工具

经代码检索，当前未发现：

- Google Analytics / gtag / GA4
- Plausible
- Matomo
- Sentry
- Hotjar / Clarity
- Google Maps
- YouTube / Vimeo
- 社交媒体嵌入
- 聊天工具
- 邮件营销脚本
- CRM 脚本
- 第三方字体或第三方图片

结论：

- 当前无公开前端追踪、统计、营销或嵌入式第三方脚本

### 外部字体 / 外部图片 / CDN

- 字体使用本地系统字体栈
- 图片均来自 `static/images/`
- JS / CSS 均本地静态资源
- 未发现外部 CDN URL

### Cloudflare

- 代码中未发现 Cloudflare 配置
- **待用户确认**

### Render

- 可确认在 `render.yaml` 中配置为部署平台

### 数据库托管

- 本地开发：SQLite
- 生产：通过 `DATABASE_URL` 指向 PostgreSQL，且 `render.yaml` 中绑定 Render 数据库

### 备份

- 代码中未发现备份策略
- Render 数据库是否启用自动备份：**待用户确认 / 待平台配置确认**

## 2.2 数据收集矩阵

| 项目 | 是否存在 | 发现位置 | 数据内容 | 目的 | 是否第三方 | 是否可能欧盟外传输 | 保留期限 | 是否需同意 | 是否应写入隐私政策 |
|---|---|---|---|---|---|---|---|---|---|
| 公开咨询表单 | 否 | `/consultation/` 占位页 | 无 | 无 | 否 | 否 | 不适用 | 否 | 需说明“当前无表单，未来上线后补充” |
| 邮箱/电话展示 | 是 | Footer / PDF | 联系方式展示 | 商业联系 | 否 | 否 | 不适用 | 否 | 是 |
| 管理后台登录 | 是 | `/admin/` | 管理员账户、登录元数据 | 后台管理 | 否（代码层） | 可能，经托管平台 | 待确认 | 否 | 是 |
| 服务器访问日志 | 可能存在 | Gunicorn / Render 部署 | IP、UA、路径、时间、状态码 | 安全、运维、排错 | 是，托管平台 | 可能 | 待确认 | 通常否 | 是 |
| Session 机制 | 已启用但公开页未观察到 | `SessionMiddleware` | session 标识符 | 登录态/会话管理 | 否 | 可能，经托管平台 | 默认 2 周（若发出） | 严格必要，不需同意 | 是 |
| CSRF 机制 | 是 | `CsrfViewMiddleware` / admin login | `csrftoken` | 表单安全 | 否 | 可能，经托管平台 | 约 1 年 | 严格必要，不需同意 | 是 |
| 语言偏好 | 未实际使用 | 默认 Django 设置 | 理论上为语言代码 | 语言切换 | 否 | 否 | 不适用 | 一般不需 | 可选说明 |
| Analytics | 否 | 全局搜索未发现 | 无 | 无 | 无 | 无 | 不适用 | 不适用 | 可明确说明未使用 |
| 错误监控 | 否 | 全局搜索未发现 | 无 | 无 | 无 | 无 | 不适用 | 不适用 | 可明确说明未使用 |
| 外部嵌入 | 否 | 模板搜索未发现 | 无 | 无 | 无 | 无 | 不适用 | 不适用 | 可明确说明未使用 |

## 3. Cookie 与本地存储审计

## 3.1 当前已识别的 Cookie / 存储项

### 1) `csrftoken`

- 来源：Django CSRF 中间件
- 配置来源：`config/settings.py`
- 默认名：`csrftoken`
- 默认期限：`31449600` 秒（约 1 年）
- 观察结果：
  - 首页 `/`：未观察到
  - `/about/`：未观察到
  - `/consultation/`：未观察到
  - `/admin/login/`：**实际观察到**
- 目的：
  - 防止跨站请求伪造
- 类型：
  - 第一方 Cookie
- 是否严格必要：
  - 是
- 是否需事先同意：
  - 否

### 2) `sessionid`

- 来源：Django Session 中间件
- 配置来源：`config/settings.py`
- 默认名：`sessionid`
- 默认期限：`1209600` 秒（约 2 周）
- 观察结果：
  - 当前公开页面和 admin 登录页 GET 访问未观察到
- 目的：
  - 登录态 / 会话管理 / 消息机制
- 类型：
  - 第一方 Cookie
- 是否严格必要：
  - 若实际使用，则是
- 是否需事先同意：
  - 否

结论：

- `sessionid` 当前是**可能使用但未在匿名公开访问中实际下发**的必要 Cookie。

### 3) `django_language`

- 来源：Django 默认语言 Cookie 机制
- 默认名：`django_language`
- 观察结果：
  - 当前未发现 `LocaleMiddleware`
  - 未观察到该 Cookie
- 结论：
  - 当前未实际使用

### 4) Consent / Analytics / Third-party Cookies

- 未发现任何：
  - consent cookie
  - analytics cookie
  - 第三方跟踪 cookie

### 5) `localStorage` / `sessionStorage`

- 全局搜索未发现使用

### 6) 其他 JS 追踪标识

- 未发现使用

## 3.2 Cookie Banner 判断

### 当前结论

当前公开站点可合理归类为：

- **只使用严格必要或潜在严格必要技术机制**
- 且公开匿名页面当前**没有观察到任何非必要 Cookie 实际下发**

因此：

- **当前可以不展示 Cookie 同意 Banner**
- 但仍建议上线正式的 Cookie 政策页面，说明：
  - 站点使用哪些严格必要技术 Cookie
  - 公开页面当前未使用统计/广告类 cookie
  - admin 或未来表单功能可能触发必要 cookie

### 何时需要 Banner

如果未来新增以下任一功能，则通常需要在同意前阻止：

- Google Analytics / GA4
- Plausible（如果配置跨站识别或 cookie）
- Matomo（非严格必要配置）
- Meta Pixel / LinkedIn Insight / Ads
- YouTube / Vimeo 嵌入
- 地图、聊天、营销自动化、第三方 CRM
- A/B 测试或行为分析工具

当前项目中：

- 未发现接受/拒绝/设置类同意管理逻辑
- 未发现 consent storage 或 banner 逻辑

## 4. 隐私政策当前应覆盖的内容

基于现有站点，隐私政策至少应覆盖以下内容：

### 当前已可写入的内容

- 数据控制者：**待用户确认法定主体**
- 联系邮箱：当前至少可写 `contact@acoeursconsulting.com`
- 网站收集的数据类别：
  - 服务器访问日志中可能出现的技术数据
  - 管理后台使用时的认证与安全数据
  - 联系信息展示而非前端收集
- 数据来源：
  - 用户访问网站时自动生成的技术信息
  - 管理后台操作过程中的认证信息
- 处理目的：
  - 网站运行
  - 安全防护
  - 运维和排错
- 法律依据：
  - 网站安全与运行的合法利益
  - 管理后台认证和访问控制的必要性
- 接收方：
  - 网站托管与数据库提供方（Render）
- Cookie 和追踪器说明：
  - 严格必要 cookie
  - 当前无统计或营销 cookie
- 用户权利：
  - 访问、更正、删除、限制、反对、投诉等
- CNIL 投诉权
- 政策更新日期

### 目前无法确认、需补充的内容

- 精确的数据控制者法定信息
- 专门的隐私联系邮箱
- 具体日志保留期限
- 管理后台账号和日志保留期限
- 托管商的完整法定信息和地址
- 是否存在欧盟外存储/子处理链的合同安排
- 备份保留策略
- 实际内部访问权限管理方式

### 不应编造的内容

- 银行级加密
- 军工级安全
- 绝对保密
- 特定认证（ISO、SOC2 等）
- DPO
- 固定欧盟境内存储承诺

## 5. 未来咨询表单上线的影响

如果未来在 `/consultation/` 加入咨询表单，隐私政策至少需要新增：

### 需补充的数据类别

- 姓名
- 邮箱
- 电话
- 公司名称
- 职位（如有）
- 咨询内容 / 留言内容
- 提交时间
- 可能的 IP / 反垃圾信息

### 表单附近需要显示的第一层信息

建议至少说明：

- 数据控制者是谁
- 目的：处理咨询请求、后续联系
- 法律依据：应请求采取缔约前措施或合法利益
- 主要接收方：内部团队 / 邮件服务 / 托管系统（如适用）
- 保留期限：待用户确认
- 用户权利入口：隐私政策链接

### 哪些字段应避免收集

默认应避免：

- 护照号
- 身份证号
- 银行卡信息
- 完整税务文件
- 医疗健康信息
- 未成年人敏感信息
- 大体量文件上传

除非：

- 业务上确有必要
- 已有充分的法律基础与安全安排

### 是否需要单独同意

- 如果只是处理用户主动咨询，通常**不需要额外“同意处理”作为唯一法律基础**
- 但若要：
  - 发送营销邮件
  - 分享给额外合作方
  - 收集敏感信息
  - 保存超出合理沟通周期
  则可能需要额外同意或更明确的告知

### 数据库存储、邮件通知和 Admin 访问的影响

如果表单上线并写入数据库或发送邮件，应补充：

- 数据存储位置
- 内部可访问人员
- 是否通过邮件系统转发
- 是否进入 Django Admin 或其他后台
- 保留期限
- 删除流程
- 备份与日志影响

## 6. 三个法律页面当前可完成程度

## 6.1 法律声明

### 当前可以写的内容

- 品牌展示名称
- 网站域名
- 联系邮箱
- 联系电话
- 当前展示的巴黎地址
- 网站托管使用 Render 的事实
- 知识产权保留原则（但权利主体仍需确认）

### 缺少的关键字段

- 法定公司全称
- 法律形式
- 注册资本
- SIREN / SIRET
- RCS
- TVA
- publication director
- 托管商完整法定信息
- 知识产权法定主体

### 是否适合直接上线

- **不建议在上述字段未确认前作为正式法律声明上线**
- 可以先保留占位页，或使用“待补全”的内部草案，但不适合作为正式公开法律声明

## 6.2 隐私政策

### 当前可以写的内容

- 当前无公开咨询表单
- 当前公开页面不使用 analytics / marketing tracker
- 可能存在必要技术 cookie 和服务器日志
- admin 后台存在认证与安全数据处理
- 站点托管在 Render 生态中

### 仍需根据真实技术情况补充

- 数据控制者法定信息
- 日志与后台数据保留期限
- 处理者完整信息
- 跨境传输细节
- 备份与子处理链

### 咨询表单上线后需要更新

- 表单字段
- 法律依据
- 保留期限
- 接收方
- 后台访问和邮件发送逻辑

## 6.3 Cookie 政策

### 当前实际 Cookie 清单

- `csrftoken`
  - 实测仅在 `/admin/login/` 观察到
- `sessionid`
  - 配置支持，但当前公开路径未实测到
- 无 analytics / marketing / third-party cookies

### 当前是否需要 Cookie Banner

- 当前**不需要**
- 前提是继续保持无统计、无营销、无第三方嵌入

### 当前可以写的政策范围

- 严格必要 cookie 的说明
- 当前未使用非必要 cookie 的说明
- 将来若启用统计或嵌入工具将更新政策

### 后续增加统计工具时应如何更新

- 更新 cookie 清单
- 说明目的、类型、期限、提供方
- 实施同意机制
- 在同意前阻止非必要脚本

## 7. 当前第三方服务与可能的欧盟外传输

### 当前可确认的第三方 / 处理者

- Render（Web 托管与数据库平台）
- Gunicorn / WhiteNoise 为技术组件，不是独立外部服务商关系主体

### 未发现的第三方

- Cloudflare
- Google Analytics
- Google Maps
- YouTube / Vimeo
- CRM
- 邮件营销
- 错误监控
- 外部字体服务

### 欧盟外数据传输可能

存在**可能性**，原因包括：

- Render 为美国公司/美国平台生态
- 如果生产环境按 `render.yaml` 部署，访问日志、站点内容与数据库处理可能经过 Render 基础设施

但目前无法仅靠仓库确认：

- 实际部署区域
- 子处理者链条
- SCC / DPA / 数据传输机制

因此应写为：

- **可能发生欧盟外传输，具体安排待用户确认**

## 8. 当前法律页面的上线建议

### 适合立即推进的

- 先起草：
  - 隐私政策
  - Cookie 政策

因为当前技术事实相对明确。

### 不建议直接正式上线的

- 完整法律声明

因为公司法定信息缺失过多。

## 9. 审计结论摘要

### 当前已确认

- 网站公开页目前没有咨询表单
- 没有前端 analytics / marketing tracker
- 没有 localStorage / sessionStorage
- 没有外部图片、外部字体和第三方嵌入
- Render 是明确的托管与数据库平台
- admin 后台存在，admin 登录页实际下发 `csrftoken`

### 当前核心缺口

- 法律主体信息不完整
- 托管商法务信息不完整
- 日志/后台/备份保留期限未确认
- 咨询表单上线后的数据处理方案尚未定义

