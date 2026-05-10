# 微信模块界面。
# 这里只负责“画出来”：左侧栏、聊天记录、自由输入框、朋友圈列表。
# 数据来源在 data/wechat_data.rpy，点击后的行为函数在 systems/wechat_system.rpy。

# 新微信消息出现时的淡入效果。
# 每条消息对应的 hbox show 时都会从透明过渡到不透明，满足“微信聊天信息 show 时 dissolve”的需求。
transform wx_message_dissolve:
    on show:
        alpha 0.0
        linear 0.25 alpha 1.0

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
    modal standalone

    # 如果剧情没有提前初始化聊天，这里会自动加载默认聊天，避免空白。
    on "show" action Function(wx_ensure_default_state)

    # 外侧黑色背景，对应截图中手机/窗口两边的黑边。
    add Solid("#000000")

    # 中间微信主体：左侧栏 110px + 内容区 1170px。
    hbox:
        xalign 0.5
        ypos 0
        yanchor 0.0
        xsize 1200
        ysize 820

        use wx_sidebar()

        # 内容区。wx_current_view 决定显示聊天还是朋友圈。
        frame:
            xsize 1160
            ysize 820
            padding (25, 20)
            background Solid("#f4f4f4")

            if wx_current_view == "moments":
                use wx_moments_page()
            else:
                use wx_chat_page()

    # AI 自由聊天使用仿微信输入栏；剧本聊天阶段保留 Ren'Py 默认文本框显示旁白/心理。
    if wx_current_view == "chat" and wx_active_chat_mode == "free":
        use wx_free_chat_bar()


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
# viewport 支持鼠标滚轮和拖动；yinitial 1.0 尽量让新消息后保持底部可见。
screen wx_chat_page():
    viewport:
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


# 单条聊天气泡。
# side 来自 wx_contacts[contact_id]["side"]：
# right 表示头像和气泡靠右；left 表示靠左。
# 当前男主 player 是主视角，在右侧；女主 heroine 在左侧。
screen wx_chat_message(message):
    $ speaker = message.get("speaker", WX_DEFAULT_CONTACT_ID)
    $ side = wx_message_side(message)
    $ message_text = message.get("text", "")

    if side == "right":
        # 右侧气泡：主视角男主。文本右对齐，绿色气泡。
        hbox at wx_message_dissolve:
            xalign 1.0
            spacing 16

            null:
                xfill True

            frame:
                xmaximum 610
                padding (28, 18)
                background Solid("#b9e99d")

                text message_text:
                    size 31
                    color "#2d3338"
                    xmaximum 550
                    text_align 1.0
                    xalign 1.0

            use wx_avatar(speaker)
    else:
        # 左侧气泡：女主。文本左对齐，白色气泡。
        hbox at wx_message_dissolve:
            spacing 16

            use wx_avatar(speaker)

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


# 剧本选项底栏。
# 只有当前节点消息全部显示完并且有 choices 时，流程才 call 这个 screen。
screen wx_scripted_choice_bar():
    modal True
    zorder 200
    $ choices = wx_current_scripted_choices()

    use wx_wechat_bottom_bar("scripted", choices)


# 自由输入底栏。
# input 绑定 default wx_free_input_text；发送按钮和回车都会调用 wx_send_free_chat()。
screen wx_free_chat_bar():
    use wx_wechat_bottom_bar("free")

    key "K_RETURN" action Function(wx_send_free_chat)


# 仿微信底部输入栏。
# mode 为 "free" 时显示可输入文本框；mode 为 "scripted" 时把剧本选项放进中间区域。
screen wx_wechat_bottom_bar(mode="free", choices=None):
    default sticker_open = False
    $ choice_items = choices or []

    fixed:
        xalign 0.5
        yalign 1.0
        xsize 1200
        ysize 520

        if sticker_open:
            use wx_sticker_popconfirm()

        hbox:
            xpos 0
            ypos 260
            xsize 1200
            ysize 260

            frame:
                xsize 110
                yfill True
                padding (0, 0)
                background Solid("#3d3d43")

            frame:
                xsize 1090
                yfill True
                padding (0, 0)
                background Solid("#1f2522")

                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 22

                    textbutton ")))":
                        xsize 72
                        ysize 72
                        background None
                        hover_background Solid("#303733")
                        action NullAction()
                        text_size 30
                        text_color "#d8d8d8"
                        text_hover_color "#ffffff"
                        text_xalign 0.5
                        text_yalign 0.5

                    if mode == "free":
                        use wx_free_chat_input_box()
                    else:
                        use wx_scripted_choice_input_box(choice_items)

                    textbutton "☺":
                        xsize 72
                        ysize 72
                        background None
                        hover_background Solid("#303733")
                        action SetScreenVariable("sticker_open", not sticker_open)
                        text_size 52
                        text_color "#d8d8d8"
                        text_hover_color "#ffffff"
                        text_xalign 0.5
                        text_yalign 0.5

                    textbutton "+":
                        xsize 72
                        ysize 72
                        background None
                        hover_background Solid("#303733")
                        action NullAction()
                        text_size 56
                        text_color "#d8d8d8"
                        text_hover_color "#ffffff"
                        text_xalign 0.5
                        text_yalign 0.5


# AI 自由聊天的真实输入框。回车发送，右侧按钮只保留视觉摆设。
screen wx_free_chat_input_box():
    frame:
        xsize 610
        ysize 82
        padding (24, 0)
        background Solid("#ffffff")

        fixed:
            xfill True
            yfill True

            if wx_ai_waiting:
                text "等待回复...":
                    xpos 0
                    ypos 22
                    size 34
                    color "#9a9a9a"
            elif not wx_free_input_text:
                text "发送消息...":
                    xpos 0
                    ypos 22
                    size 34
                    color "#9a9a9a"

            input:
                value VariableInputValue("wx_free_input_text")
                # 单次输入最大长度。以后觉得玩家回复太短/太长，就改 length。
                length 80
                xpos 0
                ypos 20
                xfill True
                size 34
                color "#2d3338"


# 剧本选项显示在微信输入框位置，替代旧的大块蓝色选项底栏。
screen wx_scripted_choice_input_box(choices):
    $ choice_count = len(choices)
    $ choice_width = 610 if choice_count <= 1 else max(180, int((610 - (choice_count - 1) * 10) / choice_count))

    frame:
        xsize 610
        ysize 82
        padding (14, 0)
        background Solid("#ffffff")

        if choice_count:
            hbox:
                xalign 0.5
                yalign 0.5
                spacing 10

                for choice_index, choice in enumerate(choices):
                    textbutton choice.get("text", ""):
                        xsize choice_width
                        ysize 58
                        background Solid("#f4f4f4")
                        hover_background Solid("#e8f1ff")
                        action [ Function(wx_choose_scripted_option, choice_index), Return(choice_index) ]
                        text_size 24
                        text_color "#222222"
                        text_hover_color "#111111"
                        text_xalign 0.5
                        text_yalign 0.5
        else:
            textbutton "继续":
                xalign 0.5
                yalign 0.5
                xsize 220
                ysize 58
                background Solid("#f4f4f4")
                hover_background Solid("#e8f1ff")
                action Return("continue")
                text_size 26
                text_color "#222222"
                text_hover_color "#111111"
                text_xalign 0.5
                text_yalign 0.5


# 表情包按钮的 Popconfirm 弹窗。
screen wx_sticker_popconfirm():
    frame:
        xpos 850
        ypos 35
        xysize (245, 245)
        padding (16, 16)
        background Solid("#ffffff")

        add "images/wechat/milk_tea_sticker.png":
            xalign 0.5
            yalign 0.5
            xysize (150, 220)

    text "▼":
        xpos 956
        ypos 268
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
                use wx_moment_post(post)


# 单条朋友圈。
# post 字段来自 data/wechat_data.rpy：post_id/author/time/text/images。
screen wx_moment_post(post):
    $ author_id = post.get("author", WX_DEFAULT_CONTACT_ID)
    $ post_id = post.get("post_id", "")
    $ images = list(post.get("images", ()))
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

                    # 点赞按钮：空心/实心爱心图片只看 wx_moment_likes，不调用好感度接口。
                    imagebutton:
                        xalign 1.0
                        yalign 0.5
                        xysize (46, 46)
                        idle Transform(heart_image, xysize=(46, 46))
                        hover Transform(heart_image, xysize=(46, 46))
                        action Function(wx_toggle_moment_like, post_id)

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
