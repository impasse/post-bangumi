# Post Bangumi

基于 qbittorrent 下载完成通知的自动追番工具

## 功能说明

在 qbittorrent rss 自动下载完成后自动通过 ChatGPT 解析番剧信息，并 link 为 emby 支持的目录结构。

## 使用说明

- 配置 .env
- 启动 main.py
- qbittorrent 配置 run on torrent finish: `curl  -X POST 'http://{post-bangumi}:8000/api/post_download' -H 'Content-Type: application/json' --data-raw '{ "category": "%L", "save_path": "%F", "torrent_id": "%K" }'`
- 配置 qbittorrent rss 自动下载规则
