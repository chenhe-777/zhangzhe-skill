import yt_dlp
import os
import json

# 禁用代理
for proxy in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy, None)

# 搜索YouTube上的江泽民视频
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'socket_timeout': 60,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        queries = [
            'Jiang Zemin Hong Kong press conference 2000',
            'Jiang Zemin interview',
            '江泽民 香港记者会',
            '江泽民 采访'
        ]

        all_videos = []

        for query in queries:
            try:
                print(f'Searching: {query}')
                search_results = ydl.extract_info(f'ytsearch10:{query}', download=False)
                if 'entries' in search_results:
                    for video in search_results['entries']:
                        if video and 'id' in video and 'title' in video:
                            all_videos.append({
                                'id': video['id'],
                                'title': video['title'],
                                'view_count': video.get('view_count', 0),
                                'duration': video.get('duration', 0),
                                'url': f"https://www.youtube.com/watch?v={video['id']}"
                            })
            except Exception as e:
                print(f'  Search failed: {str(e)[:50]}')
                continue

        # 去重并按观看数排序
        unique_videos = {}
        for v in all_videos:
            if v['id'] not in unique_videos or v['view_count'] > unique_videos[v['id']]['view_count']:
                unique_videos[v['id']] = v

        sorted_videos = sorted(unique_videos.values(), key=lambda x: x.get('view_count', 0), reverse=True)

        print(f'\nFound {len(sorted_videos)} unique videos (sorted by view count):')
        print('=' * 100)
        for i, video in enumerate(sorted_videos[:20], 1):
            print(f'{i}. Views: {video.get("view_count", 0):,} | Duration: {video.get("duration", 0)}s')
            print(f'   Title: {video.get("title", "No title")[:80]}')
            print(f'   URL: {video.get("url", "")}')
            print()

        # 保存结果到文件
        with open('C:/Users/51968/.claude/skills/jiang-zemin-perspective/reference/youtube_videos.json', 'w', encoding='utf-8') as f:
            json.dump(sorted_videos, f, ensure_ascii=False, indent=2)

        print(f'\nSaved {len(sorted_videos)} videos to youtube_videos.json')

except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
