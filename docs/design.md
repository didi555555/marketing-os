# Marketing OS — Design Document

## Overview
All-in-One SaaS Marketing Platform. Open-source, free, modular.
Covers 35 marketing & development skills as plugin modules.

## Tech Stack
- **Backend:** Python + Flask
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Frontend:** HTML + CSS + JS (vanilla, no framework)
- **AI:** Gemini API (free tier)
- **Hosting:** Render/Railway free tier

## Architecture
Monolith with Plugin Architecture.
Core Flask app auto-discovers and loads plugins from `plugins/` directory.

## Phase 1 — Core System
- User auth (register/login/logout)
- SQLite database (users + plugin settings)
- Plugin loader system
- Main dashboard

## Phase 2 — AI Writer
- Copywriting, copy-editing, content strategy, social posts

## Phase 3 — Media Studio
- Image, video, DOCX, PDF, PPTX, XLSX generation, auto-publish

## Phase 4 — SEO & Analytics
- SEO audit, AI-SEO, competitor profiling, marketing psychology

## Phase 5 — Ads & Planning
- Ad manager, marketing planner, product marketing, brainstorming

## Data Flow
```
User → Flask Route → Plugin Router → Plugin Handler → Gemini API / Local Logic → Response
                                   → Database CRUD
                                   → File Generation (DOCX/PDF/etc)
```

## Database Schema (Phase 1)
```sql
users: id, name, email, password_hash, plan, created_at
plugins: id, user_id, plugin_name, enabled, config_json
```
