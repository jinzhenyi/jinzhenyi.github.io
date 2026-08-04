---
title: 友链
permalink: /friends/
date: 2026-08-04
type: page
---

<h2 style="text-align: center;">🌟 我的朋友们</h2>

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
  /* 只显示名称的卡片（无头像和简介） */
  .friend-card-simple {
    justify-content: center;   /* 内容居中 */
    text-align: center;
  }
  .friend-card-simple .friend-name {
    font-size: 18px;          /* 稍微放大一点，填补空白 */
  }
  @media (prefers-color-scheme: dark) {
    .friend-card {
      background: #2d2d2d;
      border-color: #444;
      color: #eee;
    }
    .friend-desc { color: #aaa; }
  }

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
</style>

<div class="friend-links">

  <!-- woodfish（正常显示头像+简介） -->
  <a href="https://woodfish.site/newBlog/" class="friend-card" target="_blank" rel="noopener">
    <img class="friend-avatar" src="https://pic1.imgdb.cn/item/682f3d1658cb8da5c807b704.jpg" alt="woodfish" />
    <div class="friend-info">
      <span class="friend-name">woodfish</span>
      <span class="friend-desc">我喜欢你</span>
    </div>
  </a>

  <!-- 二叉树树（只显示名称，无头像、无简介） -->
  <a href="https://2x.nz" class="friend-card friend-card-simple" target="_blank" rel="noopener">
    <span class="friend-name">二叉树树</span>
  </a>

</div>

<div class="footer-text">
  欢迎交换友链，联系邮箱：<a href="mailto:zhenyi20231221@outlook.com">zhenyi20231221@outlook.com</a>
</div>