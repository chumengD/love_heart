# 微信模块运行状态和行为函数。
# 数据怎么写看 data/wechat_data.rpy，界面怎么画看 screens/wechat_screens.rpy。
# 这里负责把“点击选项、输入文本、切换朋友圈、点赞”等动作转成 Ren'Py 状态变化。

# 当前左侧栏显示哪个页面："chat" 是聊天页，"moments" 是朋友圈页。
default wx_current_view = "chat"

# 当前聊天模式："scripted" 是剧本选项推进版，"free" 是输入框自由聊天版。
default wx_active_chat_mode = "scripted"

# 当前聊天 id。对应 data/wechat_data.rpy 里的 wx_scripted_chats 或 wx_free_chats 的 key。
default wx_active_chat_id = "1"

# 当前剧本节点 id。只在 scripted 模式下使用，对应 wx_scripted_chats[chat_id]["nodes"] 的 key。
default wx_active_node_id = "1"

# 当前屏幕上已经出现的聊天记录。
# 用 default 保存，是为了让存档和回滚能记录当前聊天进度。
default wx_chat_messages = []

# 自由输入框里的临时文本。
default wx_free_input_text = ""

# 朋友圈点赞状态，格式是 {"post_id": True/False}。
# 这里只影响红心显示，不调用 lc_add_affection()，不会影响剧情和结局。
default wx_moment_likes = {}

init python:
    # 通用数字 clamp 工具。
    # 微信自由输入评分用它限制在 -10 到 +10；剧本选项好感变化也会先转成整数。
    def wx_clamp(value, min_value, max_value):
        try:
            numeric_value = int(value)
        except (TypeError, ValueError):
            numeric_value = 0

        return max(min_value, min(max_value, numeric_value))


    # 清理图片路径。
    # 用户示例里可能写 @D:\xxx 这种外部路径；真正给 Ren'Py add 时只接受 game/ 下相对路径。
    # 目前外部绝对路径不会直接加载，应该先把图片复制进 game/images/wechat/ 再填写相对路径。
    def wx_clean_image_path(image_path):
        if not image_path:
            return ""

        clean_path = str(image_path)

        if clean_path.startswith("@"):
            clean_path = clean_path[1:]

        return clean_path


    # 判断图片是否可以被 Ren'Py 读取。
    # 绝对路径会返回 False，避免打包后失效；缺图时界面会显示色块或“图片未放入”。
    def wx_image_loadable(image_path):
        clean_path = wx_clean_image_path(image_path)

        if not clean_path:
            return False

        if ":" in clean_path or clean_path.startswith("/") or clean_path.startswith("\\"):
            return False

        return renpy.loadable(clean_path)


    # 读取联系人配置。
    # 如果 contact_id 写错，会退回默认女主配置，避免界面崩掉。
    def wx_get_contact(contact_id):
        return wx_contacts.get(contact_id, wx_contacts.get(WX_DEFAULT_CONTACT_ID, {}))


    # 联系人显示名。朋友圈作者和头像缺图首字都依赖它。
    def wx_contact_name(contact_id):
        return wx_get_contact(contact_id).get("name", str(contact_id))


    # 联系人头像路径。以后换头像只改 data/wechat_data.rpy 的 avatar 字段。
    def wx_contact_avatar(contact_id):
        return wx_get_contact(contact_id).get("avatar", "")


    # 联系人聊天气泡方向。
    # 现在按你的要求：女主 right，男主 left；如果以后想恢复常见微信布局，只改数据表 side 字段。
    def wx_contact_side(contact_id):
        return wx_get_contact(contact_id).get("side", "left")


    # 头像图片缺失时的兜底颜色。
    def wx_contact_color(contact_id):
        return wx_get_contact(contact_id).get("fallback_color", "#b8c4d1")


    # 头像图片缺失时显示联系人名字第一个字，方便开发阶段定位是谁。
    def wx_avatar_initial(contact_id):
        name = wx_contact_name(contact_id)
        if name:
            return name[0]

        return "?"


    # 根据消息 speaker 查出这一条消息应该显示在左边还是右边。
    def wx_message_side(message):
        return wx_contact_side(message.get("speaker", WX_DEFAULT_CONTACT_ID))


    # 读取剧本聊天。
    # chat_id 对应 data/wechat_data.rpy 里的 wx_scripted_chats key。
    def wx_get_scripted_chat(chat_id):
        return wx_scripted_chats.get(str(chat_id), {})


    # 读取剧本聊天节点。
    # node_id 对应 wx_scripted_chats[chat_id]["nodes"] 里的 key。
    def wx_get_scripted_node(chat_id, node_id):
        chat = wx_get_scripted_chat(chat_id)
        return chat.get("nodes", {}).get(str(node_id), {})


    # 追加一条聊天消息到当前聊天记录。
    # 注意这里会复制 list 再赋值，方便 Ren'Py 的存档/回滚系统识别状态变化。
    def wx_append_message(speaker, text):
        global wx_chat_messages

        if not text:
            return

        next_messages = list(wx_chat_messages)
        next_messages.append({
            "speaker": speaker,
            "text": str(text),
        })
        wx_chat_messages = next_messages


    # 批量追加消息。剧本节点的 messages 和选项后的 reply_messages 都走这里。
    def wx_append_messages(messages):
        for message in messages or []:
            wx_append_message(
                message.get("speaker", WX_DEFAULT_CONTACT_ID),
                message.get("text", ""),
            )


    # 打开剧本选项推进聊天。
    # 剧情里调用示例：
    # $ wx_start_scripted_chat("1", "1")
    # call screen wx_phone
    # 第一个参数是 chat_id，第二个参数是 node_id；不传 node_id 时会用数据里的 start_node。
    def wx_start_scripted_chat(chat_id="1", node_id=None):
        global wx_current_view
        global wx_active_chat_mode
        global wx_active_chat_id
        global wx_active_node_id
        global wx_chat_messages

        chat_key = str(chat_id)
        chat = wx_get_scripted_chat(chat_key)
        start_node = str(node_id or chat.get("start_node", "1"))

        wx_current_view = "chat"
        wx_active_chat_mode = "scripted"
        wx_active_chat_id = chat_key
        wx_active_node_id = start_node
        wx_chat_messages = []
        wx_append_messages(wx_get_scripted_node(chat_key, start_node).get("messages", []))


    # 获取当前节点底部可点选项。
    # screen wx_scripted_choice_bar() 会调用它来生成按钮。
    def wx_current_scripted_choices():
        if wx_active_chat_mode != "scripted":
            return []

        node = wx_get_scripted_node(wx_active_chat_id, wx_active_node_id)
        return node.get("choices", [])


    # 玩家点击剧本选项后的统一入口。
    # 做的事按顺序是：
    # 1. 把 player_text 追加成男主气泡。
    # 2. 读取 affection_delta，并调用隐藏好感度系统 lc_add_affection()。
    # 3. 追加女主 reply_messages。
    # 4. 如果配置了 next_label，直接跳剧情 label；否则按 next 切到下一个聊天节点。
    def wx_choose_scripted_option(choice_index):
        global wx_active_node_id

        choices = wx_current_scripted_choices()

        if choice_index < 0 or choice_index >= len(choices):
            return

        choice = choices[choice_index]
        wx_append_message(WX_PLAYER_CONTACT_ID, choice.get("player_text", choice.get("text", "")))

        # 剧本选项的好感变化只从数据字段 affection_delta 来。
        # 这里不新建微信自己的好感度变量，只调用方案一的 lc_add_affection()。
        affection_delta = wx_clamp(choice.get("affection_delta", 0), -100, 100)
        if affection_delta:
            lc_add_affection(
                affection_delta,
                source="wechat:{0}:{1}:choice:{2}".format(
                    wx_active_chat_id,
                    wx_active_node_id,
                    choice_index,
                ),
            )

        wx_append_messages(choice.get("reply_messages", []))

        # next_label 用于从微信选项直接跳回某段剧情。
        # 数据示例：{"next_label": "chapter_02_after_wechat"}。
        # 如果你只想继续聊天节点，就不要写 next_label，写 next 即可。
        next_label = choice.get("next_label", "")
        if next_label:
            renpy.jump(next_label)
            return

        # next 是同一个 chat_id 内部的下一个 node_id。
        # 切换后会自动把新节点 messages 追加到聊天记录。
        next_node = choice.get("next", "")
        if next_node:
            wx_active_node_id = str(next_node)
            wx_append_messages(wx_get_scripted_node(wx_active_chat_id, wx_active_node_id).get("messages", []))


    # 读取自由聊天配置。
    def wx_get_free_chat(chat_id):
        return wx_free_chats.get(str(chat_id), {})


    # 打开自由输入聊天。
    # 剧情里调用示例：
    # $ wx_start_free_chat("91")
    # call screen wx_phone
    # chat_id 对应 data/wechat_data.rpy 里的 wx_free_chats key。
    def wx_start_free_chat(chat_id="91"):
        global wx_current_view
        global wx_active_chat_mode
        global wx_active_chat_id
        global wx_active_node_id
        global wx_chat_messages
        global wx_free_input_text

        chat_key = str(chat_id)
        chat = wx_get_free_chat(chat_key)

        wx_current_view = "chat"
        wx_active_chat_mode = "free"
        wx_active_chat_id = chat_key
        wx_active_node_id = ""
        wx_chat_messages = []
        wx_free_input_text = ""
        wx_append_messages(chat.get("initial_messages", []))


    # 当前自由聊天上下文。
    # 评分函数和 AI 回复函数都接收同一份 context，后续接 Ollama 时可以把 scene/scoring_rule 作为提示词材料。
    def wx_active_free_context():
        return wx_get_free_chat(wx_active_chat_id).get("context", {})


    # 自由输入评分函数。
    # 它只负责算“这句话该加减多少好感”，不负责生成女主回复。
    # 以后想调整评分，就改 data/wechat_data.rpy 里的关键词，或替换这个函数内部算法。
    # 返回值必须 clamp 到 -10 到 +10，防止一次输入让好感大幅跳变。
    def wx_score_player_input(text, context):
        score = 0
        normalized_text = (text or "").strip()

        if not normalized_text:
            return 0

        for keyword in context.get("positive_keywords", []):
            if keyword and keyword in normalized_text:
                score += 2

        for keyword in context.get("negative_keywords", []):
            if keyword and keyword in normalized_text:
                score -= 3

        for keyword in context.get("too_intimate_keywords", []):
            if keyword and keyword in normalized_text:
                score -= 2

        if "?" in normalized_text or "？" in normalized_text:
            score += 1

        if len(normalized_text) > 80:
            score -= 1

        return wx_clamp(score, -10, 10)


    # AI 回复生成占位函数。
    # 它只负责“女主怎么回”，不负责好感度评分；好感变化由 wx_score_player_input() 单独处理。
    # 以后接 Ollama 时，只替换这个函数内部逻辑：
    # - 不要把请求地址、模型名硬编码在数据文件里。
    # - 保留 fallback，网络失败时仍能返回一句可显示文本。
    # - 返回值必须是字符串，供 wx_append_message(WX_DEFAULT_CONTACT_ID, reply) 使用。
    def wx_generate_ai_reply(player_text, context):
        # TODO: Keep Ollama integration outside this placeholder.
        # This fallback must stay local and deterministic until a later task wires AI.
        normalized_text = (player_text or "").strip()

        if not normalized_text:
            return "你刚才是不是没发出去？"

        if "发圈" in normalized_text or "一起找" in normalized_text:
            return "嗯……谢谢你愿意陪我找。"

        if "没事" in normalized_text or "别难过" in normalized_text or "我陪你" in normalized_text:
            return "听你这么说，我好像没那么烦了。"

        if "无所谓" in normalized_text or "别烦" in normalized_text:
            return "你这样说我会更不开心。"

        return "我知道了，不过我还是有点在意这件事。"


    # 自由输入点击“发送”或按回车后的统一入口。
    # 做的事按顺序是：
    # 1. 读取输入框文本。
    # 2. 追加男主气泡。
    # 3. 调 wx_score_player_input() 计算本次好感变化，并调用 lc_add_affection()。
    # 4. 调 wx_generate_ai_reply() 得到女主回复并追加气泡。
    # 5. 清空输入框。
    def wx_send_free_chat(text=None):
        global wx_free_input_text

        player_text = wx_free_input_text if text is None else text
        player_text = (player_text or "").strip()

        if not player_text:
            return

        context = wx_active_free_context()
        wx_append_message(WX_PLAYER_CONTACT_ID, player_text)

        # 自由输入每次发送的好感变化必须经过评分函数，并限制在 -10 到 +10。
        # 这里同样只调用 lc_add_affection()，不在微信模块里保存第二套好感度。
        affection_delta = wx_score_player_input(player_text, context)
        if affection_delta:
            lc_add_affection(
                affection_delta,
                source="wechat:{0}:free_input".format(wx_active_chat_id),
            )

        wx_append_message(WX_DEFAULT_CONTACT_ID, wx_generate_ai_reply(player_text, context))
        wx_free_input_text = ""


    # 切换左侧栏页面。
    # "chat" 显示聊天，"moments" 显示朋友圈；其它值会被忽略，避免写错导致空屏。
    def wx_set_view(view_name):
        global wx_current_view

        if view_name in ("chat", "moments"):
            wx_current_view = view_name


    # 切换朋友圈点赞状态。
    # 点赞只改变 wx_moment_likes[post_id] 的 True/False，不调用 lc_add_affection()。
    def wx_toggle_moment_like(post_id):
        global wx_moment_likes

        key = str(post_id)
        next_likes = dict(wx_moment_likes)
        next_likes[key] = not bool(next_likes.get(key, False))
        wx_moment_likes = next_likes


    # 查询某条朋友圈是否已点赞，供屏幕决定显示白心还是红心。
    def wx_is_moment_liked(post_id):
        return bool(wx_moment_likes.get(str(post_id), False))


    # 计算网格行数。当前保留为图片网格布局工具，后续如果要显示页脚高度可复用。
    def wx_grid_rows(item_count, columns):
        if columns <= 0:
            return 0

        return (item_count + columns - 1) // columns


    # 把图片列表切成每行 size 张。
    # 朋友圈 3 张以上图片的网格显示会用它。
    def wx_chunks(items, size):
        if size <= 0:
            return []

        return [items[index:index + size] for index in range(0, len(items), size)]


    # 打开 wx_phone 屏幕时的兜底初始化。
    # 如果剧情忘了先调用 wx_start_scripted_chat() 或 wx_start_free_chat()，这里会按当前模式加载默认聊天。
    def wx_ensure_default_state():
        if wx_chat_messages:
            return

        if wx_active_chat_mode == "free":
            wx_start_free_chat(wx_active_chat_id)
        else:
            wx_start_scripted_chat(wx_active_chat_id, wx_active_node_id)
