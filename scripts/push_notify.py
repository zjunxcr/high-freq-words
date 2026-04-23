#!/usr/bin/env python3
"""
推送通知脚本 - Push Notification Script
支持飞书 Webhook 和微信 Server酱 推送
"""

import json
import sys
import argparse
import requests
from datetime import datetime


def send_feishu(webhook_url, title, content, msg_url=""):
    """发送飞书群消息"""
    if not webhook_url:
        print("[SKIP] FEISHU_WEBHOOK_URL not set")
        return False
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📚 {title}"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    
    # 如果有链接，增加按钮
    if msg_url:
        payload["card"]["elements"].append({
            "tag": "action",
            "actions": [{
                "tag": "button",
                "text": {"tag": "plain_text", "content": "📖 打开学习页面"},
                "url": msg_url,
                "type": "primary"
            }]
        })
    
    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        result = resp.json()
        if result.get("code") == 0 or resp.status_code == 200:
            print("[OK] Feishu notification sent!")
            return True
        else:
            print(f"[ERROR] Feishu: {result}")
            return False
    except Exception as e:
        print(f"[ERROR] Feishu error: {e}")
        return False


def send_wechat(serverchan_key, title, content, msg_url=""):
    """通过 Server酱 推送到微信"""
    if not serverchan_key:
        print("[SKIP] SERVERCHAN_KEY not set")
        return False
    
    url = f"https://sctapi.ftqq.com/{serverchan_key}.send"
    # 构建描述：内容 + 链接按钮
    desp = content.replace("\n", "\n\n> ")
    if msg_url:
        desp += f"\n\n---\n👉 [打开学习页面]({msg_url})"
    data = {
        "title": title,
        "desp": desp
    }
    if msg_url:
        data["url"] = msg_url
    
    try:
        resp = requests.post(url, data=data, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print("[OK] WeChat notification sent!")
            return True
        else:
            print(f"[ERROR] WeChat: {result}")
            return False
    except Exception as e:
        print(f"[ERROR] WeChat error: {e}")
        return False


def build_message(day_num, date_str):
    """构建推送消息内容"""
    # 读取词库获取当天单词预览
    try:
        import json as _json
        from pathlib import Path
        
        data_file = Path(__file__).parent.parent / "data" / "frequency_1000.json"
        with open(data_file, 'r', encoding='utf-8') as f:
            all_words = _json.load(f)
        
        start_idx = (day_num - 1) * 10
        day_words = all_words[start_idx:start_idx + 10]
        
        word_list = []
        for w in day_words:
            word_list.append(
                f"**{w['word']}** {w['phonetic']}\n"
                f"> {w['meaning']}\n"
                f"> 📝 {w['sentence']}\n"
                f"> 🇨🇳 {w['sentence_cn']}\n"
            )
        
        words_preview = "\n\n".join(word_list)
        
    except Exception as e:
        print(f"[WARN] Could not load word list: {e}")
        words_preview = "(加载词库失败，请打开HTML查看)"
    
    title = f"🔤 高频词汇 Day {day_num} | {date_str}"
    
    content = (
        f"## 📚 今日学习：第{day_num}天（第{(day_num-1)*10+1}-{day_num*10}词）\n\n"
        f"{words_preview}\n\n"
        f"---\n"
        f"💡 **今日提示**：先听发音，跟读3遍，再看例句理解用法！\n\n"
        f"🎬 **老友记片段**：今天有1个Friends场景对话等你发现~\n\n"
        f"_基于龙飞虎6个月法 | 1000高频词 = 85%日常沟通_"
    )
    
    return title, content


def main():
    parser = argparse.ArgumentParser(description='Push notifications')
    parser.add_argument('channel', choices=['feishu', 'wechat', 'all'],
                        help='通知渠道')
    parser.add_argument('--day', type=int, required=True, help='天数')
    parser.add_argument('--date', required=True, help='日期 YYYY-MM-DD')
    parser.add_argument('--url', default='', help='HTML页面URL')
    args = parser.parse_args()
    
    title, content = build_message(args.day, args.date)
    
    success = True
    
    if args.channel in ('feishu', 'all'):
        import os
        wh_url = os.environ.get('FEISHU_WEBHOOK_URL', '')
        if not send_feishu(wh_url, title, content, args.url):
            success = False
    
    if args.channel in ('wechat', 'all'):
        import os
        key = os.environ.get('SERVERCHAN_KEY', '')
        if not send_wechat(key, title, content, args.url):
            success = False
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
