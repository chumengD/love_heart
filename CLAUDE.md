# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A Ren'Py visual novel (romance/dating sim) at 1920×1080 resolution, written in Simplified Chinese. The game features a custom WeChat-style messaging system with both scripted (node-based) and free-form (AI-powered) chat modes, plus a hidden affection system that determines which ending the player gets.

## Running the game

Open the project in the Ren'Py Launcher (point it at `D:\renpy_game\prtactice`). Use the Launcher to lint, build distributions, or launch the game. There are no CLI test/build commands — Ren'Py projects are managed through the Launcher GUI.

Ren'Py SDK 路径：`F:\Download\renpy-8.5.2-sdk`（renpy.exe 在此目录下）。

Ren'Py 官方文档：https://www.renpy.org/doc/html/

## File init order (critical for correctness)

Ren'Py loads `.rpy` files in Unicode sort order within each directory. Files use `init offset` to control execution order:

| File | Init offset | Purpose |
|------|------------|---------|
| `game/gui.rpy` | -2 | GUI sizing, colors, fonts, style variables |
| `game/screens.rpy` | -1 | All screen definitions and styles |
| Everything else | 0 (default) | |

This matters because `gui.rpy` must run first so screen styles can reference its variables. Don't add new files with init offsets lower than -2 without understanding this dependency chain.

## Architecture

### Character system (`game/script.rpy`)

Two characters: `m` (我, male protagonist/player, blue `#4874CB`) and `g` (女主, female lead, `#EF939E`). Characters are rendered on a custom `character_front` layer placed above the `screens` layer, so sprites always appear above UI. `define g_right` is a variant for when the heroine needs right-aligned namebox (e.g., alternating dialogue scenes).

### Affection system (`game/systems/affection_system.rpy`)

The hidden affection score lives in `default lc_affection = 0` (range 0–100). All reads/writes go through the `lc_*` functions — never read `lc_affection` directly in story code. Use `lc_add_affection(delta, source="...")` to modify, `lc_get_affection()` to read, `lc_get_affection_tier()` for branching, and `lc_get_ending_key()` for ending routing. Tier thresholds are defined in `game/data/ending_rules.rpy` and map affection ranges to ending keys (`low_affection`, `normal_affection`, `high_affection`, `true_ending`).

### WeChat system (three-file split)

- **`game/data/wechat_data.rpy`** — Static data: contacts table, scripted chat nodes, free chat config (keywords, scoring rules), moments posts. This is the file to edit when changing content.
- **`game/systems/wechat_system.rpy`** — Runtime logic: message display, scripted chat flow, free input scoring (`wx_score_player_input`), AI reply generation via Deepseek API, moments like toggling. All state uses Ren'Py `default` variables so save/load works correctly.
- **`game/screens/wechat_screens.rpy`** — UI rendering: `wx_phone` main screen, sidebar navigation, chat bubbles, avatar component, bottom input bars, moments page, sticker popconfirm.

The WeChat system has two modes triggered by story scripts:
1. **Scripted** (`wx_start_scripted_chat()` + `call wx_scripted_chat_flow`): Messages reveal one-by-one per click, choices appear at node end, affection changes come from `affection_delta` in data.
2. **Free** (`wx_start_free_chat()` + `call screen wx_phone`): Player types freely, input scored by keyword matching, AI generates reply via Deepseek API (with local fallback rules).

### Story structure (`game/story/`)

Acts are called sequentially from `label start` in `script.rpy`: Act1 → Act2 (with WeChat interlude) → Acts 3–5. Acts 3–5 are incomplete/placeholder. Story files use `menu` for branching choices that modify affection.

## Conventions

- All comments are in Chinese and describe design rationale ("why"), not mechanics ("what").
- Use `$ lc_add_affection(N)` in story files for affection changes. Never directly set `lc_affection`.
- New WeChat content goes in `data/wechat_data.rpy`, not in system or screen files.
- The Deepseek API key is embedded in `wechat_system.rpy` — do not commit real keys to public repos.
- Image paths in data should be relative to `game/` (e.g., `"images/wechat/heroine_avatar.png"`).
- `wx_clean_image_path` strips `@` prefix from paths (used in data examples); absolute paths are rejected by `wx_image_loadable`.
- VS Code settings exclude `.rpyc`, `.rpymc`, `.rpa`, and `cache/` from the file tree.
- 只修改用户明确提到的地方，不擅自改动其他结构体、函数或无关代码。

## Git 工作流

- 修改文件前，如果有未提交的改动，先 commit 再开始修改。
- 修改完文件后也要 commit。
- Commit 信息必须用中文写。
- 不要使用 `git add -A` 或 `git add .`，而是按文件名精确暂存。

## 模块拆分规范

- 不要默认把所有代码塞进 `gui.rpy`、`options.rpy`、`screens.rpy`、`script.rpy` 这 4 个模板文件。Ren'Py 会读取 `game/` 目录及其子目录中的 `.rpy` 文件，项目变大时应按职责拆分。
- 默认保留 4 个模板文件的职责：`options.rpy` 放项目配置，`gui.rpy` 放 GUI 基础参数，`screens.rpy` 放默认或通用界面，`script.rpy` 放入口流程和主线跳转。
- 新增内容优先按模块拆分：`characters.rpy` 放角色定义，`defaults.rpy` 放 `default` 存档变量，`story/` 放章节剧情，`screens/` 放自定义界面，`systems/` 放玩法系统逻辑，`data/` 放静态数据。
- 拆分剧情时用清晰的 `label` 配合 `jump` / `call` 串联流程；不要重复定义同名 `label`、`screen`、`transform`、`style` 或 Python 名称。
- 需要固定加载顺序时，用清晰的文件名前缀或 Ren'Py 的 `init` 优先级处理，不要使用 `00_` 这类 Ren'Py 内部保留风格的文件名前缀。
- Python 逻辑较多时优先放在 `.rpy` 的 `init python` 或单独系统文件中；只有纯工具逻辑才考虑普通 `.py` 模块。玩家状态、好感度、背包等需要存档和回滚的数据不要放进普通 `.py` 模块。
- 移动、删除或改名 `.rpy` 文件后，如果旧逻辑仍被执行，检查并清理对应的 `.rpyc` 缓存文件。
- 如需新增文件或目录来完成模块拆分，先列出目标文件清单并征询用户意见，得到确认后再修改。

## 图片生成

- 需要生成图片时，画风参考 `C:\Users\LENOVO\Desktop\flavor` 目录中的图片。
- 输出格式为 PNG。
