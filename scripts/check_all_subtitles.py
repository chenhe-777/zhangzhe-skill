import yt_dlp
import os
import sys

# 禁用代理
for proxy in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy, None)

# 更多热门视频URL
videos_to_check = [
    {'id': '1', 'title': '60 Minutes Interview', 'url': 'https://www.youtube.com/watch?v=GdWOWPjafDs'},
    {'id': '2', 'title': '60 Minutes Archives', 'url': 'https://www.youtube.com/watch?v=1tNMH2M_jJ0'},
    {'id': '3', 'title': 'China Caretaker President', 'url': 'https://www.youtube.com/watch?v=0_iUDMupp5s'},
    {'id': '4', 'title': 'Hong Kong press conference 2000', 'url': 'https://www.youtube.com/watch?v=vGlN6z9dTBc'},
    {'id': '5', 'title': 'Full history video', 'url': 'https://www.youtube.com/watch?v=ez7jYxFrRII'},
    {'id': '6', 'title': 'Too simple sometimes naive', 'url': 'https://www.youtube.com/watch?v=kMCSMrnVsek'},
    {'id': '7', 'title': 'TVBS interview', 'url': 'https://www.youtube.com/watch?v=p4lVvVcraHM'},
    {'id': '8', 'title': 'TVB interview', 'url': 'https://www.youtube.com/watch?v=VmZRacAUuvE'},
]

ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 60,
}

print('Checking all videos for subtitles...')
print('=' * 100)

videos_with_subs = []

for video in videos_to_check:
    try:
        print(f'{video["id"]}. {video["title"][:50]}')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video['url'], download=False)

            # 检查字幕
            has_manual_subs = 'subtitles' in info and info['subtitles'] and len(info['subtitles']) > 0
            has_auto_subs = 'automatic_captions' in info and info['automatic_captions'] and len(info['automatic_captions']) > 0

            manual_langs = list(info['subtitles'].keys()) if has_manual_subs else []
            auto_langs = list(info['automatic_captions'].keys()) if has_auto_subs else []

            if has_manual_subs or has_auto_subs:
                print(f'   Manual subtitles: {manual_langs}')
                print(f'   Auto subtitles: {auto_langs}')
                videos_with_subs.append({
                    'title': video['title'],
                    'url': video['url'],
                    'manual_langs': manual_langs,
                    'auto_langs': auto_langs
                })
            else:
                print(f'   No subtitles')

            print()

    except Exception as e:
        print(f'   Error: {str(e)[:80]}')
        print()

print('=' * 100)
print(f'\nVideos with subtitles: {len(videos_with_subs)}/{len(videos_to_check)}')

if videos_with_subs:
    print('\nVideos with subtitles:')
    for v in videos_with_subs:
        print(f'  - {v["title"]}')
        print(f'    URL: {v["url"]}')
