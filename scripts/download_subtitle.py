import yt_dlp
import os
import sys

# 禁用代理
for proxy in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy, None)

video_url = 'https://www.youtube.com/watch?v=1tNMH2M_jJ0'
output_dir = 'C:/Users/51968/.claude/skills/jiang-zemin-perspective/reference'

ydl_opts = {
    'quiet': False,
    'no_warnings': False,
    'writesubtitles': True,
    'writeautomaticcaptions': True,  # 也下载自动生成字幕
    'skip_download': True,  # 不下载视频，只下载字幕
    'subtitleslangs': ['en', 'en-US', 'en-GB', 'zh', 'zh-Hans', 'zh-CN'],  # 优先英文和中文字幕
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    'socket_timeout': 120,
}

print(f'Downloading subtitles for: {video_url}')
print(f'Output directory: {output_dir}')
print('=' * 100)

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print('\nSubtitle download completed!')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
