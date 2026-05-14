screen lc_achievement_menu_content():

    default unlocked_achievements = lc_unlocked_achievements()
    default achievement_cols = 4
    default achievement_rows = (len(unlocked_achievements) + achievement_cols - 1) // achievement_cols
    default achievement_fillers = (achievement_cols - (len(unlocked_achievements) % achievement_cols)) % achievement_cols

    use game_menu(_("成就系统"), scroll="viewport"):

        vbox:
            spacing 32

            label _("成就系统")

            if unlocked_achievements:
                text _("已解锁 [len(unlocked_achievements)]") style "lc_achievement_summary_text"

                grid achievement_cols achievement_rows:
                    spacing 28

                    for item in unlocked_achievements:
                        use lc_achievement_card(item)

                    for i in range(achievement_fillers):
                        null width 240 height 168

            else:
                text _("还没有解锁成就。") style "lc_achievement_empty_text"


screen lc_achievement_card(item):

    frame:
        style "lc_achievement_card"

        vbox:
            spacing 14
            xalign 0.5
            yalign 0.5

            add Transform(lc_achievement_icon(item), xysize=(100, 100), fit="cover"):
                xalign 0.5

            text item["name"] style "lc_achievement_name_text":
                xalign 0.5


screen lc_achievement_toast(achievement_id):

    zorder 220
    $ item = lc_achievement_by_id(achievement_id)

    if item:
        frame at lc_achievement_toast_appear:
            style "lc_achievement_toast_frame"

            hbox:
                spacing 18
                yalign 0.5

                add Transform(lc_achievement_icon(item), xysize=(100, 100), fit="cover"):
                    yalign 0.5

                vbox:
                    spacing 6
                    yalign 0.5

                    text _("解锁成就：") style "lc_achievement_toast_label_text"
                    text item["name"] style "lc_achievement_toast_name_text"

    timer 3.25 action Hide("lc_achievement_toast")


transform lc_achievement_toast_appear:
    on show:
        alpha 0
        yoffset -24
        linear .25 alpha 1.0 yoffset 0
    on hide:
        linear .45 alpha 0.0 yoffset -24


style lc_achievement_summary_text is gui_text
style lc_achievement_empty_text is gui_text
style lc_achievement_card is empty
style lc_achievement_name_text is gui_text
style lc_achievement_toast_frame is empty
style lc_achievement_toast_label_text is gui_text
style lc_achievement_toast_name_text is gui_text

style lc_achievement_summary_text:
    size 34
    color "#5c4a42"

style lc_achievement_empty_text:
    size 34
    color "#5c4a42"

style lc_achievement_card:
    xsize 240
    ysize 168
    padding (18, 16, 18, 16)
    background Solid("#f8efe9")

style lc_achievement_name_text:
    font gui.interface_text_font
    size 28
    color "#5c4a42"
    textalign 0.5

style lc_achievement_toast_frame:
    xalign 0.5
    ypos gui.notify_ypos
    xsize 520
    ysize 136
    padding (18, 18, 18, 18)
    background Solid("#fff7f0ee")

style lc_achievement_toast_label_text:
    font gui.interface_text_font
    size 24
    color "#8d493e"

style lc_achievement_toast_name_text:
    font gui.interface_text_font
    size 36
    color "#d98770"
