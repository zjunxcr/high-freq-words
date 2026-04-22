#!/usr/bin/env python3
"""
批量生成TTS音频：单词发音 + 例句朗读
使用 Edge TTS (Microsoft Neural Voices)
- 慢速0.6x，适合英语学习者
- 生成 mp3 文件，嵌入HTML
"""

import json
import os
import sys
import asyncio
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
DATA_FILE   = SCRIPT_DIR / "data" / "frequency_1000.json"
AUDIO_DIR   = SCRIPT_DIR / "audio" / "tts"

# TTS配置
TTS_VOICE = "en-US-JennyNeural"  # 美式女声，清晰标准
TTS_RATE  = "-20%"                # 慢速（原速为+0%）
# 单词发音更慢，例句稍快
WORD_RATE = "-30%"
SENT_RATE = "-15%"

async def generate_tts(text, output_path, voice=TTS_VOICE, rate=TTS_RATE):
    """用 Edge TTS 生成单个mp3"""
    import edge_tts
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))
    
    # 确认文件存在且非空
    if not output_path.exists() or output_path.stat().st_size < 500:
        print(f"  ⚠️ {output_path.name} 生成异常（文件过小或不存在）", flush=True)
        return False
    size_kb = output_path.stat().st_size / 1024
    print(f"  ✅ {output_path.name} ({size_kb:.1f}KB)", flush=True)
    return True


async def generate_all_audio(start_idx=1, end_idx=1028, force=False):
    """批量生成所有词的TTS音频"""
    import edge_tts
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        words = json.load(f)
    
    print(f"📦 词库共 {len(words)} 个词")
    print(f"🎤 目标范围: #{start_idx} ~ #{end_idx}")
    print(f"🔊 TTS音色: {TTS_VOICE}, 语速: {TTS_RATE}")
    print()
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for i in range(max(0, start_idx-1), min(end_idx, len(words))):
        word_data = words[i]
        word      = word_data['word']
        sentence  = word_data.get('sentence', '')
        idx       = i + 1
        
        # 创建该词的音频目录: audio/tts/word001/
        word_dir = AUDIO_DIR / f"{idx:04d}"
        word_dir.mkdir(parents=True, exist_ok=True)
        
        word_file  = word_dir / f"word.mp3"
        sent_file  = word_dir / f"sentence.mp3"
        
        # === 单词发音 ===
        if not force and word_file.exists() and word_file.stat().st_size > 500:
            skip_count += 1
        else:
            ok = await generate_tts(word, word_file, TTS_VOICE, WORD_RATE)
            if ok:
                success_count += 1
            else:
                fail_count += 1
        
        # === 例句朗读 ===
        if sentence and len(sentence) > 2:
            if not force and sent_file.exists() and sent_file.stat().st_size > 500:
                skip_count += 1
            else:
                ok = await generate_tts(sentence, sent_file, TTS_VOICE, SENT_RATE)
                if ok:
                    success_count += 1
                else:
                    fail_count += 1
        
        # 每10个词打印一次进度
        if idx % 50 == 0 or idx == end_idx:
            total_gen = success_count + fail_count
            print(f"\n📊 进度: #{idx}/{len(words)} | 新增✅{success_count} 失败❌{fail_count} 跳过⏭{skip_count}\n")
        
        # 避免请求过快被限流
        await asyncio.sleep(0.3)
    
    print(f"\n{'='*50}")
    print(f"🏁 完成！新增 {success_count} | 失败 {fail_count} | 跳过 {skip_count}")
    print(f"📁 音频目录: {AUDIO_DIR}")
    
    # 统计总大小
    total_size = sum(f.stat().st_size for f in AUDIO_DIR.rglob("*.mp3") if f.exists())
    print(f"💾 总大小: {total_size / 1024 / 1024:.1f} MB ({success_count + skip_count} 个文件)")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='批量生成TTS音频')
    parser.add_argument('--start', type=int, default=1, help='起始词序号(从1开始)')
    parser.add_argument('--end', type=int, default=99999, help='结束词序号')
    parser.add_argument('--force', action='store_true', help='强制重新生成所有')
    args = parser.parse_args()
    
    print("=" * 55)
    print("  🎙️ High-Freq-Words TTS Audio Generator")
    print("  Edge TTS - Microsoft Neural Voice (Jenny)")
    print("=" * 55)
    
    asyncio.run(generate_all_audio(args.start, args.end, args.force))


if __name__ == "__main__":
    main()
