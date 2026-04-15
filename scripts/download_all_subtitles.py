import yt_dlp
import os

# 禁用代理
for proxy in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy, None)

videos_to_download = [
    {'title': 'China_Caretaker_President', 'url': 'https://www.youtube.com/watch?v=0_iUDMupp5s', 'lang': 'en-US'},
    {'title': '60_Minutes_Interview', 'url': 'https://www.youtube.com/watch?v=GdWOWPjafDs', 'lang': 'en'},
    {'title': '60_Minutes_Archives', 'url': 'https://www.youtube.com/watch?v=1tNMH2M_jJ0', 'lang': 'en'},
    {'title': 'Full_History_Video', 'url': 'https://www.youtube.com/watch?v=ez7jYxFrRII', 'lang': 'en'},
    {'title': 'TVBS_Interview', 'url': 'https://www.youtube.com/watch?v=p4lVvVcraHM', 'lang': 'en'},
]

output_dir = 'C:/Users/51968/.claude/skills/jiang-zemin-perspective/reference/subtitles'
os.makedirs(output_dir, exist_ok=True)

print('Downloading subtitles for 5 videos...')
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
            'subtitleslangs': [video['lang'], 'en', 'en-US'],
            'subtitlesformat': 'srt',  # 使用SRT格式
            'outtmpl': os.path.join(output_dir, f'{video["title"]}.%(ext)s'),
            'socket_timeout': 120,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video['url']])

        # 检查是否下载成功
        srt_files = [f for f in os.listdir(output_dir) if video['title'] in f and f.endswith('.srt')]
        if srt_files:
            print(f'  Downloaded: {srt_files[0]}')
            successful_downloads.append({
                'title': video['title'],
                'file': os.path.join(output_dir, srt_files[0])
            })
        else:
            print(f'  Warning: No SRT file found')

        print()

    except Exception as e:
        print(f'  Error: {str(e)[:100]}')
        print()

print('=' * 100)
print(f'\nSuccessfully downloaded: {len(successful_downloads)}/{len(videos_to_download)}')

if successful_downloads:
    print('\nDownloaded files:')
    for dl in successful_downloads:
        print(f'  - {dl["title"]}: {dl["file"]}')
