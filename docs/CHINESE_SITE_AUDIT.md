# 中文网站全站审计报告

更新日期：2026-07-23

本报告用于中文第一版网站的内部评审准备。本轮重点是确认当前正式页面范围、修复客观问题、整理待评审事项，并为下一阶段反馈收集做准备。

## 一、当前正式页面清单

| 页面 | URL | URL name | 模板 | 专用 CSS | 专用 JS | Header | Footer | 其他 CTA 入口 | sitemap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 首页 | `/` | `home` | `templates/website/home.html` | `static/css/home.css` | 无 | 是 | 是 | 全站 Logo、页脚、多个 CTA | 当前未接入 |
| 企业服务总览 | `/business/` | `business` | `templates/website/enterprise_services.html` | `static/css/services.css` | 无 | 是 | 是 | 首页、关于我们、服务详情返回链接 | 当前未接入 |
| 欧洲市场进入与战略 | `/business/market-entry/` | `business_market_entry` | `templates/website/service_market_entry.html` | `static/css/service-detail.css` | 无 | 否 | 是 | 首页、企业服务总览 | 当前未接入 |
| 公司架构与银行金融 | `/business/company-banking/` | `business_company_banking` | `templates/website/service_company_banking.html` | `static/css/service-detail.css` | 无 | 否 | 是 | 首页、企业服务总览 | 当前未接入 |
| 财税、法律与合规 | `/business/tax-legal-compliance/` | `business_tax_legal_compliance` | `templates/website/service_tax_legal_compliance.html` | `static/css/service-detail.css` | 无 | 否 | 是 | 首页、企业服务总览 | 当前未接入 |
| 本地运营与团队建设 | `/business/local-operations/` | `business_local_operations` | `templates/website/service_local_operations.html` | `static/css/service-detail.css` | 无 | 否 | 是 | 首页、企业服务总览 | 当前未接入 |
| 商务拓展与增长 | `/business/growth/` | `business_growth` | `templates/website/service_business_growth.html` | `static/css/service-detail.css` | 无 | 否 | 是 | 首页、企业服务总览 | 当前未接入 |
| 个人服务总览 | `/personal/` | `personal` | `templates/website/personal_services.html` | `static/css/services.css` | 无 | 是 | 是 | 首页、关于我们 | 当前未接入 |
| 居留与家庭定居 | `/personal/residency-family/` | `personal_residency_family` | `templates/website/service_residency_family.html` | `static/css/service-detail.css` `static/css/personal-service-detail.css` | 无 | 否 | 是 | 个人服务总览 | 当前未接入 |
| 房产与资产配置 | `/personal/property-wealth/` | `personal_property_wealth` | `templates/website/service_property_wealth.html` | `static/css/service-detail.css` `static/css/personal-service-detail.css` | 无 | 否 | 是 | 个人服务总览 | 当前未接入 |
| 跨境税务与风险管理 | `/personal/cross-border-tax-risk/` | `personal_cross_border_tax_risk` | `templates/website/service_cross_border_tax_risk.html` | `static/css/service-detail.css` `static/css/personal-service-detail.css` | 无 | 否 | 是 | 个人服务总览 | 当前未接入 |
| 关于我们 | `/about/` | `about` | `templates/website/about.html` | `static/css/about.css` | 无 | 是 | 是 | 首页、Footer | 当前未接入 |
| 联系我们 | `/contact/` | `contact` | `templates/website/contact.html` | `static/css/contact.css` | `static/js/contact.js` | 按钮入口 | 是 | 首页、服务页、关于我们、总览页 | 当前未接入 |
| 法律声明 | `/legal/` | `legal` | `templates/website/legal_notice.html` | `static/css/legal.css` | 无 | 否 | 是 | Footer、法律页互链 | 当前未接入 |
| 隐私政策 | `/privacy/` | `privacy` | `templates/website/privacy_policy.html` | `static/css/legal.css` | 无 | 否 | 是 | Footer、法律页互链、联系表单隐私同意 | 当前未接入 |
| Cookie 政策 | `/cookies/` | `cookies` | `templates/website/cookie_policy.html` | `static/css/legal.css` | 无 | 否 | 是 | Footer、法律页互链 | 当前未接入 |

补充说明：

- 全站共享模板为 `templates/base.html`、`templates/includes/header.html`、`templates/includes/footer.html`。
- 全站共享 CSS 为 `static/css/base.css`、`static/css/components.css`。
- 全站共享 JS 为 `static/js/main.js`。
- 当前未实现公开 `sitemap.xml` 或 `robots.txt` 路由；canonical / noindex 逻辑仍保留在 `templates/base.html` 与 `website/context_processors.py`。
- `/consultation/` 继续 301 到 `/contact/`。
- `fr` / `en` 占位路由仍保留为内部预留，但已移出公开导航，不计入当前正式中文页面范围。

## 二、案例页面与案例入口处理结果

### A. 已修复

- 首页案例区保留，未删除。
- 首页案例区已移除“查看完整案例”按钮，避免指向不存在的公开案例详情页。
- `欧洲市场进入与战略` 页面中的匿名案例区保留，但已移除“查看完整案例”文字链接。
- 历史案例详情路由 `/cases/listed-company-france/` 保留兼容访问能力，但已改为 `301` 重定向到首页案例区锚点 `/#case-title`。
- Header、Footer、首页和服务页中均未新增任何“客户案例总览页”或“客户案例详情页”入口。

### B. 需要领导或同事决定

- 首页匿名案例区当前长度是否合适。
- 首页案例区是否需要进一步压缩语气、缩短成果描述或减少视觉权重。

### C. 等部署阶段处理

- 无。

## 三、已发现并修复的客观问题

### A. 已修复

- 移除 Header 中公开的 `FR / EN` 占位语言入口，避免把未完成语言版本暴露给评审用户。
- 修复公开案例详情入口：不再从首页和服务详情页链接到旧案例页面。
- 将旧案例详情路由调整为 301 重定向到首页案例区，避免保留空白占位页。
- Footer 中“个人服务与公司”标题调整为“个人服务与公司信息”，避免栏目名称不完整。
- Footer 增加统一城市表述：`Acoeurs Consulting在巴黎、上海和香港设有办公室与团队。`
- Footer 联系方式统一为：
  - 中国：`400-606-0685`
  - 法国：`+33 (0)9 72 96 05 73`
  - 邮箱：`contact@acoeursconsulting.com`
  - 巴黎地址：`32 AV. Kléber / 75116 Paris`
- 联系表单第 2 步单选项重复 `id` 已修复，避免可访问性和自动化测试冲突。
- 法律声明页移除过度具体的托管商公开描述，改为“上线前确认后补充”。
- 隐私政策页移除公开的域名注册商 / DNS / 托管商细节，改为更稳妥的通用说明。

### B. 需要领导或同事决定

- 首页“为什么选择 Acoeurs”区域是否保留当前数据模块的展示方式。
- `500+`、`92%`、`10+` 是否需要在首页继续保留当前密度，还是缩减到更克制的展示。

### C. 等部署阶段处理

- 若未来启用多语言，需要重新确认语言切换入口位置与公开范围。
- 若未来启用 sitemap / robots，需要按正式上线域名和多语言策略重新生成。

## 四、CTA 与旧文案检查结果

### A. 已修复

- 当前公开模板已清除以下旧 CTA 文案：
  - `预约30分钟咨询`
  - `立即预约咨询`
- 当前 CTA 使用情况已统一为：
  - 页面名称 / 导航：`联系我们`
  - 普通入口：`联系我们`
  - 服务详情页主行动按钮：`联系咨询`
  - 联系表单最终提交按钮：`提交咨询`

### B. 需要领导或同事决定

- 首页、总览页与关于我们页中的“联系我们”按钮密度是否合适。

### C. 等部署阶段处理

- 无。

## 五、联系方式一致性检查结果

### A. 已修复

- Footer、联系页、法律页中的电话、邮箱与巴黎地址已保持一致。
- `mailto:` 与 `tel:` 链接格式已正确使用。
- 未新增上海或香港详细地址，仅保留已确认的城市级公开表述。

### B. 需要领导或同事决定

- 是否在关于我们页或联系我们页增加更明确的“巴黎 · 上海 · 香港”办公室信息模块。

### C. 等部署阶段处理

- 若未来确认上海或香港公开地址，需要统一更新法律页、联系我们页与 Footer。

## 六、SEO 基础检查结果

### A. 已修复

- 正式页面均保留独立 `title` 与 `meta description`。
- 页面仍保持单一 `H1`。
- 面包屑结构仍在主要二级页和详情页生效。
- canonical / noindex 逻辑未破坏。

### B. 需要领导或同事决定

- 当前中文页面标题是否需要进一步品牌化。
- 首页标题 `首页 | Acoeurs Consulting` 是否要在上线前调整为更完整的品牌标题。

### C. 等部署阶段处理

- 当前未实现公开 `sitemap.xml`。
- 当前未实现公开 `robots.txt`。
- 上线前需按正式域名、环境变量与多语言策略复核 canonical 输出。

## 七、可访问性基础检查结果

### A. 已修复

- 联系表单中的重复 HTML `id` 已修复。
- 图片 `alt` 仍存在，主要按钮和链接使用了真实 `button` / `a` 元素。
- `prefers-reduced-motion` 逻辑仍保留在共享 CSS 与 `main.js` 中。
- 移动端菜单仍支持 `Escape` 关闭与键盘焦点控制。

### B. 需要领导或同事决定

- 无明显主观问题，本轮不建议因审美偏好调整现有交互形式。

### C. 等部署阶段处理

- 若后续接入更多图片资源，需继续逐张核对 `alt` 文案与尺寸属性。

## 八、桌面端与移动端检查结果

说明：本轮未实际启动浏览器或可视化设备模拟工具，因此以下结果基于模板、CSS、结构约束和自动化测试，不宣称完成真实浏览器视觉验收。

### A. 已修复

- 共享导航和联系表单的结构性问题已清理。
- 联系表单重复 `id` 已消除，降低移动端表单交互异常风险。
- 公开无效入口已移除，减少移动端菜单和 CTA 的误触达死链问题。

### B. 需要领导或同事决定

- 1440 / 1366 / 1024 / 768 / 390 / 360 视口下的真实视觉表现，仍需在浏览器中人工复核：
  - Header 是否拥挤
  - Hero 标题是否异常断行
  - 联系表单按钮是否始终可见
  - 法律页长文本是否足够易读
  - 360px 下是否仍有边距或容器宽度问题

### C. 等部署阶段处理

- 无。

## 九、联系我们页面与邮件逻辑检查结果

### A. 已修复

- 联系表单结构、honeypot、隐私同意与 3 步问卷逻辑仍保留。
- 开发与测试环境不会因为本轮改动而引入真实 SMTP 配置。
- 自动化测试继续使用 Django 测试邮件后端。

### B. 需要领导或同事决定

- 无。

### C. 等部署阶段处理

- 联系表单真实邮件投递尚未接入，待服务器及邮箱配置阶段完成。
- 生产 SMTP 仍应通过环境变量配置，不应写入代码仓库。
- 当前不新增 CRM、不新增咨询数据库模型、不增加自动回复邮件。

## 十、法律与隐私页面待确认事项

### A. 已修复

- 保留法律声明、隐私政策和 Cookie 政策页面可访问性与互链。
- 收敛了未经最终确认的公开技术细节。

### B. 需要领导或同事决定

- 上线前是否公开运营主体法定信息。
- 上线前是否公开域名注册、托管商或其他法务信息。

### C. 等部署阶段处理

- 法律主体完整名称
- 公司注册号 / SIREN / TVA 等法务字段
- ICP / 公安备案信息
- 最终托管商法务信息
- 最终服务器地区与部署区域

## 十一、多语言功能待完成事项

### A. 已修复

- 已移除公开语言入口，避免评审期误入占位页面。

### B. 需要领导或同事决定

- 中文站评审结束后，是否继续保留 `fr` / `en` 路由作为内部预留，或统一改为重定向。

### C. 等部署阶段处理

- 多语言内容本身尚未完成。
- 多语言导航、SEO、canonical、hreflang 与 sitemap 策略尚未设计。

## 十二、部署前待完成事项

### A. 已修复

- 无。

### B. 需要领导或同事决定

- 正式环境品牌数据展示密度。
- 是否公开更多公司背景信息、团队信息或实景图片。

### C. 等部署阶段处理

- 真实邮件投递配置
- 生产环境域名 / HTTPS / 服务器配置
- 正式 `SITE_URL`、`SITE_NOINDEX` 和 canonical 策略复核
- `sitemap.xml` 与 `robots.txt` 是否上线
- 法律主体和法务字段确认
- 多语言策略确认

## 十三、测试与检查执行结果

本轮执行命令：

```bash
./.venv/bin/python manage.py test website.tests
```

结果：

- 112 项测试通过。
- 已新增或调整的测试覆盖：
  - 所有正式中文页面返回 200
  - `/consultation/` 301 到 `/contact/`
  - 旧案例路由 301 到首页案例区
  - Header 主导航链接有效
  - Footer 法律链接有效
  - 服务详情页可从总览页访问
  - 公开模板中不存在案例详情公开入口
  - 首页案例区保留但不再链接旧案例页
  - 公开模板中不存在旧 CTA 文案
  - 页面不存在明显重复 HTML `id`
  - canonical / noindex 逻辑未被破坏

尚未执行：

- `./.venv/bin/python manage.py check`
- `./.venv/bin/python manage.py collectstatic --noinput`

这两项将在本轮代码与文档全部完成后统一执行。
