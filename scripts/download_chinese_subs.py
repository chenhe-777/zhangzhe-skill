import yt_dlp
import os

# 禁用代理
for proxy in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy, None)

# 优先下载中文字幕
videos_to_download = [
    {'title': '60_Minutes_Interview', 'url': 'https://www.youtube.com/watch?v=GdWOWPjafDs', 'lang': ['zh-Hans', 'zh-CN', 'zh']},
    {'title': '60_Minutes_Archives', 'url': 'https://www.youtube.com/watch?v=1tNMH2M_jJ0', 'lang': ['zh-Hans', 'zh-CN', 'zh']},
    {'title': 'Full_History_Video', 'url': 'https://www.youtube.com/watch?v=ez7jYxFrRII', 'lang': ['zh-Hans', 'zh-CN', 'zh']},
    {'title': 'TVBS_Interview', 'url': 'https://www.youtube.com/watch?v=p4lVvVcraHM', 'lang': ['zh-Hans', 'zh-CN', 'zh']},
    {'title': 'Hong_Kong_Press_Conference_2000', 'url': 'https://www.youtube.com/watch?v=vGlN6z9dTBc', 'lang': ['zh-Hans', 'zh-CN', 'zh']},
]

output_dir = 'C:/Users/51968/.claude/skills/jiang-zemin-perspective/reference/subtitles'
os.makedirs(output_dir, exist_ok=True)

print('Downloading subtitles (prefer Chinese)...')
print('=' * 100)

successful_downloads = []

for video in videos_to_download:
    try:
        print(f'Processing: {video["title"]}')
        print(f'URL: {video["url"]}')

        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'writesubtitles': True,
            'writeautomaticcaptions': True,
            'skip_download': True,
            'subtitleslangs': video['lang'] + ['en', 'en-US'],  # 优先中文，也保留英文作为备份
            'subtitlesformat': 'srt',
            'outtmpl': os.path.join(output_dir, f'{video["title"]}.%(ext)s'),
            'socket_timeout': 120,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video['url']])

        # 检查下载的文件
        srt_files = [f for f in os.listdir(output_dir) if video['title'] in f and f.endswith('.srt')]
        if srt_files:
            # 找出是否是中文字幕
            chinese_subs = [f for f in srt_files if 'zh' in f.lower()]
            if chinese_subs:
                print(f'  Downloaded Chinese subtitles: {chinese_subs[0]}')
                successful_downloads.append({
                    'title': video['title'],
                    'file': os.path.join(output_dir, chinese_subs[0]),
                    'language': 'Chinese'
                })
            elif srt_files:
                print(f'  Downloaded (no Chinese): {srt_files[0]}')
                successful_downloads.append({
                    'title': video['title'],
                    'file': os.path.join(output_dir, srt_files[0]),
                    'language': 'English/Other'
                })
        else:
            print(f'  Warning: No SRT file found')

        print()

    except Exception as e:
        print(f'  Error: {str(e)[:150]}')
        print()

print('=' * 100)
print(f'\nSuccessfully downloaded: {len(successful_downloads)}/{len(videos_to_download)}')

if successful_downloads:
    print('\nDownloaded files:')
    for dl in successful_downloads:
        print(f'  - {dl["title"]} ({dl["language"]}): {dl["file"]}')
