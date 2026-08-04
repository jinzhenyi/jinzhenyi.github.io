---
title: 友链
permalink: /friends/
layout: single
author_profile: false
---

<style>
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
  .footer-text {
    text-align: center;
    margin-top: 30px;
    font-size: 15px;
    color: #555;
  }
  @media (prefers-color-scheme: dark) {
    .friend-card {
      background: #2d2d2d;
      border-color: #444;
      color: #eee;
    }
    .friend-desc { color: #aaa; }
  }
</style>

<h2 style="text-align: center;">🌟 我的朋友们</h2>

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

<div class="footer-text">
  欢迎交换友链，联系邮箱：<a href="mailto:zhenyi20231221@outlook.com">zhenyi20231221@outlook.com</a>
</div>