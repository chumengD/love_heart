# WeChat module screens.

screen wx_phone():
    tag wx_phone
    modal True

    on "show" action Function(wx_ensure_default_state)

    add Solid("#000000")

    hbox:
        xalign 0.5
        yalign 0.0
        xsize 1280
        ysize 820

        use wx_sidebar()

        frame:
            xsize 1170
            ysize 820
            padding (0, 0)
            background Solid("#f4f4f4")

            if wx_current_view == "moments":
                use wx_moments_page()
            else:
                use wx_chat_page()

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


screen wx_sidebar():
    frame:
        xsize 110
        yfill True
        padding (0, 0)
        background Solid("#3d3d43")

        vbox:
            xfill True
            spacing 0

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
                        color ("#4285f4" if wx_current_view == "moments" else "#989ba2")


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
            xoffset 30
            yoffset 28
            xmaximum 1110

            for message in wx_chat_messages:
                use wx_chat_message(message)


screen wx_chat_message(message):
    $ speaker = message.get("speaker", WX_DEFAULT_CONTACT_ID)
    $ side = wx_message_side(message)
    $ message_text = message.get("text", "")

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


screen wx_moments_page():
    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True

        vbox:
            xfill True
            spacing 0
            xoffset 38
            yoffset 18
            xmaximum 1094

            for post in wx_moment_posts:
                use wx_moment_post(post)


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

                if images:
                    use wx_moment_images(images)

                hbox:
                    xfill True

                    text post.get("time", ""):
                        size 25
                        color "#9a9a9a"

                    null width 760

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
