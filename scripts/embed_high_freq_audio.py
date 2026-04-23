#!/usr/bin/env python3
"""
embed-high-freq-audio.py - 将TTS音频base64内嵌到HTML中
（参考 daily-words 的 embed-daily-words-audio.py 方案）

用法:
  python scripts/embed-high-freq-audio.py [day_num] [date_str]
  # 自动读取 output/ 目录下的HTML，内嵌音频后覆盖保存

原理:
  1. 扫描 HTML 中所有 <audio> 标签的 source src 路径
  2. 读取对应的本地 mp3 文件
  3. 转 base64 data URI，替换 src 属性
  这样浏览器不需要通过网络/文件路径加载音频，直接从HTML内部解码播放
"""

import base64
import sys
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
AUDIO_DIR = SCRIPT_DIR / "audio" / "tts"
OUTPUT_DIR = SCRIPT_DIR / "output"


def embed_audio_to_html(html_path):
    """读取HTML，将所有<audio>标签的外部mp3替换为base64内嵌"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    orig_size = len(html)
    
    # 查找所有 <audio> 标签中的 source src
    pattern = re.compile(
        r'<audio\s+[^>]*id="([^"]+)"[^>]*>.*?<source\s+src="([^"]+)"[^>]*>',
        re.DOTALL
    )
    
    matches = list(pattern.finditer(html))
    
    if not matches:
        print(f"  [SKIP] No audio tags found in {html_path.name}")
        return html, 0
    
    print(f"  Found {len(matches)} audio tags to embed")
    
    embedded = 0
    for m in reversed(matches):  # 反向遍历，避免位置偏移
        audio_id = m.group(1)
        rel_src = m.group(2)  # e.g., "audio/tts/0001/word.mp3"
        
        # 从相对路径找到实际文件
        local_file = SCRIPT_DIR / rel_src
        
        if not local_file.exists():
            print(f"  [WARN] File not found: {local_file} (for {audio_id})")
            continue
        
        # 读取并转base64
        try:
            with open(local_file, 'rb') as mp3:
                b64 = base64.b64encode(mp3.read()).decode('ascii')
            
            data_uri = f"data:audio/mpeg;base64,{b64}"
            old_tag = m.group(0)
            new_tag = old_tag.replace(rel_src, data_uri)
            
            html = html[:m.start()] + new_tag + html[m.end():]
            embedded += 1
            
            size_kb = len(b64) * 3 / 4 / 1024
            print(f"  [{embedded}/{len(matches)}] {audio_id}: {local_file.name} ({size_kb:.1f}KB)")
        except Exception as e:
            print(f"  [ERROR] Failed to embed {audio_id}: {e}")
    
    delta = len(html) - orig_size
    print(f"  Embedded: {embedded}/{len(matches)} | Size change: +{delta/1024:.1f}KB")
    
    return html, embedded


def main():
    day_num = sys.argv[1] if len(sys.argv) > 1 else "1"
    date_str = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 查找目标HTML文件
    if date_str:
        html_name = f"high_freq_words_day{int(day_num):03d}_{date_str}.html"
    else:
        # 自动查找最新的匹配文件
        candidates = sorted(
            OUTPUT_DIR.glob(f"high_freq_words_day{int(day_num):03d}_*.html"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        if candidates:
            html_name = candidates[0].name
        else:
            # 尝试找任何output文件
            all_html = list(OUTPUT_DIR.glob("*.html"))
            if all_html:
                html_name = sorted(all_html, key=lambda p: p.stat().st_mtime, reverse=True)[0].name
            else:
                print("[ERROR] No HTML files found in output/")
                sys.exit(1)
    
    html_path = OUTPUT_DIR / html_name
    if not html_path.exists():
        print(f"[ERROR] File not found: {html_path}")
        sys.exit(1)
    
    print(f"[*] Processing: {html_path.name}")
    print(f"[*] Size: {html_path.stat().st_size / 1024:.1f} KB")
    
    html, count = embed_audio_to_html(html_path)
    
    if count > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        final_size = html_path.stat().st_size / 1024
        print(f"\n[OK] Done! {count} audio files embedded -> {html_name} ({final_size:.1f} KB)")
    else:
        print("\n[WARN] No audio was embedded")


if __name__ == "__main__":
    main()
