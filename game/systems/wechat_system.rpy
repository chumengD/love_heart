# 微信模块运行状态和行为函数。
# 数据怎么写看 data/wechat_data.rpy，界面怎么画看 screens/wechat_screens.rpy。
# 这里负责把“点击推进、点击选项、输入文本、切换朋友圈、点赞、评论”等动作转成 Ren'Py 状态变化。

# 当前左侧栏显示哪个页面："chat" 是聊天页，"moments" 是朋友圈页。
default wx_current_view = "chat"

# 当前聊天模式："scripted" 是剧本选项推进版，"free" 是输入框自由聊天版。
default wx_active_chat_mode = "scripted"

# 当前剧本节点 id。对应 wx_scripted_chat["nodes"] 的 key。
default wx_active_node_id = "1"

# 当前节点已经显示到第几条消息。
# 剧本聊天不再一次性 show 全部消息，而是玩家每点击一次默认文本框推进一条。
default wx_active_message_index = 0

# 当前屏幕上已经出现的聊天记录。
# 用 default 保存，是为了让存档和回滚能记录当前聊天进度。
default wx_chat_messages = []

# 等待逐条显示的消息。自由聊天里女主回复可自动出现，剧本聊天里由玩家点击逐条推进。
default wx_pending_messages = []

# 聊天框自动下滑用的版本号。每追加一条可见消息就递增一次。
default wx_chat_scroll_version = 0
default wx_chat_scrolled_version = -1

# 最近一条微信消息对应的旁白或我的心理。
# 演示流程会把它放进 Ren'Py 默认文本框里显示。
default wx_last_narration = ""

# 自由输入框里的临时文本。
default wx_free_input_text = ""

# 朋友圈点赞状态，格式是 {"post_id": True/False}。
# 这里只影响红心显示，不调用 lc_add_affection()，不会影响剧情和结局。
default wx_moment_likes = {}

# 朋友圈评论状态，格式是 {"post_id": "玩家评论文本"}。
# 这里只显示预设评论，不调用 lc_add_affection()，不会影响剧情和结局。
default wx_moment_comments = {}

default wx_ai_waiting = False


init python:
    import os
    import json
    import requests

    # Deepseek API 配置
    DEEPSEEK_API_KEY = "sk-d099bd19f811464fb98131b9fc084a7d"
    DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

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
    # 当前按微信主视角：我 player 在右侧，女主 heroine 在左侧；如果以后想反过来，只改数据表 side 字段。
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


    # 自由聊天里女主消息逐条出现的间隔。
    WX_HEROINE_MESSAGE_DELAY = 0.75


    def wx_mark_chat_needs_scroll():
        global wx_chat_scroll_version

        wx_chat_scroll_version += 1


    def wx_chat_needs_scroll():
        return wx_chat_scrolled_version != wx_chat_scroll_version


    def wx_mark_chat_scrolled():
        global wx_chat_scrolled_version

        wx_chat_scrolled_version = wx_chat_scroll_version


    def wx_append_visible_message(message):
        global wx_chat_messages

        next_messages = list(wx_chat_messages)
        next_messages.append(message)
        wx_chat_messages = next_messages
        wx_mark_chat_needs_scroll()


    def wx_queue_message(message):
        global wx_pending_messages

        next_pending = list(wx_pending_messages)
        next_pending.append(message)
        wx_pending_messages = next_pending


    def wx_queue_text_message(speaker, text, narration=""):
        if not text:
            return

        message = {
            "speaker": speaker,
            "text": str(text),
        }

        if narration:
            message["narration"] = str(narration)

        wx_queue_message(message)


    def wx_reveal_next_pending_message():
        global wx_pending_messages
        global wx_last_narration

        if not wx_pending_messages:
            return

        next_pending = list(wx_pending_messages)
        message = next_pending.pop(0)
        wx_pending_messages = next_pending
        wx_last_narration = message.get("narration", "")
        wx_append_visible_message(message)
        renpy.restart_interaction()


    # 读取当前剧本聊天节点。
    # node_id 对应 wx_scripted_chat["nodes"] 里的 key。
    def wx_get_scripted_node(node_id=None):
        target_node_id = str(node_id or wx_active_node_id)
        return wx_scripted_chat.get("nodes", {}).get(target_node_id, {})


        
    # 追加一条聊天消息到当前聊天记录。
    # 注意这里会复制 list 再赋值，方便 Ren'Py 的存档/回滚系统识别状态变化。
    def wx_append_message(speaker, text, slow_heroine=True, narration=""):
        if not text:
            return

        message = {
            "speaker": speaker,
            "text": str(text),
        }

        if narration:
            message["narration"] = str(narration)

        if slow_heroine and (speaker == WX_DEFAULT_CONTACT_ID or wx_pending_messages):
            wx_queue_message(message)
        else:
            wx_append_visible_message(message)


    # 追加一条图片表情消息。表情入口会复用聊天气泡布局，只是不显示文字气泡背景。
    def wx_append_sticker(speaker, image):
        if not image:
            return

        wx_append_visible_message({
            "speaker": speaker,
            "image": str(image),
        })


    # 点击奶茶表情包后发送给女主；只触发一次，避免重复刷好感和重复消息。
    def wx_send_milk_tea_sticker():
        global act2_sticker_break

        if act2_sticker_break:
            return

        act2_sticker_break = True
        wx_append_sticker(WX_PLAYER_CONTACT_ID, "images/wechat/milk_tea_sticker.png")
        lc_add_affection(8, source="wechat:sticker:milk_tea")
        wx_append_message(WX_DEFAULT_CONTACT_ID, "你还挺可爱的嘛。")


    # 批量追加消息。自由聊天初始消息和通用追加会走这里。
    def wx_append_messages(messages):
        for message in messages or []:
            wx_append_message(
                message.get("speaker", WX_DEFAULT_CONTACT_ID),
                message.get("text", ""),
                narration=message.get("narration", ""),
            )


    # 打开剧本选项推进聊天。
    # 剧情里调用示例：
    # $ wx_start_scripted_chat()
    # show screen wx_phone
    # call wx_scripted_chat_flow
    # 不再传入编号；如果以后要换起始节点，可以传 node_id。
    def wx_start_scripted_chat(node_id=None):
        global wx_current_view
        global wx_active_chat_mode
        global wx_active_node_id
        global wx_active_message_index
        global wx_chat_messages
        global wx_pending_messages
        global wx_last_narration

        start_node = str(node_id or wx_scripted_chat.get("start_node", "1"))

        wx_current_view = "chat"
        wx_active_chat_mode = "scripted"
        wx_active_node_id = start_node
        wx_active_message_index = 0
        wx_chat_messages = []
        wx_pending_messages = []
        wx_last_narration = ""


    # 当前节点是否还有未显示的微信消息。
    # 演示流程用它决定下一次点击是继续出消息，还是进入选项。
    def wx_scripted_has_next_message():
        node = wx_get_scripted_node()
        return wx_active_message_index < len(node.get("messages", []))


    # 选项后的玩家消息和女主回复会先进入这里，等待默认文本框点击逐条显示。
    def wx_scripted_has_pending_message():
        return wx_active_chat_mode == "scripted" and bool(wx_pending_messages)


    # 显示当前节点的下一条微信消息。
    # 这个函数只追加一条，所以能做到玩家点击一次推进一条。
    # 返回 True 表示成功显示了消息；返回 False 表示当前节点已经没有消息。
    def wx_reveal_next_scripted_message():
        global wx_active_message_index
        global wx_last_narration

        node = wx_get_scripted_node()
        messages = node.get("messages", [])

        if wx_active_message_index >= len(messages):
            wx_last_narration = ""
            return False

        message = messages[wx_active_message_index]
        wx_active_message_index += 1
        wx_append_message(
            message.get("speaker", WX_DEFAULT_CONTACT_ID),
            message.get("text", ""),
            slow_heroine=False,
        )
        wx_last_narration = message.get("narration", "")
        return True


    # 读取最近一条微信消息对应的旁白或我的心理。
    # Ren'Py label 会把这个字符串交给默认文本框显示。
    def wx_get_last_narration():
        return wx_last_narration


    # 获取当前节点底部可点选项。
    # 只有当前节点 messages 全部显示完后才返回 choices；否则返回空列表，不会一直占着底部。
    def wx_current_scripted_choices():
        if wx_active_chat_mode != "scripted":
            return []

        if wx_scripted_has_next_message():
            return []

        if wx_scripted_has_pending_message():
            return []

        node = wx_get_scripted_node()
        return node.get("choices", [])


    # 玩家点击剧本选项后的统一入口。
    # 做的事按顺序是：
    # 1. 把 player_text 放进待显示队列，下一次点击才显示我的气泡。
    # 2. 读取 affection_delta，并调用隐藏好感度系统 lc_add_affection()。
    # 3. 把女主 reply_messages 也放进同一个队列，后续每点击一次只显示一条。
    # 4. 如果配置了 next_label，直接跳剧情 label；否则按 next 切到下一个聊天节点。
    def wx_choose_scripted_option(choice_index):
        global wx_active_node_id
        global wx_active_message_index
        global wx_last_narration

        choices = wx_current_scripted_choices()

        if choice_index < 0 or choice_index >= len(choices):
            return

        choice = choices[choice_index]
        wx_last_narration = ""
        player_text = str(choice.get("player_text", choice.get("text", "")) or "")
        if player_text:
            wx_queue_message({
                "speaker": WX_PLAYER_CONTACT_ID,
                "text": player_text,
            })

        # 剧本选项的好感变化只从数据字段 affection_delta 来。
        # 这里不新建微信自己的好感度变量，只调用方案一的 lc_add_affection()。
        affection_delta = wx_clamp(choice.get("affection_delta", 0), -100, 100)
        if affection_delta:
            lc_add_affection(
                affection_delta,
                source="wechat:choice:{0}".format(choice_index),
            )

        for message in choice.get("reply_messages", []):
            reply_text = str(message.get("text", "") or "")
            if reply_text:
                wx_queue_message({
                    "speaker": message.get("speaker", WX_DEFAULT_CONTACT_ID),
                    "text": reply_text,
                    "narration": message.get("narration", ""),
                })

        # next_label 用于从微信选项直接跳回某段剧情。
        # 数据示例：{"next_label": "chapter_02_after_wechat"}。
        # 如果你只想继续聊天节点，就不要写 next_label，写 next 即可。
        next_label = choice.get("next_label", "")
        if next_label:
            renpy.jump(next_label)
            return

        # next 是当前剧本内部的下一个 node_id。
        # 切换后不会立刻显示新节点消息，下一次点击默认文本框时才逐条显示。
        next_node = choice.get("next", "")
        if next_node:
            wx_active_node_id = str(next_node)
            wx_active_message_index = 0
    # 调用 Deepseek API 生成女主回复
    def wx_call_deepseek(player_text, context):
        """
        调用 Deepseek API 生成女主的回复。
        
        参数：
            player_text: 玩家输入的文本
            context: 聊天上下文（包含场景、角色设定等信息）
        
        返回：
            女主的回复文本
        """
        try:
            # 构建系统提示词
            system_prompt = context.get("system_prompt", "你是我刚认识的女孩子，不过可能发展为恋人，一位可爱温柔的女孩，也有自己的小脾气。你现在发圈丢了，和我诉苦中。回复如微信聊天一般简洁明了，不要过于正式或生硬。")
            scene_info = context.get("scene", "")
            
            system_message = system_prompt
            if scene_info:
                system_message += f"\n当前场景：{scene_info}"
            
            # 直接调用 Deepseek API，使用 requests 库
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": player_text},
                ],
                "temperature": 0.7,
                "max_tokens": 150,
                "stream": False
            }
            
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 提取回复内容
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0].get("message", {}).get("content", "").strip()
                
                # 限制回复长度（微信消息气泡宽度）
                if len(reply) > 150:
                    reply = reply[:150]
                
                return reply if reply else "嗯，我听着呢。"
            
            return "嗯，我听着呢。"
        
        except requests.exceptions.Timeout:
            return "网络有点慢，等等再说吧。"
        except requests.exceptions.ConnectionError:
            return "好像没网了，连不上呢。"
        except Exception as e:
            # 网络错误或 API 异常时，返回备用文本
            print(f"Deepseek 调用出错: {str(e)}")
            return "我现在有点烦，回头再聊吧。"

    # 打开自由输入聊天。
    # 剧情里调用示例：
    # $ wx_start_free_chat()
    # call screen wx_phone
    # 不再传入编号；当前只有一套自由聊天配置。
    def wx_start_free_chat():
        global wx_current_view
        global wx_active_chat_mode
        global wx_active_node_id
        global wx_active_message_index
        global wx_chat_messages
        global wx_pending_messages
        global wx_free_input_text
        global wx_last_narration

        wx_current_view = "chat"
        wx_active_chat_mode = "free"
        wx_active_node_id = ""
        wx_active_message_index = 0
        wx_chat_messages = []
        wx_pending_messages = []
        wx_free_input_text = ""
        wx_last_narration = ""
        wx_append_messages(wx_free_chat.get("initial_messages", []))


    # 当前自由聊天上下文。
    # 评分函数和 AI 回复函数都接收同一份 context，后续接 Ollama 时可以把 scene/scoring_rule 作为提示词材料。
    def wx_active_free_context():
        return wx_free_chat.get("context", {})


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
        normalized_text = (player_text or "").strip()

        if not normalized_text:
            return "你刚才是不是没发出去？"

        # 尝试调用 Deepseek 生成回复
        try:
            ai_reply = wx_call_deepseek(normalized_text, context)
            if ai_reply:
                return ai_reply
        except Exception as e:
            # 如果 Deepseek 调用失败，打印错误并使用 fallback
            print(f"Deepseek 调用异常，使用本地规则: {str(e)}")
        
        # Fallback: 使用本地规则库
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
    # 2. 立即追加我的气泡并清空输入框。
    # 3. 调 wx_score_player_input() 计算本次好感变化，并调用 lc_add_affection()。
    # 4. 刷新界面后用后台线程等待 AI 回复。
    # 5. AI 返回后再从主线程追加女主气泡。
    def wx_send_free_chat(text=None):
        global wx_free_input_text
        global wx_ai_waiting

        if wx_ai_waiting:
            return

        player_text = wx_free_input_text if text is None else text
        player_text = (player_text or "").strip()

        if not player_text:
            return

        context = dict(wx_active_free_context())

        wx_append_message(WX_PLAYER_CONTACT_ID, player_text)
        wx_free_input_text = ""
        wx_ai_waiting = True

        affection_delta = wx_score_player_input(player_text, context)
        if affection_delta:
            lc_add_affection(affection_delta, source="wechat:free_input")

        renpy.restart_interaction()
        renpy.invoke_in_thread(wx_request_ai_reply_thread, player_text, context)


    # wx_send_free_chat 的配套函数1：后台等待 AI 回复。
    def wx_request_ai_reply_thread(player_text, context):
        try:
            reply = wx_generate_ai_reply(player_text, context)
        except Exception as e:
            print(f"AI 回复线程异常: {str(e)}")
            reply = "我现在有点烦，回头再聊吧。"

        renpy.invoke_in_main_thread(wx_receive_ai_reply, reply)


    # wx_send_free_chat 的配套函数2：回到主线程追加女主气泡。
    def wx_receive_ai_reply(reply):
        global wx_ai_waiting

        wx_append_message(WX_DEFAULT_CONTACT_ID, reply)
        wx_ai_waiting = False
        renpy.restart_interaction()

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


    # 查询某条朋友圈是否已点赞，供屏幕决定显示空心还是实心爱心图片。
    def wx_is_moment_liked(post_id):
        return bool(wx_moment_likes.get(str(post_id), False))


    # 写入朋友圈预设评论。
    def wx_add_moment_comment(post_id, comment_text):
        global wx_moment_comments

        key = str(post_id)
        text = str(comment_text).strip()
        if not key or not text:
            return

        next_comments = dict(wx_moment_comments)
        next_comments[key] = text
        wx_moment_comments = next_comments


    # 查询某条朋友圈的玩家评论。
    def wx_moment_comment(post_id):
        return wx_moment_comments.get(str(post_id), "")


    # 判断某条朋友圈当前是否应该展示。
    def wx_should_show_moment_post(post):
        if post.get("unlock_after_act2", False):
            return bool(act2_moments_unlocked)

        return True


    # 把图片列表切成每行 size 张。
    # 朋友圈 3 张以上图片的网格显示会用它。
    def wx_chunks(items, size):
        if size <= 0:
            return []

        return [items[index:index + size] for index in range(0, len(items), size)]


    # 打开 wx_phone 屏幕时的兜底初始化。
    # 如果剧情忘了先初始化，这里会按当前模式加载默认聊天。
    def wx_ensure_default_state():
        if wx_chat_messages or wx_pending_messages:
            return

        if wx_active_chat_mode == "free":
            wx_start_free_chat()
        else:
            wx_start_scripted_chat()


# 剧本聊天演示流程。
# 这里负责把“微信屏幕显示”和“默认文本框点击推进”串起来。
# 进入方式：
# $ wx_start_scripted_chat()
# show screen wx_phone
# call wx_scripted_chat_flow
label wx_scripted_chat_flow:
    while True:
        while wx_scripted_has_pending_message():
            pause
            $ wx_reveal_next_pending_message()
            with dissolve
            $ wx_narration = wx_get_last_narration()
            if wx_narration:
                "[wx_narration]"
            else:
                pause

        while wx_scripted_has_next_message():
            pause
            $ wx_reveal_next_scripted_message()
            with dissolve
            $ wx_narration = wx_get_last_narration()
            if wx_narration:
                "[wx_narration]"
            else:
                pause

        $ wx_choices = wx_current_scripted_choices()

        if wx_choices:
            $ wx_choice_items = [(choice.get("text", ""), choice_index) for choice_index, choice in enumerate(wx_choices)]
            $ wx_choice_result = renpy.display_menu(wx_choice_items)
            $ wx_choose_scripted_option(wx_choice_result)
            with dissolve
            $ wx_narration = wx_get_last_narration()
            if wx_narration:
                "[wx_narration]"
        else:
            return


label wx_click_reveal_pending_message:
    if wx_pending_messages:
        pause
        $ wx_reveal_next_pending_message()
        with dissolve
    return
