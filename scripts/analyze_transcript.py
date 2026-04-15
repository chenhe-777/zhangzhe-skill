"""
分析江泽民采访英文字幕，提取原汁原味表达，
然后用江泽民的表达DNA进行翻译和优化
"""

import re
import json

# 读取英文字幕
srt_file = 'C:/Users/51968/.claude/skills/jiang-zemin-perspective/reference/subtitles/China_Caretaker_President.en-US.srt'

print('Analyzing Jiang Zemin transcript...')
print('=' * 100)

# 读取SRT文件
with open(srt_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 解析SRT格式
def parse_srt(srt_content):
    """解析SRT文件，提取对话内容"""
    entries = []
    blocks = re.split(r'\n\n(?=\d+\n)', srt_content)

    for block in blocks:
        if not block.strip():
            continue

        # 提取时间戳和文本
        lines = block.split('\n')
        timestamp_line = None
        text_lines = []

        for i, line in enumerate(lines):
            if '-->' in line:
                timestamp_line = line
            elif line.strip() and not re.match(r'^\d+$', line):
                # 清理文本
                cleaned = re.sub(r'<[^>]+>', '', line)  # 移除HTML标签
                cleaned = re.sub(r'\{[^}]*\}', '', cleaned)  # 移除花字
                cleaned = cleaned.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                cleaned = cleaned.replace('  ', ' ')  # 合并多余空格
                if cleaned.strip():
                    text_lines.append(cleaned.strip())

        if text_lines:
            entries.append({
                'timestamp': timestamp_line,
                'text': ' '.join(text_lines)
            })

    return entries

entries = parse_srt(content)

print(f'Total entries found: {len(entries)}')
print()

# 江泽民表达DNA特征
JIANG_EXPRESSION_DNA = {
    # 坚定词汇
    'firm_words': ['必须', '始终', '一定', '坚决', '彻底', '始终如一', '要坚定不移',
                  '我们绝不能', '我们一定要', '应当', '要'],

    # 排比句式
    'parallelism': [
        '三个代表',
        '发展是硬道理',
        '解放思想，实事求是',
        '与时俱进',
        '立党为公，执政为民',
    ],

    # 语气特征
    'tone_markers': [
        '我想强调的是',
        '我们必须认识到',
        '这是一个基本事实',
        '从根本上说',
        '这个道理很简单',
    ],

    # 理论升华
    'elevation_markers': [
        '从理论和实践的结合上讲',
        '从世界观和方法论的高度看',
        '这是历史发展的必然',
    ],
}

# 过滤出可能包含江泽民原话的片段
def is_jiang_speaking(text):
    """判断是否可能是江泽民在说话"""
    # 关键词指示
    jiang_indicators = [
        'I would like to emphasize',
        'We must recognize',
        'This is a basic fact',
        'Fundamentally speaking',
        'The principle is very simple',
        'three represents',
        'represents advanced productive forces',
        'represents advanced culture',
        'represents fundamental interests',
        'development is the absolute principle',
        'keep pace with the times',
        'serve the people wholeheartedly',
        'establish a public for the people, govern for the people',
    ]

    text_lower = text.lower()
    for indicator in jiang_indicators:
        if indicator.lower() in text_lower:
            return True
    return False

# 提取江泽民相关片段
jiang_segments = []

for i, entry in enumerate(entries):
    # 检查当前和前后几个条目
    context = []
    if i > 0:
        context.append(entries[i-1]['text'])
    if i > 1:
        context.append(entries[i-2]['text'])
    context.append(entry['text'])
    if i < len(entries) - 1:
        context.append(entries[i+1]['text'])

    combined_context = ' '.join(context)

    # 判断是否包含江泽民原话
    if is_jiang_speaking(combined_context) or is_jiang_speaking(entry['text']):
        jiang_segments.append({
            'timestamp': entry['timestamp'],
            'text': entry['text'],
            'context': combined_context,
        })

print(f'Jiang-related segments found: {len(jiang_segments)}')
print()

# 提取重要的直接引语或表达
important_quotes = []

# 直接引语模式
direct_quote_pattern = r'["\'](.+?)["\']'
for entry in entries:
    matches = re.findall(direct_quote_pattern, entry['text'])
    if matches:
        for quote in matches:
            if len(quote) > 10:  # 过滤太短的
                important_quotes.append({
                    'timestamp': entry['timestamp'],
                    'quote': quote.strip('"\''),
                })

# 提取排比句
parallelism_pattern = r'(three|Three).*(represent|Represent)'
for entry in entries:
    if re.search(parallelism_pattern, entry['text']):
        important_quotes.append({
            'timestamp': entry['timestamp'],
            'quote': entry['text'],
        })

print(f'Important quotes extracted: {len(important_quotes)}')
print()

# 显示一些重要的提取结果
print('=' * 100)
print('IMPORTANT JIANG ZEMIN EXPRESSIONS FROM TRANSCRIPT')
print('=' * 100)
print()

for i, quote in enumerate(important_quotes[:20], 1):  # 显示前20个
    print(f'{i}. {quote["timestamp"]}')
    print(f'   {quote["quote"][:150]}...' if len(quote["quote"]) > 150 else f'   {quote["quote"]}')
    print()

# 保存提取结果
output_file = 'C:/Users/51968/.claude/skills/jiang-zemin-perspective/reference/jiang_extracted_quotes.json'

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'quotes': important_quotes,
        'segments': jiang_segments[:50],  # 保存前50个片段
    }, f, ensure_ascii=False, indent=2)

print(f'Extracted quotes saved to: {output_file}')
