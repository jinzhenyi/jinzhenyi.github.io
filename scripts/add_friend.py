#!/usr/bin/env python3
import json
import os
import sys
import requests
from github import Github, GithubException

# ---------- 日志函数 ----------
def log(msg):
    print(f"[DEBUG] {msg}")
    sys.stdout.flush()

# ---------- 环境变量 ----------
TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_NAME = os.environ.get('REPO')
ISSUE_NUMBER = int(os.environ.get('ISSUE_NUMBER', 0))
MY_DOMAIN = os.environ.get('MY_DOMAIN', '')

log(f"环境变量: REPO={REPO_NAME}, ISSUE={ISSUE_NUMBER}, DOMAIN={MY_DOMAIN}")

if not all([TOKEN, REPO_NAME, ISSUE_NUMBER, MY_DOMAIN]):
    log("❌ 缺少环境变量")
    sys.exit(1)

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)
issue = repo.get_issue(ISSUE_NUMBER)

# ---------- 解析 Issue 表单 ----------
def extract_field(body, label):
    lines = body.split('\n')
    for i, line in enumerate(lines):
        if label in line and i+1 < len(lines):
            j = i+1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                return lines[j].strip()
    return None

log("开始解析 Issue 正文...")
body = issue.body
log(f"Issue 正文长度: {len(body)} 字符")

name = extract_field(body, '站点名称')
homepage = extract_field(body, '站点主页')
friend_page = extract_field(body, '友链页面')
avatar = extract_field(body, '头像链接')
desc = extract_field(body, '一句话描述')

log(f"解析结果: name={name}, homepage={homepage}, friend_page={friend_page}")

# ---------- 必填校验 ----------
if not all([name, homepage, friend_page]):
    log("❌ 缺少必要字段")
    issue.create_comment("❌ 缺少必要信息（站点名称、站点主页、友链页面）")
    issue.edit(state='closed')
    sys.exit(0)

for url in [homepage, friend_page]:
    if not url.startswith(('http://', 'https://')):
        log(f"❌ URL格式错误: {url}")
        issue.create_comment(f"❌ 链接格式不正确：{url}")
        issue.edit(state='closed')
        sys.exit(0)

# ---------- Ping 检测 ----------
def ping_url(url, timeout=10):
    log(f"Ping URL: {url}")
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        log(f"HEAD 状态码: {resp.status_code}")
        if resp.status_code >= 400:
            log("HEAD 失败，尝试 GET...")
            resp = requests.get(url, timeout=timeout, stream=True)
            log(f"GET 状态码: {resp.status_code}")
            resp.raise_for_status()
        return True, None
    except Exception as e:
        log(f"Ping 异常: {e}")
        return False, str(e)

# 1. 站点主页
log("检查站点主页...")
ok, err = ping_url(homepage)
if not ok:
    log("站点主页不可访问")
    issue.create_comment(f"❌ 站点主页无法访问：{err}")
    issue.add_to_labels('链接不通')
    issue.edit(state='closed')
    sys.exit(0)

# 2. 友链页面
log("检查友链页面...")
ok, err = ping_url(friend_page)
if not ok:
    log("友链页面不可访问")
    issue.create_comment(f"❌ 友链页面无法访问：{err}")
    issue.add_to_labels('链接不通')
    issue.edit(state='closed')
    sys.exit(0)

# 3. 头像（仅当真正填写时检测）
if avatar and avatar.strip() != '':
    log("检查头像链接...")
    ok, err = ping_url(avatar)
    if not ok:
        log("头像链接不可访问")
        issue.create_comment(f"❌ 头像链接无法访问：{err}")
        issue.add_to_labels('头像链接不通')
        issue.edit(state='closed')
        sys.exit(0)
else:
    log("未填写头像，跳过检测")

# ---------- 反链检测 ----------
log(f"开始反链检测，搜索域名: {MY_DOMAIN}")
def check_backlink(page_url, domain):
    log(f"请求页面: {page_url}")
    try:
        resp = requests.get(page_url, timeout=15)
        log(f"页面状态码: {resp.status_code}")
        log(f"页面内容前200字符: {resp.text[:200]}")
        if resp.status_code != 200:
            return False, f"状态码 {resp.status_code}"
        if domain in resp.text:
            return True, "找到反链"
        else:
            return False, f"未找到 `{domain}`"
    except Exception as e:
        log(f"请求异常: {e}")
        return False, f"请求异常: {e}"

backlink_found, msg = check_backlink(friend_page, MY_DOMAIN)
if not backlink_found:
    log(f"反链检测失败: {msg}")
    issue.create_comment(f"❌ 反链检测失败：{msg}")
    issue.add_to_labels('返链未存在')
    issue.edit(state='closed')
    sys.exit(0)

log("反链检测通过 ✅")

# ---------- 更新 JSON（通过 GitHub API） ----------
log("正在更新 _data/friends.json ...")
# 先获取当前文件内容（如果存在）
try:
    contents = repo.get_contents("_data/friends.json")
    current_json = contents.decoded_content.decode('utf-8')
    friends = json.loads(current_json)
    log("已读取现有文件")
except GithubException as e:
    if e.status == 404:
        friends = []
        log("文件不存在，将创建新文件")
    else:
        log(f"读取文件异常: {e}")
        issue.create_comment(f"❌ 读取数据文件失败: {e}")
        sys.exit(1)

# 去重
if any(f.get('link') == homepage for f in friends):
    log("站点已存在")
    issue.create_comment("⚠️ 该站点已在友链列表中")
    issue.edit(state='closed')
    sys.exit(0)

# 构造新条目
new_friend = {"name": name, "link": homepage, "friend_page": friend_page}
if avatar and avatar.strip() != '':
    new_friend["avatar"] = avatar
if desc:
    new_friend["desc"] = desc

friends.append(new_friend)
json_str = json.dumps(friends, ensure_ascii=False, indent=2)

# 写入文件（更新或创建）
try:
    if 'contents' in locals() and contents:
        repo.update_file(contents.path, f"docs: 添加友链 {name}", json_str, contents.sha, branch=repo.default_branch)
    else:
        repo.create_file("_data/friends.json", f"docs: 添加友链 {name}", json_str, branch=repo.default_branch)
    log("✅ JSON 文件更新成功")
except Exception as e:
    log(f"❌ 更新文件失败: {e}")
    issue.create_comment(f"❌ 更新友链数据失败: {e}")
    sys.exit(1)

# ---------- 成功 ----------
issue.add_to_labels('审核通过')
issue.create_comment(f"✅ 友链 `{name}` 已成功添加！")
issue.edit(state='closed')
log("处理完成 🎉")