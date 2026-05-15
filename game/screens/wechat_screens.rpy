# 微信模块界面。
# 这里只负责“画出来”：左侧栏、聊天记录、自由输入框、朋友圈列表。
# 数据来源在 data/wechat_data.rpy，点击后的行为函数在 systems/wechat_system.rpy。

# 新微信消息出现时的淡入效果。
# 每条消息对应的 hbox show 时都会从透明过渡到不透明，满足“微信聊天信息 show 时 dissolve”的需求。
transform wx_message_dissolve:
    on show:
        alpha 0.0
        linear 0.25 alpha 1.0

default wx_phone_standalone_modal = False

# 主微信屏幕。
# 剧本聊天演示：
# $ wx_start_scripted_chat()
# show screen wx_phone
# call wx_scripted_chat_flow
# 自由聊天演示：
# $ wx_start_free_chat()
# call screen wx_phone
screen wx_phone(standalone=False):
    tag wx_phone
    modal wx_phone_standalone_modal
    default sticker_open = False

    # 如果剧情没有提前初始化聊天，这里会自动加载默认聊天，避免空白。
    on "show" action Function(wx_ensure_default_state)
    on "hide" action [SetVariable("wx_phone_standalone_modal", False), Function(wx_standalone_restore_window)]

    if standalone:
        key "game_menu" action [SetVariable("wx_phone_standalone_modal", False), Hide("wx_phone")]
        key "dismiss" action NullAction()
        key "rollforward" action NullAction()

    # 外侧黑色背景，对应截图中手机/窗口两边的黑边。
    add Solid("#000000")

    $ wx_show_bottom_bar = wx_current_view == "chat" and wx_active_chat_mode in ("free", "scripted")
    $ wx_bottom_height = 112 if wx_active_chat_mode == "scripted" else 150
    $ wx_chat_height = 668 if wx_active_chat_mode == "scripted" else 886
    $ wx_main_height = wx_chat_height if wx_show_bottom_bar else wx_chat_height + wx_bottom_height

    # 中间微信主体：左侧栏 110px + 内容区 1160px。
    vbox:
        xalign 0.5
        ypos 0
        yanchor 0.0
        xsize 1270
        spacing 0

        hbox:
            xsize 1270
            ysize wx_main_height

            use wx_sidebar()

            # 内容区。wx_current_view 决定显示聊天还是朋友圈。
            frame:
                xsize 1160
                ysize wx_main_height
                padding (25, 20)
                background Solid("#f4f4f4")

                if wx_current_view == "moments":
                    use wx_moments_page()
                else:
                    use wx_chat_page()

        # 微信底部栏。剧本聊天只提供操作入口，台词仍走 Ren'Py 默认文本框。
        if wx_show_bottom_bar:
            if wx_active_chat_mode == "free":
                key "K_RETURN" action Function(wx_send_free_chat)

            fixed:
                xsize 1270
                ysize wx_bottom_height

                if sticker_open:
                    use wx_sticker_popconfirm()

                hbox:
                    xsize 1270
                    ysize wx_bottom_height

                    frame:
                        xsize 110
                        yfill True
                        padding (0, 0)
                        background Solid("#3d3d43")

                    frame:
                        xsize 1160
                        yfill True
                        padding (0, 0)
                        background Solid("#272a28")

                        vbox:
                            xfill True
                            yfill True

                            # 顶部分割线
                            frame:
                                xfill True
                                ysize 1
                                padding (0, 0)
                                background Solid("#d9d9d9")

                            frame:
                                xfill True
                                yfill True
                                padding (0, 0)
                                background None

                                fixed:
                                    xfill True
                                    yfill True

                                    button:
                                        xpos 40
                                        yalign 0.4
                                        xysize (76, 76)
                                        background None
                                        hover_background None
                                        action NullAction()

                                        add "images/wechat/bottom_voice.png":
                                            xysize (76, 76)

                                    hbox:
                                        xalign 0.5
                                        yalign 0.5

                                        if wx_active_chat_mode == "free":
                                            use wx_free_chat_input_box()
                                        else:
                                            use wx_scripted_chat_input_box()

                                    button:
                                        xpos 955
                                        yalign 0.4
                                        xysize (76, 76)
                                        background None
                                        hover_background None
                                        action SetScreenVariable("sticker_open", not sticker_open)

                                        add "images/wechat/bottom_emoji.png":
                                            xysize (76, 76)

                                    button:
                                        xpos 1040
                                        yalign 0.4
                                        xysize (76, 76)
                                        background None
                                        hover_background None
                                        action NullAction()

                                        add "images/wechat/bottom_more.png":
                                            xysize (76, 76)


# 左侧导航栏。
# 图标文件在 game/images/wechat/；以后换图标只替换图片或改 add 路径。
screen wx_sidebar():
    frame:
        xsize 110
        yfill True
        padding (0, 0)
        background Solid("#3d3d43")

        vbox:
            xfill True
            spacing 0

            # 聊天按钮：点击后只切换 wx_current_view，不会重置聊天记录。
            button:
                xsize 110
                ysize 145
                background (Solid("#4b4b55") if wx_current_view == "chat" else Solid("#3d3d43"))
                hover_background Solid("#484850")
                action Function(wx_set_view, "chat")

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 6

                    if wx_image_loadable("images/wechat/wechat_icon.png"):
                        add "images/wechat/wechat_icon.png":
                            xalign 0.5
                            xysize (58, 58)
                    else:
                        text "●":
                            xalign 0.5
                            size 42
                            color "#18b02d"

                    text "WeChat":
                        xalign 0.5
                        size 23
                        color ("#18b02d" if wx_current_view == "chat" else "#989ba2")

            # 朋友圈按钮：只切换视图，不影响好感度和剧情进度。
            button:
                xsize 110
                ysize 145
                background (Solid("#4b4b55") if wx_current_view == "moments" else Solid("#3d3d43"))
                hover_background Solid("#484850")
                action Function(wx_set_view, "moments")

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 6

                    if wx_image_loadable("images/wechat/moments_icon.png"):
                        add "images/wechat/moments_icon.png":
                            xalign 0.5
                            xysize (58, 58)
                    else:
                        text "◉":
                            xalign 0.5
                            size 42
                            color "#4285f4"

                    text "朋友圈":
                        xalign 0.5
                        size 23
                        color ("#18b02d" if wx_current_view == "moments" else "#989ba2")


# 聊天记录区域。
# viewport 支持鼠标滚轮和拖动；新消息出现后会自动下滑到底部。
screen wx_chat_page():
    viewport id "wx_chat_viewport":
        xfill True
        yfill True
        mousewheel True
        yinitial 1.0

        vbox:
            xfill True
            spacing 28
            # xoffset/yoffset 是聊天内容内边距。不要在 vbox 上写 padding，Ren'Py 不支持。
            xoffset 120
            yoffset 120
            xmaximum 1110

            for message in wx_chat_messages:
                use wx_chat_message(message)

    if wx_pending_messages and wx_active_chat_mode == "free":
        timer WX_HEROINE_MESSAGE_DELAY action Function(wx_reveal_next_pending_message) repeat True

    if wx_chat_needs_scroll():
        timer 0.01 action [Scroll("wx_chat_viewport", "vertical increase", amount=1000000, delay=0.12), Function(wx_mark_chat_scrolled)]

    if wx_heroine_exit:
        timer 0.15 action [Notify("对方感觉你不礼貌，表示不想和你聊天"), SetVariable("wx_heroine_exit", False)]
        timer 0.5 action Hide("wx_phone")


# 单条聊天气泡。
# side 来自 wx_contacts[contact_id]["side"]：
# right 表示头像和气泡靠右；left 表示靠左。
# 当前我 player 是主视角，在右侧；女主 heroine 在左侧。
screen wx_chat_message(message):
    $ speaker = message.get("speaker", WX_DEFAULT_CONTACT_ID)
    $ side = wx_message_side(message)
    $ message_text = message.get("text", "")
    $ message_image = message.get("image", "")
    $ time_text = message.get("time_text", "")

    vbox:
        xfill True
        spacing 16

        if time_text:
            text time_text:
                xalign 0.5
                size 24
                color "#8b8b8f"
                text_align 0.5

        if not message_text and not message_image:
            pass
        elif side == "right":
            # 右侧气泡：主视角我。文本左对齐，绿色气泡。
            hbox at wx_message_dissolve:
                xalign 1.0
                spacing 16

                null:
                    xfill True

                if message_image:
                    add wx_clean_image_path(message_image):
                        xysize (150, 220)
                else:
                    frame:
                        xmaximum 610
                        padding (28, 18)
                        background Solid("#b9e99d")

                        text message_text:
                            size 31
                            color "#2d3338"
                            xmaximum 550
                            text_align 0.0
                            xalign 0.0

                use wx_avatar(speaker)
        else:
            # 左侧气泡：女主。文本左对齐，白色气泡。
            hbox at wx_message_dissolve:
                spacing 16

                use wx_avatar(speaker)

                if message_image:
                    add wx_clean_image_path(message_image):
                        xysize (150, 220)
                else:
                    frame:
                        xmaximum 720
                        padding (28, 18)
                        background Solid("#ffffff")

                        text message_text:
                            size 31
                            color "#2d3338"
                            xmaximum 660
                            text_align 0.0
                            xalign 0.0

                null:
                    xfill True


# 头像组件。
# 优先加载联系人 avatar 图片；缺图时显示 fallback_color 色块和名字首字。
screen wx_avatar(contact_id):
    $ avatar_path = wx_contact_avatar(contact_id)

    if wx_image_loadable(avatar_path):
        add wx_clean_image_path(avatar_path):
            xysize (78, 78)
    else:
        frame:
            xysize (78, 78)
            padding (0, 0)
            background Solid(wx_contact_color(contact_id))

            text wx_avatar_initial(contact_id):
                xalign 0.5
                yalign 0.5
                size 33
                color "#ffffff"



# AI 自由聊天的真实输入框。回车发送，右侧按钮只保留视觉摆设。
screen wx_free_chat_input_box():
    frame:
        xsize 610
        ysize 64
        padding (22, 0)
        background Solid("#ffffff")

        fixed:
            xfill True
            yfill True

            if wx_ai_waiting:
                text "等待回复...":
                    xpos 0
                    ypos 16
                    size 28
                    color "#9a9a9a"
            elif not wx_free_input_text:
                text "发送消息...":
                    xpos 0
                    ypos 16
                    size 28
                    color "#9a9a9a"

            input:
                value VariableInputValue("wx_free_input_text")
                # 单次输入最大长度。以后觉得玩家回复太短/太长，就改 length。
                length 80
                xpos 0
                ypos 15
                xfill True
                size 28
                color "#2d3338"


screen wx_scripted_chat_input_box():
    frame:
        xsize 610
        ysize 64
        padding (22, 0)
        background Solid("#ffffff")


# 表情包按钮的 Popconfirm 弹窗。
screen wx_sticker_popconfirm():
    frame:
        xpos 1103
        xanchor 0.5
        ypos -225
        xysize (245, 245)
        padding (0, 0)
        background Solid("#ffffff")

        button:
            xfill True
            yfill True
            background None
            hover_background Solid("#f4f4f4")
            action [Function(wx_send_milk_tea_sticker), SetScreenVariable("sticker_open", False)]

            add "images/wechat/milk_tea_sticker.png":
                xalign 0.5
                yalign 0.5
                xysize (150, 220)

    text "▼":
        xpos 1103
        xanchor 0.5
        ypos 8
        size 34
        color "#ffffff"


# 朋友圈页面。
# 数据来自 wx_moment_posts；滚动区域只显示内容，不会影响好感度。
screen wx_moments_page():
    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True

        vbox:
            xfill True
            spacing 0
            # 朋友圈内容内边距。不要改成 padding，vbox 不支持。
            xoffset 38
            yoffset 18
            xmaximum 1094

            for post in wx_moment_posts:
                if wx_should_show_moment_post(post):
                    use wx_moment_post(post)


# 单条朋友圈。
# post 字段来自 data/wechat_data.rpy：post_id/author/time/text/images/comment_text。
screen wx_moment_post(post):
    $ author_id = post.get("author", WX_DEFAULT_CONTACT_ID)
    $ post_id = post.get("post_id", "")
    $ images = list(post.get("images", ()))
    $ comment_text = post.get("comment_text", "")
    $ player_comment = wx_moment_comment(post_id)
    $ heart_image = "images/wechat/heart_full.png" if wx_is_moment_liked(post_id) else "images/wechat/heart_empty.png"

    frame:
        xfill True
        padding (0, 26, 0, 26)
        background Solid("#f4f4f4")

        hbox:
            xfill True
            spacing 24

            use wx_avatar(author_id)

            vbox:
                xfill True
                spacing 14

                text wx_contact_name(author_id):
                    size 31
                    color "#6c789b"
                    bold True

                text post.get("text", ""):
                    size 31
                    color "#333333"
                    xmaximum 850

                # images 为空时不调用 wx_moment_images()，所以无图片朋友圈不会出现占位图。
                if images:
                    use wx_moment_images(images)

                fixed:
                    xfill True
                    ysize 58

                    text post.get("time", ""):
                        xpos 0
                        ypos 9
                        size 25
                        color "#9a9a9a"

                    hbox:
                        xalign 1.0
                        yalign 0.5
                        spacing 18

                        # 评论按钮：只写入 data/wechat_data.rpy 里配置好的预设评论。
                        textbutton "评论":
                            xsize 86
                            ysize 42
                            background None
                            hover_background Solid("#e6e6e6")
                            action Function(wx_add_moment_comment, post_id, comment_text)
                            text_size 25
                            text_color "#666666"
                            text_hover_color "#333333"
                            text_xalign 0.5
                            text_yalign 0.5

                        # 点赞按钮：空心/实心爱心图片只看 wx_moment_likes，不调用好感度接口。
                        imagebutton:
                            xysize (46, 46)
                            idle Transform(heart_image, xysize=(46, 46))
                            hover Transform(heart_image, xysize=(46, 46))
                            action Function(wx_toggle_moment_like, post_id)

                if player_comment:
                    frame:
                        xfill True
                        padding (14, 10)
                        background Solid("#e8e8e8")

                        text wx_contact_name(WX_PLAYER_CONTACT_ID) + "：" + player_comment:
                            size 25
                            color "#4f4f4f"
                            xmaximum 820

                frame:
                    xfill True
                    ysize 1
                    padding (0, 0)
                    background Solid("#dedede")


# 朋友圈图片排布。
# 1 张：大图；2 张：并排；3 张以上：每行 3 张网格。
# 以后想改图片尺寸，改 wx_moment_image() 调用里的宽高。
screen wx_moment_images(images):
    if len(images) == 1:
        use wx_moment_image(images[0], 560, 315)
    elif len(images) == 2:
        hbox:
            spacing 22

            for image_path in images:
                use wx_moment_image(image_path, 390, 220)
    else:
        vbox:
            spacing 14

            for image_row in wx_chunks(images, 3):
                hbox:
                    spacing 14

                    for image_path in image_row:
                        use wx_moment_image(image_path, 190, 190)


# 单张朋友圈图片。
# 图片存在就显示真实图片；图片路径写了但文件未放入时，显示“图片未放入”提示。
# 注意：无图片朋友圈不会走到这里，所以不会凭空出现占位图。
screen wx_moment_image(image_path, image_width, image_height):
    if wx_image_loadable(image_path):
        add wx_clean_image_path(image_path):
            xysize (image_width, image_height)
    else:
        frame:
            xysize (image_width, image_height)
            padding (0, 0)
            background Solid("#c8d1dc")

            text "图片未放入":
                xalign 0.5
                yalign 0.5
                size 24
                color "#ffffff"
