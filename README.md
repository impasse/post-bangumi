# Post Bangumi

基于 qbittorrent 下载完成通知的自动追番工具

## 功能说明

在 qbittorrent rss 自动下载完成后自动<del>通过 ChatGPT 解析</del>番剧信息，并 link 为 emby 支持的目录结构。

## 使用说明

- 配置 .env
- 启动 main.py
- qbittorrent 配置 run on torrent finish: `post-bangumi.sh "%L" "%F" "%K"`
- 配置 qbittorrent rss 自动下载规则
