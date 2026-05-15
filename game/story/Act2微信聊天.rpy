default act2_flag = 0
default act2_sticker_break = False
default act2_moments_unlocked = False
define pause_time =1
define config.return_not_found_label = "act2_missing_return_recovery"

image watch_phone = "images/Act2/watch_phone.png"
image office1 = "images/Act2/office.png"
image office2 = "images/Act2/office_phone_message.png"


label Act2_wx:
    $ act1_wechat_unlocked = True
    $ renpy.music.play(bg_music3, channel="music", fadeout=2.0, relative_volume=0.3, loop=True)
    scene black
    show watch_phone
    "婚礼结束回到家，窗外天色慢慢暗了下来。"
    "我躺在床上，反复点开微信界面。"
    "聊天框顶端，静静躺着她的头像，还没有备注。"
    "xx，真是个好听的名字。"
    "加完好友之后，我们一直没有说话。"
    "聊天框上干干净净，只有系统提示：你们已成为好友，可以开始聊天。"
    # show m normal at left
    m "怎么办……要不要先发消息？"
    m "第一次主动加女生微信，完全不知道该说什么啊......"
    "我在输入框里打下“你好”，又觉得太生硬，慢慢删掉。"
    "换成“在吗”，看起来又像有急事，只好再次清空。"
    "指尖悬停在屏幕上方，迟迟不敢按下发送。"
    "脑海里又想起白天相撞的那一瞬间。"

    # hide m normal
    hide watch_phone
    with dissolve
    show get_flower2
    with pixellate

    "她泛红的脸颊、软软的声音，还有那束躺在她怀里的捧花。"
    "一切都是那么美好，那么浪漫，那么甜蜜。"
    "心跳又开始不受控制地加快。"
    hide get_flower2
    with pixellate
    $ wx_start_scripted_chat()
    show screen wx_phone
    pause pause_time


    "算了，不可能一直等她先开口。"
    menu chat1:
        "要发什么……？"
        "你叫什么名字？也是大学生吗？":
            $ lc_add_affection(-3)
            $ lc_set_choice_flag("act2_first_chat", "ask_identity")
            $ act2_flag = 1
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "你叫什么名字？也是大学生吗？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嗯，我叫xx，在中国计量大学。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "你在哪个专业？平时喜欢做啥？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "啊，我在计算机专业。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "平时...看看小说听听音乐什么的吧。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "你平时看些什么小说？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嗯......很多种类。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "今天不早了，先不聊了哦。")
            call wx_click_reveal_pending_message
            "对话很快停在了礼貌又尴尬的位置。"
            "她的回复不算冷淡，却也没有继续展开的意思。"
            $ lc_grant_achievement("awkward_break_ice")

        "白天撞疼你了吧？实在不好意思，婚礼人多太乱了":
            $ lc_add_affection(4)
            $ lc_set_choice_flag("act2_first_chat", "apology_care")
            $ act2_flag = 2
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "白天撞疼你了吧？实在不好意思，婚礼人太乱了。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "没事啦，我本来也往前挤嘛。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "对啦，你是新娘新郎的朋友吗？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "嗯嗯，新郎是我表哥呢。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "这样呀，我是新娘的好闺蜜！")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "哈哈哈，当初和她还比赛谁先能找到对象呢。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "结果她都结婚了我还是母胎solo。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "其实我今天本来是来凑凑热闹的哈哈。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "那我跟你不一样呢！")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "我闺蜜一开始非要我做伴娘。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "但是我这几天实在是太忙了，没时间准备什么，只能作为婚礼宾客送祝福啦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "你最近在忙些什么呀？你是大学生吗？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "我是杭州电子科技大学的大四学生，最近已经在实习了......")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "对呀，我是中国计量大学计算机专业大三的学生。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "毕竟大三了嘛，在很紧张地写论文呢。")
            call wx_click_reveal_pending_message
            "简单几句来回，气氛缓和温柔。"
            "她主动接话，没有刻意结束聊天。"

        "今天婚礼的捧花寓意超好，没想到我们这么有缘分":
            $ lc_add_affection(6)
            $ lc_set_choice_flag("act2_first_chat", "bouquet_fate")
            $ act2_flag = 3
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "今天婚礼的捧花寓意超好，没想到我们这么有缘分。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "我也觉得！第一次抢捧花还能撞到人，缘分拉满了哈哈。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "对啦，你是新娘新郎的朋友吗？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "嗯嗯，新郎是我表哥呢。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "这样呀，我是新娘的好闺蜜！")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "哈哈哈，当初和她还比赛谁先能找到对象呢。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "结果她都结婚了我还是母胎solo。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "其实我今天本来是来凑凑热闹的哈哈。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "那我跟你不一样呢！")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "我闺蜜一开始非要我做伴娘。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "但是我这几天实在是太忙了，没时间准备什么，只能作为婚礼宾客送祝福啦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "你最近在忙些什么呀？你是大学生吗？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "我是杭州电子科技大学的大四学生，最近已经在实习了......")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "这样呀，我是中国计量大学计算机专业大三的学生。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "毕竟大三了嘛，在很紧张地写论文呢。")

            call wx_click_reveal_pending_message
            "她主动分享自己参加婚礼的感受和生活经历。"
            "聊天氛围比想象中更快升温。"

label act2_after_chat1:
    $ wx_sticker_allowed = True
    pause
    if act2_sticker_break:
        $ lc_grant_achievement("sticker_break_ice")
    else:
        "我忍住继续发消息的冲动，把手机放到枕边。"

    hide screen wx_phone
    show office1
    with dissolve
    "微信那头的对话框，终于不再是冷冰冰的系统提示。"
    "日子一天天过去，我们的聊天渐渐从 “礼貌问候” 变成了 “日常习惯”。"
    "从偶尔聊几句，到每天都会说上几句话；从简单问答，到愿意把小事都讲给对方听。"

    "办公室里安安静静，只有键盘敲击的轻响。"
    "我埋首在工作里，手指在键盘上不停敲打着。"
    "手边的咖啡凉了又热，目光却总会不自觉地，飘向桌角亮着屏保的手机。"
    hide office1
    show office2
    with dissolve
    "就在我重新低头专注工作时，桌角的手机忽然轻轻一震，屏幕骤然亮起。"
    "我猛地停下手里的动作，微微前倾身子，看向那行弹出的新消息，心跳在这一刻，悄悄乱了节拍。"
    hide office2
    
    show screen wx_phone
    pause pause_time

    $ wx_queue_text_message("heroine", "这个水课老师好烦呐，只是念ppt，还不让我们看手机。", time_text="10:07")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("player", "哈哈哈，老师也很想水掉这个课啊。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("player", "不过不让看手机确实很死板。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "诶，想到我下课之后还有专业课作业，还要改论文。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "好多事情呀，我都忙晕了。")
    call wx_click_reveal_pending_message

    menu:
        "她被课程和作业压得有点烦，我该怎么回？"
        "加油，坚持一下就下课啦":
            $ lc_add_affection(3)
            $ lc_set_choice_flag("act2_class_reply", "simple_comfort")
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "加油，坚持一下就下课啦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嗯嗯，好哦。")
            call wx_click_reveal_pending_message
        "专业课确实很累，有需要我帮忙的就跟我说哦":
            $ lc_add_affection(5)
            $ lc_set_choice_flag("act2_class_reply", "empathy_help")
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "专业课确实很累，慢慢写，不用着急，有需要我帮忙的就跟我说哦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嘿嘿，好呀，谢谢你。")
            call wx_click_reveal_pending_message
        "别烦啦，给你分享一个搞笑短视频":
            $ lc_add_affection(4)
            $ lc_set_choice_flag("act2_class_reply", "funny_video")
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "别烦啦，给你分享一个搞笑短视频。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "【搞笑短视频】")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "哈哈哈哈哈哈哈哈！Xswl！")
            call wx_click_reveal_pending_message

    "聊天框里的陌生感一点点消散。"
    "我开始期待每一次手机震动。"
    $ act2_moments_unlocked = True
    hide screen wx_phone
    return

label act2_chat1_bouquet_branch:
    $ lc_add_affection(6)
    $ lc_set_choice_flag("act2_first_chat", "bouquet_fate")
    $ act2_flag = 3
    $ wx_sticker_allowed = False
    if act2_sticker_break:
        $ wx_queue_text_message("heroine", "噗")
        call wx_click_reveal_pending_message
        $ wx_queue_text_message("heroine", "你还蛮可爱的嘛")
        call wx_click_reveal_pending_message
        "简单一句话，让我忍不住傻笑了出来。"
    $ wx_queue_text_message("player", "今天婚礼的捧花寓意超好，没想到我们这么有缘分。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "我也觉得！第一次抢捧花还能撞到人，缘分拉满了哈哈。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "对啦，你是新娘新郎的朋友吗？")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("player", "嗯嗯，新郎是我表哥呢。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "这样呀，我是新娘的好闺蜜！")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "哈哈哈，当初和她还比赛谁先能找到对象呢。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "结果她都结婚了我还是母胎solo。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("player", "其实我今天本来是来凑凑热闹的哈哈。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "那我跟你不一样呢！")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "我闺蜜一开始非要我做伴娘。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "但是我这几天实在是太忙了，没时间准备什么，只能作为婚礼宾客送祝福啦。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "你最近在忙些什么呀？你是大学生吗？")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("player", "我是杭州电子科技大学的大四学生，最近已经在实习了......")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "这样呀，我是中国计量大学计算机专业大三的学生。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "大三了嘛，我在很紧张地写论文呢。你呢？")
    call wx_click_reveal_pending_message
    "她主动分享自己参加婚礼的感受和生活经历。"
    "聊天氛围比想象中更快升温。"
    jump act2_after_chat1

label act2_missing_return_recovery:
    if act1_wechat_unlocked and not act2_moments_unlocked:
        jump act2_after_chat1
    return

init 10 python:
    _act2_base_send_milk_tea_sticker = wx_send_milk_tea_sticker

    def wx_send_milk_tea_sticker():
        global act2_sticker_break, wx_sticker_allowed

        filename, _line = renpy.get_filename_line()
        in_act2_script = filename.replace("\\", "/").endswith("game/story/Act2微信聊天.rpy")

        if in_act2_script and act2_flag == 0:
            if act2_sticker_break:
                return

            if not wx_sticker_allowed:
                renpy.notify("看起来现在不是发送表情包的好时机，你错过了哦")
                return

            wx_sticker_allowed = False
            act2_sticker_break = True
            lc_set_choice_flag("act2_sticker", True)
            wx_append_sticker(WX_PLAYER_CONTACT_ID, "images/wechat/milk_tea_sticker.png")
            lc_add_affection(8, source="wechat:sticker:milk_tea")
            renpy.jump("act2_chat1_bouquet_branch")

        renpy.notify("看起来现在不是发送表情包的好时机，你错过了哦")
