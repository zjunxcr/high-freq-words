#!/usr/bin/env python3
"""通过 GitHub API 推送文件，绕过 git push

用法:
  python scripts/api_push.py                          # 推送 FILES 列表
  python scripts/api_push.py data/frequency_1000.json  # 推送指定文件

环境变量:
  GITHUB_TOKEN - GitHub PAT (必填，不再硬编码)
"""
import urllib.request
import json
import ssl
import base64
import os
import sys
from pathlib import Path


def get_token():
    """从环境变量获取Token（优先级：GITHUB_TOKEN > GH_TOKEN）"""
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        print("[ERROR] GITHUB_TOKEN or GH_TOKEN environment variable required")
        print("  Usage: set GITHUB_TOKEN=ghp_xxxx && python scripts/api_push.py")
        sys.exit(1)
    return token


REPO = "zjunxcr/high-freq-words"
HEADERS_TEMPLATE = lambda token: {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}
ctx = ssl.create_default_context()

# 基础目录：脚本所在项目的根目录（相对路径）
BASE = Path(__file__).parent.parent.resolve()

# 默认推送文件列表（可通过命令行覆盖）
DEFAULT_FILES = [
    "data/frequency_1000.json",
]

# 自动扫描 output/ 目录下所有HTML文件
OUTPUT_DIR = BASE / "output"


def auto_scan_output_files():
    """扫描 output/ 下所有 .html 文件"""
    if OUTPUT_DIR.exists():
        html_files = sorted(OUTPUT_DIR.glob("*.html"))
        return [f.relative_to(BASE).as_posix() for f in html_files]
    return []


def push_file(remote_path, token, headers):
    local_path = BASE / remote_path.replace("/", os.sep)
    
    if not local_path.exists():
        print(f"  [SKIP] File not found: {local_path}")
        return False
    
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    # Get existing SHA
    url = f"https://api.github.com/repos/{REPO}/contents/{remote_path}"
    sha = None
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            sha = json.loads(r.read()).get("sha")
        if sha:
            print(f"  [SHA] {remote_path} -> {sha[:8]}")
        else:
            print(f"  [NEW] {remote_path}")
    except Exception as e:
        print(f"  [NEW] {remote_path} ({e})")
    
    # Push via API
    body = {"message": f"update: {remote_path}", "content": content}
    if sha:
        body["sha"] = sha
    
    payload = json.dumps(body).encode()
    req2 = urllib.request.Request(url, data=payload, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req2, timeout=20, context=ctx) as r:
            resp = json.loads(r.read())
            commit_msg = resp.get("commit", {}).get("message", "")[:60]
            print(f"  [OK]  {remote_path} -> {commit_msg}")
            return True
    except Exception as e:
        print(f"  [ERR] {remote_path}: {e}")
        return False


def main():
    token = get_token()
    headers = HEADERS_TEMPLATE(token)
    
    # 确定要推送的文件列表
    if len(sys.argv) > 1:
        # 命令行指定文件
        files = sys.argv[1:]
    else:
        # 默认：词库 + 扫描output目录所有HTML
        files = list(DEFAULT_FILES)
        files.extend(auto_scan_output_files())
    
    if not files:
        print("[WARN] No files to push")
        return
    
    print(f"Pushing {len(files)} file(s) via GitHub API...")
    print(f"  Repo: {REPO}")
    print(f"  Base: {BASE}")
    print()
    
    ok = 0
    for fp in files:
        if push_file(fp, token, headers):
            ok += 1
    print(f"\nDone: {ok}/{len(files)} files pushed")


if __name__ == "__main__":
    main()
