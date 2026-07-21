# Render staging 域名接入运行手册

更新日期：2026-07-21

本手册用于当前 Django 站点接入：

- Render 默认域名
- `staging.acoeursconsulting.com`

并为未来接入：

- `acoeursconsulting.com`
- `www.acoeursconsulting.com`

保留统一的环境变量驱动配置。

## 1. 当前域名结构

- 本地开发：
  - `localhost`
  - `127.0.0.1`
  - `[::1]`
- Render 默认域名：
  - `<your-service>.onrender.com`
- staging：
  - `staging.acoeursconsulting.com`
- 未来正式域名：
  - `acoeursconsulting.com`
  - `www.acoeursconsulting.com`

## 2. 当前 Render 服务

- Render blueprint 已在 `render.yaml` 定义
- Web Service 名称：
  - `acoeursconsulting-web`
- 数据库名称：
  - `acoeursconsulting-db`

## 3. Render 默认域名

当前仓库代码无法确认实际分配的 Render 默认域名。

在 Render Dashboard 中查看：

- Web Service
- Settings
- Custom Domains / Live URL

并记录为：

- `<your-service>.onrender.com`

## 4. staging 域名

目标 staging 域名：

- `staging.acoeursconsulting.com`

## 5. 正式主域名规划

未来正式主域名建议：

- 主 canonical：`https://acoeursconsulting.com`
- 辅助访问：`https://www.acoeursconsulting.com`

正式上线前再决定是否保留 `www` 访问以及是否将其重定向到根域名。

## 6. Render Dashboard 添加自定义域名步骤

1. 打开 Render Dashboard
2. 进入 Web Service：`acoeursconsulting-web`
3. 打开 `Settings`
4. 打开 `Custom Domains`
5. 添加：
   - `staging.acoeursconsulting.com`
6. 记录 Render 提供的目标地址
7. 等待 Render 显示验证状态

## 7. 阿里云 DNS 的 staging 记录

推荐记录：

- 类型：`CNAME`
- 主机记录：`staging`
- 记录值：`<your-service>.onrender.com`

## 8. 不修改 Nameserver 的说明

当前仅需要添加或调整 `staging` 的 DNS 记录。

不要：

- 修改 Nameserver
- 切换 DNS 服务商
- 删除现有邮箱或其他业务记录

## 9. 不删除邮箱相关记录的警告

操作 DNS 时，不要删除：

- MX
- SPF
- DKIM
- DMARC

这些记录与邮箱收发和反垃圾保护有关，不属于本轮网站接入范围。

## 10. 冲突记录检查

在为 `staging` 添加 CNAME 前，先检查是否已存在：

- `staging` 的 A 记录
- `staging` 的 AAAA 记录
- `staging` 的旧 CNAME

若存在冲突，先删除旧冲突记录，再保留唯一的 `staging` CNAME。

## 11. Render 验证步骤

1. Render 中添加 `staging.acoeursconsulting.com`
2. DNS 生效后等待 Render 验证
3. 确认：
   - Render default URL 可访问
   - `https://staging.acoeursconsulting.com` 可访问
   - `/health/` 返回 200

## 12. HTTPS 证书检查

验证以下项目：

- Render 已为 staging 域名签发证书
- `https://staging.acoeursconsulting.com` 正常打开
- 不出现证书错误
- Admin 登录页能以 HTTPS 加载

## 13. ALLOWED_HOSTS 环境变量

当前推荐 staging 值：

```env
ALLOWED_HOSTS=staging.acoeursconsulting.com
```

说明：

- `localhost` / `127.0.0.1` / `[::1]` 在代码中始终保留
- `RENDER_EXTERNAL_HOSTNAME` 会在运行时自动追加
- 不使用 `*`

## 14. CSRF_TRUSTED_ORIGINS 环境变量

当前推荐 staging 值：

```env
CSRF_TRUSTED_ORIGINS=https://staging.acoeursconsulting.com
```

说明：

- 必须带协议
- Render 默认域名会在运行时自动追加为 `https://<your-service>.onrender.com`

## 15. SITE_URL 与 canonical 配置

当前推荐 staging 值：

```env
SITE_URL=https://staging.acoeursconsulting.com
```

说明：

- staging 环境下 canonical 应使用 staging 域名
- 本地开发默认不输出 localhost canonical
- 正式上线后切换为：

```env
SITE_URL=https://acoeursconsulting.com
```

## 16. staging noindex 检查

当前推荐 staging 值：

```env
SITE_NOINDEX=true
```

上线后检查页面 `<head>` 中是否输出：

```html
<meta name="robots" content="noindex, nofollow">
```

## 17. 静态文件检查

部署完成后确认：

- CSS 正常加载
- JS 正常加载
- Logo 与图片正常加载
- `collectstatic` 在 Render 构建阶段成功

## 18. Admin 登录检查

部署后验证：

- `/admin/login/` 可打开
- HTTPS 正常
- `csrftoken` 正常工作
- 登录 POST 不触发 CSRF 错误

## 19. 法律页面检查

确认：

- `/legal/`
- `/privacy/`
- `/cookies/`

在 staging 上可访问，且未生成错误的正式主域 canonical。

## 20. 移动端检查

在 staging 验收时检查：

- 首页
- 服务总览页
- 服务详情页
- 法律页面

至少覆盖：

- 1440px
- 1024px
- 768px
- 390px

## 21. 回滚 DNS 的方法

如果 staging 解析后出现严重问题：

1. 删除或停用 `staging` 的新 CNAME
2. 若之前有旧记录，恢复为原值
3. 在 Render 中移除 `staging.acoeursconsulting.com`
4. 等待 DNS TTL 传播完成

## 22. 正式主域名切换前检查清单

- 是否确认主 canonical 使用根域还是 `www`
- 是否已验证 staging HTTPS、Admin、静态文件和 noindex
- 是否已完成法律声明正式信息补充
- 是否已确认 Render 部署区域和日志保留策略
- 是否已确认域名自动续费
- 是否已确认 Aliyun DNS 中无冲突记录
- 是否已决定根域名采用 ALIAS/ANAME 还是根据 Render 当时官方说明使用 A 记录
- `www` 是否使用：
  - `CNAME -> <your-service>.onrender.com`
