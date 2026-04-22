#!/usr/bin/env python3
"""
高频词汇每日生成器 - High Frequency Words Daily Generator

基于龙飞虎《6个月学会任何一种外语》方法论
- 1000个精选高频词，覆盖85%日常沟通
- 每天推送10个词，100天完成
- Edge TTS 标准发音（慢速）
- 老友记对话场景植入
"""

import json
import os
import sys
import datetime
import subprocess
import tempfile
import base64
from pathlib import Path

# ============== 配置区 ==============
SCRIPT_DIR = Path(__file__).parent.parent  # high-freq-words/
DATA_FILE = SCRIPT_DIR / "data" / "frequency_1000.json"
TEMPLATE_FILE = SCRIPT_DIR / "templates" / "daily_template.html"
OUTPUT_DIR = SCRIPT_DIR / "output"
AUDIO_DIR = SCRIPT_DIR / "audio"

WORDS_PER_DAY = 10
TOTAL_DAYS = 100  # 1000词 / 10词每天
TTS_RATE = "-30%"  # 慢速发音 (Edge TTS rate参数)
TTS_VOICE = "en-US-JennyNeural"  # 美式女声（清晰标准）

# ============== 工具函数 ==============

def load_words():
    """加载词库"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_words_for_day(day_num):
    """获取第N天的单词列表（从1开始）"""
    words = load_words()
    start_idx = (day_num - 1) * WORDS_PER_DAY
    end_idx = start_idx + WORDS_PER_DAY
    return words[start_idx:end_idx], start_idx + 1, end_idx


def generate_progress_dots(current_day):
    """生成进度条HTML"""
    dots = []
    for i in range(1, TOTAL_DAYS + 1):
        if i < current_day:
            cls = 'done'
        elif i == current_day:
            cls = 'current'
        else:
            cls = ''
        dots.append(f'<div class="progress-dot {cls}"></div>')
    return '\n'.join(dots)


def generate_word_card(word_data, index):
    """生成单个单词卡片HTML - 使用本地TTS音频文件"""
    level_cls = f"level-{word_data.get('level', 1)}"
    word      = word_data['word']
    
    # 查找TTS音频文件路径
    tts_dir = AUDIO_DIR / "tts" / f"{index:04d}"
    word_audio = (tts_dir / "word.mp3").exists()
    sent_audio = (tts_dir / "sentence.mp3").exists()
    
    # 构建audio标签
    word_btn_html = ""
    sent_btn_html = ""
    
    if word_audio:
        word_id  = f"w_{index}_audio"
        word_btn_html = f'''
            <button class="btn-audio btn-audio-tts" onclick="playLocalAudio('{word_id}')" ontouchstart="this.onclick(event)" id="{word_id}_btn">
                <span class="icon">🔊</span> 单词发音
            </button>
            <audio id="{word_id}" preload="auto"><source src="audio/tts/{index:04d}/word.mp3" type="audio/mpeg"></audio>'''
    else:
        # Fallback: Web Speech API
        word_btn_html = f'''
            <button class="btn-audio" onclick="speak('{word}', 0.55)" ontouchstart="this.onclick(event)">
                <span class="icon">🔊</span> 单词发音
            </button>'''
    
    if sent_audio:
        sent_id  = f"s_{index}_audio"
        sentence_escaped = word_data.get('sentence','').replace("'", "\\'")
        sent_btn_html = f'''
            <button class="btn-audio btn-audio-tts" onclick="playLocalAudio('{sent_id}')" ontouchstart="this.onclick(event)" id="{sent_id}_btn">
                <span class="icon">🗣️</span> 例句朗读
            </button>
            <audio id="{sent_id}" preload="auto"><source src="audio/tts/{index:04d}/sentence.mp3" type="audio/mpeg"></audio>'''
    else:
        sentence_escaped = word_data.get('sentence','').replace("`","\\`").replace("${","\\${")
        sent_btn_html = f'''
            <button class="btn-audio" onclick="speak(`{sentence_escaped}`, 0.6)" ontouchstart="this.onclick(event)">
                <span class="icon">🗣️</span> 例句朗读
            </button>'''
    
    card = f'''
    <div class="word-card">
        <div class="card-number">#{index}</div>
        <div class="word-main">
            <span class="word-text">{word}</span>
            <span class="phonetic">{word_data['phonetic']}</span>
        </div>
        <div class="meaning"><span class="level-badge {level_cls}">Lv.{word_data.get('level', 1)}</span> {word_data['meaning']}</div>
        
        <div class="audio-row">
            {word_btn_html}
            {sent_btn_html}
        </div>
        
        <div class="example-box">
            <div class="example-label">例句 Example</div>
            <div class="example-en">{word_data.get('sentence', '')}</div>
            <div class="example-cn">{word_data.get('sentence_cn', '')}</div>
        </div>
    </div>
    '''
    return card


# Bilibili video mapping
# BV1pyRsYHEVa has 234 parts (Friends S01-S10 clips)
# Format: S{season}-E{episode}-P{part}
# P001-010 = S01E01, P011-020 = S01E02, ... each episode has 10 parts
BILIBILI_BV = "BV1pyRsYHEVa"
# 官方外链播放器地址（专为嵌入设计，无X-Frame-Options限制）
BILIBILI_EMBED_URL = "https://player.bilibili.com/player.html?bvid=" + BILIBILI_BV + "&page="
BILIBILI_PAGE_URL  = "https://www.bilibili.com/video/" + BILIBILI_BV + "?p="


def get_bilibili_page(word_index):
    """Map word index (1-based) to Bilibili page number (1-234)."""
    available_pages = list(range(1, min(61, 235)))  # pages 1-60, S01E01~S01E06
    page_idx = (word_index - 1) % len(available_pages)
    return available_pages[page_idx]


def get_episode_info(page_num):
    """Get human-readable episode info from page number."""
    episode = ((page_num - 1) // 10) + 1
    part    = ((page_num - 1) % 10) + 1
    season  = 1
    if page_num > 60:
        season  = ((page_num - 1) // 24) + 1
        episode = ((page_num - 1) % 24) + 1
    return f"S{season:02d}E{episode:02d}-P{part}"


def generate_friends_scene(word_data, index):
    """Generate Friends scene HTML with embedded Bilibili player + smart fallback."""
    card_id    = f"scene_{index}"
    iframe_id  = f"bili_iframe_{index}"
    player_id  = f"bili_player_{index}"
    btn_id     = f"bili_btn_{index}"
    bili_page  = get_bilibili_page(index)
    ep_info    = get_episode_info(bili_page)
    embed_url  = f"{BILIBILI_EMBED_URL}{bili_page}&autoplay=0&high_quality=1&danmaku=0"
    page_url   = f"{BILIBILI_PAGE_URL}{bili_page}"

    scene = f'''
    <div class="scene-card" id="{card_id}">
        <div class="scene-header">
            <h3>&#127916; Scene #{index} &middot; &ldquo;{word_data['word']}&rdquo;</h3>
            <span class="ep-badge">Friends {ep_info}</span>
        </div>
        <div class="scene-dialogue">{word_data['friends_scene']}</div>
        <div class="scene-translation">{word_data['friends_cn']}</div>

        <div class="bili-bar">
            <button id="{btn_id}" class="btn-bili" onclick="togglePlayer('{player_id}','{btn_id}','{iframe_id}','{embed_url}')">
                &#127916; 老友记原声片段
            </button>
            <a href="{page_url}" target="_blank" class="btn-bili-fallback" title="在B站打开">&#8599;</a>
        </div>

        <div id="{player_id}" class="bili-player" style="display:none;">
            <div class="player-loading" id="loading_{index}">⏳ 加载中...</div>
            <iframe id="{iframe_id}"
                    src="about:blank"
                    data-src="{embed_url}"
                    scrolling="no"
                    frameborder="0"
                    allowfullscreen="true"
                    allow="autoplay; encrypted-media; fullscreen; picture-in-picture"
                    referrerpolicy="no-referrer-when-downgrade"
                    style="display:none;"
                    onload="onIframeLoad(this, 'loading_{index}')">
            </iframe>
            <div id="fail_{index}" class="player-fail" style="display:none;">
                &#128529; 视频无法嵌入（网络或浏览器限制）<br>
                <a href="{page_url}" target="_blank" class="btn-open-bili">&#127916; 去B站看原声</a>
            </div>
        </div>
    </div>
    '''
    return scene


def generate_html(day_num, target_date=None):
    """
    生成指定天数的完整HTML页面
    
    Args:
        day_num: 第几天 (1-100)
        target_date: 目标日期 YYYY-MM-DD 格式，默认今天
    """
    if target_date is None:
        target_date = datetime.date.today().strftime("%Y-%m-%d")
    
    # 获取当天单词
    words, start_num, end_num = get_words_for_day(day_num)
    
    if not words:
        print(f"[ERROR] Day {day_num}: No words found!")
        return None
    
    # 读取模板
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 生成各部分HTML
    progress_dots = generate_progress_dots(day_num)
    
    word_cards_html = ""
    friends_scenes_html = ""
    
    for i, w in enumerate(words):
        word_cards_html += generate_word_card(w, start_num + i)
        friends_scenes_html += generate_friends_scene(w, start_num + i)
    
    # 替换模板变量
    html = template.replace("{{day_num}}", str(day_num))
    html = html.replace("{{date_str}}", str(target_date))
    html = html.replace("{{start_num}}", str(start_num))
    html = html.replace("{{end_num}}", str(end_num))
    html = html.replace("{{progress_dots}}", progress_dots)
    html = html.replace("{{word_cards}}", word_cards_html)
    html = html.replace("{{friends_scenes}}", friends_scenes_html)
    
    return html


def save_output(html_content, day_num, date_str=None):
    """保存生成的HTML文件"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if date_str is None:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
    
    filename = f"high_freq_words_day{day_num:03d}_{date_str}.html"
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] Saved: {filepath}")
    return filepath


def generate_tts_audio(text, output_path, voice=TTS_VOICE, rate=TTS_RATE):
    """
    使用Edge TTS生成音频文件
    
    Args:
        text: 要合成的文本
        output_path: 输出mp3路径
        voice: Edge TTS音色
        rate: 语速 (如 "-30%")
    """
    try:
        import edge_tts
        
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
        asyncio_run = getattr(edge_tts, 'asyncio', None)
        # edge_tts uses its own async
        import asyncio
        
        async def _generate():
            await communicate.save(str(output_path))
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_generate())
        loop.close()
        
        print(f"[TTS OK] {output_path.name}")
        return True
        
    except ImportError:
        print("[WARN] edge_tts not installed. Run: pip install edge-tts")
        return False
    except Exception as e:
        print(f"[TTS ERROR] {e}")
        return False


def generate_all_tts_for_day(day_num):
    """为某一天的所有单词和例句生成音频"""
    words, start_idx, _ = get_words_for_day(day_num)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    day_audio_dir = AUDIO_DIR / f"day{day_num:03d}"
    day_audio_dir.mkdir(exist_ok=True)
    
    audio_files = []
    for i, w in enumerate(words):
        # 单词发音
        word_mp3 = day_audio_dir / f"{i+1:02d}_{w['word']}_word.mp3"
        generate_tts_audio(w['word'], word_mp3)
        if word_mp3.exists():
            audio_files.append(word_mp3)
        
        # 例句发音
        sent_mp3 = day_audio_dir / f"{i+1:02d}_{w['word']}_sentence.mp3"
        generate_tts_audio(w['sentence'], sent_mp3)
        if sent_mp3.exists():
            audio_files.append(sent_mp3)
    
    return audio_files


# ============== CLI 命令 ==============

def cmd_generate(args):
    """生成指定天数的HTML"""
    day = int(args[0]) if args else 1
    date_str = args[1] if len(args) > 1 else None
    
    print(f"\n🚀 Generating Day {day}...")
    html = generate_html(day, date_str)
    if html:
        filepath = save_output(html, day, date_str)
        print(f"\n✅ Done! Output: {filepath}")
        return filepath
    return None


def cmd_generate_range(args):
    """批量生成多天的HTML"""
    start = int(args[0]) if len(args) > 0 else 1
    end = int(args[1]) if len(args) > 1 else TOTAL_DAYS
    
    for day in range(start, end + 1):
        print(f"\n{'='*50}")
        cmd_generate([str(day)])
    
    print(f"\n🎉 All done! Generated Day {start}-{end}")


def cmd_list(args):
    """列出所有单词"""
    words = load_words()
    print(f"\n📚 Total words: {len(words)}\n")
    
    level_counts = {}
    for w in words:
        lv = w.get('level', 1)
        level_counts[lv] = level_counts.get(lv, 0) + 1
    
    for lv in sorted(level_counts.keys()):
        print(f"  Level {lv}: {level_counts[lv]} words")
    
    if args and args[0] == '--detail':
        print("\n--- Word List ---")
        for i, w in enumerate(words, 1):
            print(f"  {i:4d}. [{w.get('level','?')}] {w['word']:15s} {w['phonetic']}  - {w['meaning']}")


def cmd_test(args):
    """测试模式：生成第1天并预览"""
    print("🧪 Test mode: generating Day 1...\n")
    
    day = int(args[0]) if args else 1
    html = generate_html(day)
    
    if html:
        filepath = save_output(html, day)
        print(f"\n🌐 Open the file in your browser to preview:")
        print(f"   {filepath}")
        return filepath
    return None


def cmd_info(args):
    """显示项目信息"""
    words = load_words()
    total = len(words)
    days = (total + WORDS_PER_DAY - 1) // WORDS_PER_DAY
    
    print(f"""
╔══════════════════════════════════════╗
║   📚 高频词汇学习系统 v1.0          ║
║   High-Frequency Words Learner      ║
╠══════════════════════════════════════╣
║  总词数:     {total:>5} 个               ║
║  每日词汇:   {WORDS_PER_DAY:>5} 个               ║
║  总天数:     {days:>5} 天                ║
║  覆盖率:     ~85% 日常沟通              ║
║  方法论:     龙飞虎6个月法             ║
║  TTS引擎:    Edge TTS (JennyNeural)  ║
╠══════════════════════════════════════╣
║  词库文件:   data/frequency_1000.json ║
║  模板文件:   templates/daily_template ║
║  输出目录:   output/                   ║
║  音频目录:   audio/                    ║
╚══════════════════════════════════════╝
""")


def main():
    """主入口"""
    if len(sys.argv) < 2 or sys.argv[1] not in ('generate', 'range', 'list', 'test', 'info'):
        print("""
用法:
  python generate.py generate [天数 [YYYY-MM-DD]]   生成指定天数
  python generate.py range [开始天 [结束天]]         批量生成
  python generate.py list [--detail]                 列出所有单词
  python generate.py test [天数]                     测试生成
  python generate.py info                             项目信息

示例:
  python generate.py generate 1                       生成第1天
  python generate.py generate 5 2026-04-25           生成第5天(指定日期)
  python generate.py range 1 3                       生成第1-3天
  python generate.py range                            生成全部(1-100天)
  python generate.py test 1                           测试第1天
""")
        sys.exit(0)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        'generate': cmd_generate,
        'range': cmd_generate_range,
        'list': cmd_list,
        'test': cmd_test,
        'info': cmd_info,
    }
    
    commands[command](args)


if __name__ == "__main__":
    main()
