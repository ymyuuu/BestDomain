# BestDomain

## 使用说明

1. 创建 Cloudflare API 令牌
   - 访问 [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
   - 选择需要解析的域名，创建编辑 DNS 权限的 `CF_API_TOKEN`

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/26aa632b-e1b9-4e72-9e69-713f19a16fa9">

2. 设置 GitHub Secrets
   - 在你的 GitHub 仓库中，设置 `CF_API_TOKEN` 为你的 Cloudflare API 令牌

3. 配置 GitHub Actions 定时任务
   - 编辑 `.github/workflows/main.yml` 文件，设置 `cron` 表达式以定义任务运行时间
