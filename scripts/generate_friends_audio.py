#!/usr/bin/env python3
"""
老友记多角色对话音频生成器 - Friends Multi-Voice Audio Generator

使用 Edge TTS 多音色模拟老友记6位主角的对话声音，
为每个高频词生成情景对话风格的mp3音频文件。

用法:
  python generate_friends_audio.py [day_num]          生成指定天数(默认全部)
  python generate_friends_audio.py --list-voices      列出可用音色
  python generate_friends_audio.py --test             测试单个词
"""

import json
import os
import sys
import asyncio
import re
from pathlib import Path
from datetime import datetime

# ============== 路径配置 ==============
SCRIPT_DIR = Path(__file__).parent.parent
DATA_FILE = SCRIPT_DIR / "data" / "frequency_1000.json"
AUDIO_OUTPUT = SCRIPT_DIR / "audio" / "friends"

# ============== 老友记角色音色映射 ==============
# 每个角色对应一个Edge TTS音色，尽量匹配原剧人物特点
CHARACTER_VOICES = {
    # Female characters
    'Monica':   'en-US-JennyNeural',       # Clear, mature female voice
    'Rachel':   'en-US-AriaNeural',         # Young, sweet female voice
    'Phoebe':   'en-US-NancyNeural',        # Unique, dreamy female voice
    
    # Male characters
    'Ross':     'en-US-GuyNeural',          # Gentle, intellectual male voice
    'Chandler': 'en-US-EricNeural',         # Witty, slightly higher male voice
    'Joey':     'en-US-TonyNeural',         # Deep, casual male voice
}

# 默认音色（当说话人不在上述列表时）
DEFAULT_VOICE = 'en-US-JennyNeural'

# TTS parameters - dialogue speed (slightly slower than normal conversation)
DIALOGUE_RATE = '-5%'   # Dialogue: close to normal speed (just slightly slower)
PAUSE_BREAK = 'silence="300ms"'  # 句间停顿300ms


# ============== 工具函数 ==============

def load_words():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_dialogue(dialogue_text):
    """
    解析对话文本，提取 [(角色名, 台词), ...]
    
    输入格式示例:
        Monica: Anyone want a coffee?
        Joey: I'll take a large one!
        Chandler: Make that two.
    """
    lines = dialogue_text.strip().split('\n')
    dialogues = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 匹配 "RoleName: dialogue text" 格式
        match = re.match(r'^([A-Za-z]+):\s*(.+)$', line)
        if match:
            character = match.group(1).strip()
            text = match.group(2).strip()
            # 去掉markdown加粗标记
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            if text:
                dialogues.append((character, text))
    
    return dialogues


def get_voice_for_character(character):
    """根据角色名获取对应的TTS音色"""
    # 精确匹配
    if character in CHARACTER_VOICES:
        return CHARACTER_VOICES[character]
    
    # 模糊匹配
    for name, voice in CHARACTER_VOICES.items():
        if name.lower() in character.lower() or character.lower() in name.lower():
            return voice
    
    return DEFAULT_VOICE


async def generate_dialogue_audio(dialogues, output_path, word):
    """
    为一组对话生成多角色音频文件
    
    使用 SSML 格式，每个角色切换对应音色，
    中间加入自然停顿，营造真实对话感。
    """
    import edge_tts
    
    if not dialogues:
        print(f"  [SKIP] No dialogues for {word}")
        return False
    
    # 构建 SSML (Speech Synthesis Markup Language)
    ssml_parts = ['<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">']
    
    for i, (character, text) in enumerate(dialogues):
        voice = get_voice_for_character(character)
        
        # 第一句前加一个短停顿，句间停顿
        if i > 0:
            ssml_parts.append(f'<break time="400ms"/>')
        
        ssml_parts.append(f'<voice name="{voice}">')
        ssml_parts.append(f'<prosody rate="{DIALOGUE_RATE}">{text}</prosody>')
        ssml_parts.append('</voice>')
    
    ssml_parts.append('</speak>')
    ssml_content = '\n'.join(ssml_parts)
    
    # 也保存一份SSML文件方便调试（可选）
    # ssml_path = output_path.with_suffix('.ssml')
    # ssml_path.write_text(ssml_content, encoding='utf-8')
    
    try:
        communicate = edge_tts.Communicate(ssml_content, voice=DEFAULT_VOICE)
        await communicate.save(str(output_path))
        
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"  [OK] {output_path.name} ({file_size:.1f}KB, {len(dialogues)} turns)")
        return True
        
    except Exception as e:
        print(f"  [ERROR] {word}: {e}")
        return False


async def process_word(word_data, global_index, day_num):
    """处理单个单词：生成其老友记对话的音频"""
    word = word_data['word']
    friends_scene = word_data.get('friends_scene', '')
    
    if not friends_scene:
        return None
    
    # 解析对话
    dialogues = parse_dialogue(friends_scene)
    if not dialogues:
        return None
    
    # 创建输出目录
    day_dir = AUDIO_OUTPUT / f"day{day_num:03d}"
    day_dir.mkdir(parents=True, exist_ok=True)
    
    # 输出文件路径
    output_path = day_dir / f"{word}_clip.mp3"
    
    success = await generate_dialogue_audio(dialogues, output_path, word)
    
    if success:
        return {
            'word': word,
            'index': global_index,
            'audio_file': str(output_path.relative_to(SCRIPT_DIR)),
            'characters': list(set(d[0] for d in dialogues)),
            'turns': len(dialogues),
        }
    return None


async def generate_day_audio(day_num, words):
    """生成某一天所有单词的老友记对话音频"""
    print(f"\n{'='*50}")
    print(f"🎬 Generating Friends audio for Day {day_num}")
    print(f"   Words: {len(words)}")
    print(f"{'='*50}")
    
    results = []
    for i, w in enumerate(words):
        global_idx = (day_num - 1) * 10 + i + 1
        print(f"  [{i+1}/{len(w)}] #{global_idx} \"{w['word']}\"...")
        result = await process_word(w, global_idx, day_num)
        if result:
            results.append(result)
    
    print(f"\n✅ Day {day_num}: {len(results)}/{len(words)} audio files generated")
    return results


async def main_async():
    """主逻辑"""
    args = sys.argv[1:]
    
    # --list-voices: 列出可用音色
    if '--list-voices' in args:
        print("\n🎭 老友记角色音色映射 (Edge TTS):\n")
        for char, voice in CHARACTER_VOICES.items():
            print(f"  {char:12s} → {voice}")
        print(f"\n  {'默认':12s} → {DEFAULT_VOICE}")
        return
    
    # --test: 测试模式
    if '--test' in args:
        words = load_words()
        test_word = words[0]  # 第一个词 "a"
        print(f"\n🧪 Testing audio generation for: '{test_word['word']}'")
        print(f"Dialogue:\n{test_word['friends_scene']}\n")
        
        AUDIO_OUTPUT.mkdir(parents=True, exist_ok=True)
        test_output = AUDIO_OUTPUT / "_test_clip.mp3"
        
        dialogues = parse_dialogue(test_word['friends_scene'])
        print(f"Parsed: {dialogues}\n")
        
        success = await generate_dialogue_audio(dialogues, test_output, test_word['word'])
        if success:
            print(f"\n🎉 Test successful! Play: {test_output}")
        return
    
    # 加载词库
    words = load_words()
    total_words = len(words)
    total_days = (total_words + 9) // 10
    
    print(f"""
╔══════════════════════════════════════╗
║  🎬 老友记对话音频生成器 v1.0        ║
║  Friends Scene Audio Generator      ║
╠══════════════════════════════════════╣
║  词库:     {total_words:>5} 个单词              ║
║  天数:     {total_days:>5} 天                  ║
║  角色音色: {len(CHARACTER_VOICES):>5} 个                  ║
║  输出目录: audio/friends/              ║
╚══════════════════════════════════════╝
""")
    
    # 确定要生成的天数
    if args and args[0].isdigit():
        day_num = int(args[0])
        start_day = end_day = day_num
    else:
        start_day = 1
        end_day = total_days
    
    # 创建输出根目录
    AUDIO_OUTPUT.mkdir(parents=True, exist_ok=True)
    
    # 逐天生成
    all_results = []
    for day in range(start_day, end_day + 1):
        start_idx = (day - 1) * 10
        end_idx = min(start_idx + 10, total_words)
        day_words = words[start_idx:end_idx]
        
        if not day_words:
            break
        
        results = await generate_day_audio(day, day_words)
        all_results.extend(results)
    
    # 生成汇总报告
    report_path = AUDIO_OUTPUT / "_audio_manifest.json"
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_files': len(all_results),
        'days_covered': f"{start_day}-{end_day}",
        'files': all_results,
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"""
{'='*50}
Done! Generated {len(all_results)} audio files.
Report: {report_path.name}
Output: audio/friends/
""")


def main():
    if '--test' in sys.argv[1:]:
        asyncio.run(test_single())
    else:
        asyncio.run(main_async())


async def test_single():
    """快速测试单个词"""
    words = load_words()
    test_word = words[0]
    
    print(f"\n🧪 Testing: '{test_word['word']}'")
    print(f"Scene: {test_word['friends_scene'][:80]}...\n")
    
    AUDIO_OUTPUT.mkdir(parents=True, exist_ok=True)
    test_output = AUDIO_OUTPUT / "_test_clip.mp3"
    
    dialogues = parse_dialogue(test_word['friends_scene'])
    print(f"解析到 {len(dialogues)} 轮对话:")
    for char, text in dialogues:
        voice = get_voice_for_character(char)
        print(f"  {char} ({voice}): {text[:50]}")
    
    success = await generate_dialogue_audio(dialogues, test_output, test_word['word'])
    
    if success:
        size_kb = test_output.stat().st_size / 1024
        print(f"\n✅ 测试成功! 文件大小: {size_kb:.1f}KB")
        print(f"   路径: {test_output}")


if __name__ == "__main__":
    main()
