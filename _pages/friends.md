---
title: 友链
permalink: /friends/
layout: single
author_profile: false
---

<style>
  /* 页面主标题居中 */
  .page__title {
    text-align: center;
  }

  /* 友链卡片样式 */
  .friend-links {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    margin: 20px 0;
  }
  .friend-card {
    display: flex;
    align-items: center;
    width: 260px;
    padding: 16px 20px;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    text-decoration: none;
    color: #333;
    border: 1px solid #eee;
  }
  .friend-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  }
  .friend-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 14px;
    flex-shrink: 0;
  }
  .friend-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .friend-name {
    font-weight: 600;
    font-size: 16px;
    line-height: 1.4;
  }
  .friend-desc {
    font-size: 13px;
    color: #888;
    margin-top: 2px;
  }

  /* 底部文字 */
  .footer-text {
    text-align: center;
    margin-top: 30px;
    font-size: 15px;
    color: #555;
  }
  .footer-text a {
    color: #0366d6;
    text-decoration: none;
  }
  .footer-text a:hover {
    text-decoration: underline;
  }

  /* 深色模式适配 */
  @media (prefers-color-scheme: dark) {
    .friend-card {
      background: #2d2d2d;
      border-color: #444;
      color: #eee;
    }
    .friend-desc { color: #aaa; }
  }
</style>

<!-- 友链卡片列表 -->
<div class="friend-links">
  {% for friend in site.data.friends %}
    <a href="{{ friend.link }}" class="friend-card" target="_blank" rel="noopener">
      {% if friend.avatar %}
        <img class="friend-avatar" src="{{ friend.avatar }}" alt="{{ friend.name }}" />
      {% endif %}
      <div class="friend-info">
        <span class="friend-name">{{ friend.name }}</span>
        {% if friend.desc %}
          <span class="friend-desc">{{ friend.desc }}</span>
        {% endif %}
      </div>
    </a>
  {% endfor %}
</div>

<!-- 底部引导：申请友链 -->
<div class="footer-text">
  申请友链：<a href="https://github.com/jinzhenyi/jinzhenyi.github.io/issues/new?template=friend_request.yml" target="_blank">提交 GitHub Issue</a>
</div>