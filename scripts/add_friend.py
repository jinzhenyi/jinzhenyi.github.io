#!/usr/bin/env python3
import json
import os
import sys
import requests
from github import Github, GithubException

# ---------- 环境变量 ----------
TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_NAME = os.environ.get('REPO')
ISSUE_NUMBER = int(os.environ.get('ISSUE_NUMBER', 0))
MY_DOMAIN = os.environ.get('MY_DOMAIN', '')

if not all([TOKEN, REPO_NAME, ISSUE_NUMBER, MY_DOMAIN]):
    print("❌ 缺少必要的环境变量")
    sys.exit(1)

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)
issue = repo.get_issue(ISSUE_NUMBER)
user_login = issue.user.login

# ---------- 确保标签存在 ----------
def ensure_label(label_name, color='ffcc00'):
    try:
        repo.get_label(label_name)
    except GithubException as e:
        if e.status == 404:
            repo.create_label(name=label_name, color=color)
        else:
            raise

# 预定义标签（可自行修改颜色）
labels_to_ensure = [
    ('审核通过', '2ecc71'),      # 绿色
    ('返链未存在', 'e74c3c'),    # 红色
    ('链接不通', 'f39c12'),      # 橙色
    ('头像链接不通', 'f1c40f')   # 黄色
]
for name, color in labels_to_ensure:
    ensure_label(name, color)

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

body = issue.body
name = extract_field(body, '站点名称')
homepage = extract_field(body, '站点主页')
friend_page = extract_field(body, '友链页面')
avatar = extract_field(body, '头像链接')
desc = extract_field(body, '一句话描述')

# ---------- 必填校验 ----------
if not all([name, homepage, friend_page]):
    issue.add_to_labels('链接不通')
    issue.create_comment(f"@{user_login} ❌ 缺少必要信息（站点名称、站点主页、友链页面），请全部填写后重新提交。")
    issue.edit(state='closed')
    sys.exit(0)

for url in [homepage, friend_page]:
    if not url.startswith(('http://', 'https://')):
        issue.add_to_labels('链接不通')
        issue.create_comment(f"@{user_login} ❌ 链接格式不正确：{url}，请以 http:// 或 https:// 开头。")
        issue.edit(state='closed')
        sys.exit(0)

# ---------- 工具函数：Ping URL ----------
def ping_url(url, timeout=10):
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        if resp.status_code >= 400:
            resp = requests.get(url, timeout=timeout, stream=True)
            resp.raise_for_status()
        return True, None
    except Exception as e:
        return False, str(e)

# ---------- 1. 检测站点主页 ----------
ok, err = ping_url(homepage)
if not ok:
    issue.add_to_labels('链接不通')
    issue.create_comment(f"@{user_login} ❌ 站点主页无法访问：{err}\n请确认链接有效后重新提交。")
    issue.edit(state='closed')
    sys.exit(0)

# ---------- 2. 检测友链页面 ----------
ok, err = ping_url(friend_page)
if not ok:
    issue.add_to_labels('链接不通')
    issue.create_comment(f"@{user_login} ❌ 友链页面无法访问：{err}\n请确认链接有效后重新提交。")
    issue.edit(state='closed')
    sys.exit(0)

# ---------- 3. 检测头像（如有） ----------
if avatar:
    ok, err = ping_url(avatar)
    if not ok:
        issue.add_to_labels('头像链接不通')
        issue.create_comment(f"@{user_login} ❌ 头像链接无法访问：{err}\n请更换有效头像链接后重新提交。")
        issue.edit(state='closed')
        sys.exit(0)

# ---------- 4. 反链检测（在友链页面中搜索 MY_DOMAIN） ----------
def check_backlink(page_url, domain):
    try:
        resp = requests.get(page_url, timeout=15)
        if resp.status_code != 200:
            return False, f"页面状态码 {resp.status_code}"
        if domain in resp.text:
            return True, "已检测到反链"
        else:
            return False, f"未在页面中找到 `{domain}`"
    except Exception as e:
        return False, f"请求异常: {e}"

backlink_found, msg = check_backlink(friend_page, MY_DOMAIN)
if not backlink_found:
    issue.add_to_labels('返链未存在')
    issue.create_comment(
        f"@{user_login} ❌ 反链检测失败：{msg}\n"
        f"请确保您在 `{friend_page}` 中明确包含了本站链接（包含 `{MY_DOMAIN}`），然后重新提交。"
    )
    issue.edit(state='closed')
    sys.exit(0)

# ---------- 5. 去重 & 写入 JSON ----------
json_path = '_data/friends.json'
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        friends = json.load(f)
else:
    friends = []

if any(f['link'] == homepage for f in friends):
    issue.create_comment(f"@{user_login} ⚠️ 该站点主页已在友链列表中，无需重复添加。")
    issue.edit(state='closed')
    sys.exit(0)

new_friend = {
    "name": name,
    "link": homepage,
    "friend_page": friend_page
}
if avatar:
    new_friend["avatar"] = avatar
if desc:
    new_friend["desc"] = desc

friends.append(new_friend)
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(friends, f, ensure_ascii=False, indent=2)

# ---------- 6. 成功 ----------
issue.add_to_labels('审核通过')
issue.create_comment(
    f"@{user_login} ✅ 友链 `{name}` 已成功添加！\n"
    f"站点主页：{homepage}\n"
    f"友链页面：{friend_page}\n"
    f"欢迎互访！"
)
issue.edit(state='closed')