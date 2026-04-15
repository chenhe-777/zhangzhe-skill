import yt_dlp
import os
import json

# 禁用代理
for proxy in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy, None)

# 从之前的搜索结果中读取视频列表（手动输入热门视频URL）
热门视频 = [
    {'title': '60 Minutes Interview with Jiang Zemin', 'url': 'https://www.youtube.com/watch?v=GdWOWPjafDs', 'views': 1047085},
    {'title': 'Jiang Zemin lectures Hong Kong reporters at press conference in 2000', 'url': 'https://www.youtube.com/watch?v=vGlN6z9dTBc', 'views': 135143},
    {'title': '60 Minutes Archives: An interview with China\'s Jiang Zemin', 'url': 'https://www.youtube.com/watch?v=1tNMH2M_jJ0', 'views': 682000},
    {'title': 'Jiang Zemin: China\'s Caretaker President', 'url': 'https://www.youtube.com/watch?v=0_iUDMupp5s', 'views': 230730},
]

ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 60,
}

print('Checking YouTube videos for subtitles...')
print('=' * 100)

videos_with_subtitles = []

for i, video in enumerate(热门视频, 1):
    try:
        print(f'{i}. Checking: {video["title"][:60]}...')
        print(f'   URL: {video["url"]}')

        # 获取视频信息和字幕
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video['url'], download=False)

            # 检查字幕
            subtitles = []
            if 'subtitles' in info and info['subtitles']:
                for lang, sub_info in info['subtitles'].items():
                    subtitles.append(f'{lang} ({sub_info.get("ext", "unknown")})')

            if 'automatic_captions' in info and info['automatic_captions']:
                for lang, sub_info in info['automatic_captions'].items():
                    subtitles.append(f'{lang} (auto-{sub_info.get("ext", "unknown")})')

            if subtitles:
                print(f'   Subtitles: {", ".join(subtitles[:10])}')
                videos_with_subtitles.append({
                    'title': video['title'],
                    'url': video['url'],
                    'views': video['views'],
                    'subtitles': subtitles,
                    'video_id': info.get('id', 'unknown')
                })
            else:
                print(f'   No subtitles found')

            print()

    except Exception as e:
        print(f'   Error: {str(e)[:100]}')
        print()

print('=' * 100)
print(f'\nVideos with subtitles: {len(videos_with_subtitles)}/{len(热门视频)}')

if videos_with_subtitles:
    # 保存结果

    print(f'Saved results to videos_with_subtitles.json')
