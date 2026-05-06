# WeChat module runtime state and actions.

default wx_current_view = "chat"
default wx_active_chat_mode = "scripted"
default wx_active_chat_id = "1"
default wx_active_node_id = "1"
default wx_chat_messages = []
default wx_free_input_text = ""
default wx_moment_likes = {}

init python:
    def wx_clamp(value, min_value, max_value):
        try:
            numeric_value = int(value)
        except (TypeError, ValueError):
            numeric_value = 0

        return max(min_value, min(max_value, numeric_value))


    def wx_clean_image_path(image_path):
        if not image_path:
            return ""

        clean_path = str(image_path)

        if clean_path.startswith("@"):
            clean_path = clean_path[1:]

        return clean_path


    def wx_image_loadable(image_path):
        clean_path = wx_clean_image_path(image_path)

        if not clean_path:
            return False

        if ":" in clean_path or clean_path.startswith("/") or clean_path.startswith("\\"):
            return False

        return renpy.loadable(clean_path)


    def wx_get_contact(contact_id):
        return wx_contacts.get(contact_id, wx_contacts.get(WX_DEFAULT_CONTACT_ID, {}))


    def wx_contact_name(contact_id):
        return wx_get_contact(contact_id).get("name", str(contact_id))


    def wx_contact_avatar(contact_id):
        return wx_get_contact(contact_id).get("avatar", "")


    def wx_contact_side(contact_id):
        return wx_get_contact(contact_id).get("side", "left")


    def wx_contact_color(contact_id):
        return wx_get_contact(contact_id).get("fallback_color", "#b8c4d1")


    def wx_avatar_initial(contact_id):
        name = wx_contact_name(contact_id)
        if name:
            return name[0]

        return "?"


    def wx_message_side(message):
        return wx_contact_side(message.get("speaker", WX_DEFAULT_CONTACT_ID))


    def wx_get_scripted_chat(chat_id):
        return wx_scripted_chats.get(str(chat_id), {})


    def wx_get_scripted_node(chat_id, node_id):
        chat = wx_get_scripted_chat(chat_id)
        return chat.get("nodes", {}).get(str(node_id), {})


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


    def wx_append_messages(messages):
        for message in messages or []:
            wx_append_message(
                message.get("speaker", WX_DEFAULT_CONTACT_ID),
                message.get("text", ""),
            )


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


    def wx_current_scripted_choices():
        if wx_active_chat_mode != "scripted":
            return []

        node = wx_get_scripted_node(wx_active_chat_id, wx_active_node_id)
        return node.get("choices", [])


    def wx_choose_scripted_option(choice_index):
        global wx_active_node_id

        choices = wx_current_scripted_choices()

        if choice_index < 0 or choice_index >= len(choices):
            return

        choice = choices[choice_index]
        wx_append_message(WX_PLAYER_CONTACT_ID, choice.get("player_text", choice.get("text", "")))

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

        next_label = choice.get("next_label", "")
        if next_label:
            renpy.jump(next_label)
            return

        next_node = choice.get("next", "")
        if next_node:
            wx_active_node_id = str(next_node)
            wx_append_messages(wx_get_scripted_node(wx_active_chat_id, wx_active_node_id).get("messages", []))


    def wx_get_free_chat(chat_id):
        return wx_free_chats.get(str(chat_id), {})


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


    def wx_active_free_context():
        return wx_get_free_chat(wx_active_chat_id).get("context", {})


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


    def wx_send_free_chat(text=None):
        global wx_free_input_text

        player_text = wx_free_input_text if text is None else text
        player_text = (player_text or "").strip()

        if not player_text:
            return

        context = wx_active_free_context()
        wx_append_message(WX_PLAYER_CONTACT_ID, player_text)

        affection_delta = wx_score_player_input(player_text, context)
        if affection_delta:
            lc_add_affection(
                affection_delta,
                source="wechat:{0}:free_input".format(wx_active_chat_id),
            )

        wx_append_message(WX_DEFAULT_CONTACT_ID, wx_generate_ai_reply(player_text, context))
        wx_free_input_text = ""


    def wx_set_view(view_name):
        global wx_current_view

        if view_name in ("chat", "moments"):
            wx_current_view = view_name


    def wx_toggle_moment_like(post_id):
        global wx_moment_likes

        key = str(post_id)
        next_likes = dict(wx_moment_likes)
        next_likes[key] = not bool(next_likes.get(key, False))
        wx_moment_likes = next_likes


    def wx_is_moment_liked(post_id):
        return bool(wx_moment_likes.get(str(post_id), False))


    def wx_grid_rows(item_count, columns):
        if columns <= 0:
            return 0

        return (item_count + columns - 1) // columns


    def wx_chunks(items, size):
        if size <= 0:
            return []

        return [items[index:index + size] for index in range(0, len(items), size)]


    def wx_ensure_default_state():
        if wx_chat_messages:
            return

        if wx_active_chat_mode == "free":
            wx_start_free_chat(wx_active_chat_id)
        else:
            wx_start_scripted_chat(wx_active_chat_id, wx_active_node_id)
