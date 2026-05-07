# 微信模块界面。
# 这里只负责“画出来”：左侧栏、聊天记录、底部选项/输入框、朋友圈列表。
# 数据来源在 data/wechat_data.rpy，点击后的行为函数在 systems/wechat_system.rpy。

# 主微信屏幕。
# 剧情里调用：
# $ wx_start_scripted_chat("1", "1")  或  $ wx_start_free_chat("91")
# call screen wx_phone
screen wx_phone():
    tag wx_phone
    modal True

    # 如果剧情没有提前初始化聊天，这里会自动加载默认聊天，避免空白。
    on "show" action Function(wx_ensure_default_state)

    # 外侧黑色背景，对应截图中手机/窗口两边的黑边。
    add Solid("#000000")

    # 中间微信主体：左侧栏 110px + 内容区 1170px。
    # 以后想改变整体宽高，优先改这里的 xsize/ysize，并同步调底部栏宽度。
    hbox:
        xalign 0.5
        yalign 0.0
        xsize 1280
        ysize 820

        use wx_sidebar()

        # 内容区。wx_current_view 决定显示聊天还是朋友圈。
        frame:
            xsize 1170
            ysize 820
            padding (0, 0)
            background Solid("#f4f4f4")

            if wx_current_view == "moments":
                use wx_moments_page()
            else:
                use wx_chat_page()

    # 底部区域。
    # 聊天页显示选项或输入框；朋友圈页不显示底部操作栏内容。
    frame:
        xalign 0.5
        yalign 1.0
        xfill True
        ysize 260
        padding (0, 0)
        background Solid("#7f91a8")

        if wx_current_view == "chat":
            if wx_active_chat_mode == "free":
                use wx_free_chat_bar()
            else:
                use wx_scripted_choice_bar()

    # 右上角齿轮：现在作为“返回当前微信 screen”的出口。
    # call screen wx_phone 后，点击这里会 Return("wechat_settings") 回到剧情流程。
    textbutton "⚙":
        xpos 1675
        ypos 45
        xsize 90
        ysize 90
        background None
        hover_background None
        action Return("wechat_settings")
        text_size 74
        text_color "#5b6875"
        text_hover_color "#7f91a8"
        text_xalign 0.5
        text_yalign 0.5


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

                    # 图片存在时显示真实微信图标；缺图时显示文字兜底，方便开发阶段排查路径。
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

                    # 朋友圈图标路径在这里；以后换图片只改这个 add 路径或替换文件。
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
                        color ("#4285f4" if wx_current_view == "moments" else "#989ba2")


# 聊天记录区域。
# viewport 支持鼠标滚轮和拖动；yinitial 1.0 尽量让新消息后保持底部可见。
screen wx_chat_page():
    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True
        yinitial 1.0

        vbox:
            xfill True
            spacing 28
            # xoffset/yoffset 是聊天内容内边距。不要在 vbox 上写 padding，Ren'Py 不支持。
            xoffset 30
            yoffset 28
            xmaximum 1110

            for message in wx_chat_messages:
                use wx_chat_message(message)


# 单条聊天气泡。
# side 来自 wx_contacts[contact_id]["side"]：
# right 表示头像和气泡靠右；left 表示靠左。
# 以后想改“谁在左谁在右”，不要改这里，改 data/wechat_data.rpy 的 side 字段。
screen wx_chat_message(message):
    $ speaker = message.get("speaker", WX_DEFAULT_CONTACT_ID)
    $ side = wx_message_side(message)
    $ message_text = message.get("text", "")

    # 右侧气泡：当前用于女主。绿色气泡颜色在 background Solid("#b9e99d")。
    if side == "right":
        hbox:
            xfill True
            spacing 16

            null width 250

            frame:
                xmaximum 610
                padding (28, 18)
                background Solid("#b9e99d")
                xalign 1.0

                text message_text:
                    size 31
                    color "#2d3338"
                    xmaximum 550

            use wx_avatar(speaker)
    else:
        # 左侧气泡：当前用于男主。白色气泡颜色在 background Solid("#ffffff")。
        hbox:
            xfill True
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

            null width 200


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
# 按钮来自当前节点 choices；点击后调用 wx_choose_scripted_option(choice_index)。
screen wx_scripted_choice_bar():
    $ choices = wx_current_scripted_choices()

    if choices:
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 80

            for choice_index, choice in enumerate(choices):
                textbutton choice.get("text", ""):
                    xsize 800
                    ysize 92
                    # 选项按钮颜色。以后想贴近截图的描边/背景，优先改这里。
                    background Solid("#ffffff")
                    hover_background Solid("#edf5ff")
                    action Function(wx_choose_scripted_option, choice_index)
                    text_size 30
                    text_color "#111111"
                    text_hover_color "#111111"
                    text_xalign 0.5
                    text_yalign 0.5
    else:
        text "暂无可选回复":
            xalign 0.5
            yalign 0.5
            size 30
            color "#263344"


# 自由输入底栏。
# input 绑定 default wx_free_input_text；发送按钮和回车都会调用 wx_send_free_chat()。
screen wx_free_chat_bar():
    hbox:
        xalign 0.5
        yalign 0.5
        spacing 22

        frame:
            xsize 1320
            ysize 92
            padding (26, 18)
            background Solid("#ffffff")

            input:
                value VariableInputValue("wx_free_input_text")
                # 单次输入最大长度。以后觉得玩家回复太短/太长，就改 length。
                length 80
                size 31
                color "#111111"
                xfill True

        textbutton "发送":
            xsize 170
            ysize 92
            background Solid("#e9f2ff")
            hover_background Solid("#d7e9ff")
            action Function(wx_send_free_chat)
            text_size 31
            text_color "#111111"
            text_xalign 0.5
            text_yalign 0.5

    key "K_RETURN" action Function(wx_send_free_chat)


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

                hbox:
                    xfill True

                    text post.get("time", ""):
                        size 25
                        color "#9a9a9a"

                    null width 760

                    # 点赞按钮：白心/红心只看 wx_moment_likes，不调用好感度接口。
                    textbutton ("♥" if wx_is_moment_liked(post_id) else "♡"):
                        xsize 72
                        ysize 56
                        background None
                        hover_background None
                        action Function(wx_toggle_moment_like, post_id)
                        text_size 42
                        text_color ("#d94b4b" if wx_is_moment_liked(post_id) else "#8f8f8f")
                        text_hover_color "#d94b4b"
                        text_xalign 0.5
                        text_yalign 0.5

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
