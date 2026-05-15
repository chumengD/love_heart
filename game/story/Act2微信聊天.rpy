default act2_flag = 0
default act2_sticker_break = False
default act2_sticker_redirect_target = None
default act2_moments_unlocked = False
define pause_time =1

image watch_phone = "images/Act2/watch_phone.png"
image office = "images/Act2/office.png"

init 10 python:
    _act2_base_send_milk_tea_sticker = wx_send_milk_tea_sticker

    def wx_send_milk_tea_sticker():
        global act2_sticker_break, act2_sticker_redirect_target, wx_sticker_allowed

        if act2_sticker_redirect_target:
            if act2_sticker_break:
                return

            if not wx_sticker_allowed:
                renpy.notify("看起来现在不是发送表情包的好时机，你错过了哦")
                return

            target = act2_sticker_redirect_target
            act2_sticker_redirect_target = None
            wx_sticker_allowed = False
            act2_sticker_break = True
            wx_append_sticker(WX_PLAYER_CONTACT_ID, "images/wechat/milk_tea_sticker.png")
            lc_add_affection(8, source="wechat:sticker:milk_tea")
            renpy.jump(target)

        _act2_base_send_milk_tea_sticker()

label Act2_wx:
    $ act1_wechat_unlocked = True
    $ renpy.music.play(bg_music3, channel="music", fadeout=1.0, relative_volume=0.4, loop=True)
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
    #change 下定决心要发送
    hide get_flower2
    with pixellate
    $ wx_start_scripted_chat()
    show screen wx_phone
    pause pause_time

    "算了，不可能一直等她先开口。"
    $ act2_sticker_redirect_target = "act2_chat1_bouquet_branch"
    menu chat1:
        "要发什么……？"
        "你叫什么名字？也是大学生吗？":
            $ lc_add_affection(-3)
            $ act2_flag = 1
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "你叫什么名字？也是大学生吗？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嗯，我叫xx，在xx大学。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "你在哪个专业？平时喜欢做啥？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "啊，我在xx专业。")
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
            $ wx_queue_text_message("player", "我是A大学的大四学生，最近已经在实习了......")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "对呀，我是B大学XX专业大三的学生。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "毕竟大三了嘛，在很紧张地写论文呢。")
            call wx_click_reveal_pending_message
            "简单几句来回，气氛缓和温柔。"
            "她主动接话，没有刻意结束聊天。"

        "今天婚礼的捧花寓意超好，没想到我们这么有缘分":
            jump act2_chat1_bouquet_branch

label act2_after_chat1:
    $ act2_sticker_redirect_target = None
    $ wx_sticker_allowed = True
    pause
    if act2_sticker_break:
        #todo 表情包
        "简单一句话，让我盯着屏幕傻笑了好久。"
        $ lc_grant_achievement("sticker_break_ice")
    else:
        "我忍住继续发消息的冲动，把手机放到枕边。"

    #change 要描写一下男主工作，不然立马就切到女主上课的场景会有点突兀
    "微信那头的对话框，终于不再是冷冰冰的系统提示。"
    "日子一天天过去，我们的聊天渐渐从 “礼貌问候” 变成了 “日常习惯”。"
    "从偶尔聊几句，到每天都会说上几句话；从简单问答，到愿意把小事都讲给对方听。"
    show office

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
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "加油，坚持一下就下课啦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嗯嗯，好哦。")
            call wx_click_reveal_pending_message
        "专业课确实很累，有需要我帮忙的就跟我说哦":
            $ lc_add_affection(5)
            $ wx_sticker_allowed = False
            $ wx_queue_text_message("player", "专业课确实很累，慢慢写，不用着急，有需要我帮忙的就跟我说哦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嘿嘿，好呀，谢谢你。")
            call wx_click_reveal_pending_message
        "别烦啦，给你分享一个搞笑短视频":
            $ lc_add_affection(4)
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
    $ act2_sticker_redirect_target = None
    $ lc_add_affection(6)
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
    $ wx_queue_text_message("player", "我是A大学的大四学生，最近已经在实习了......")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "对呀，我是B大学XX专业大三的学生。")
    call wx_click_reveal_pending_message
    $ wx_queue_text_message("heroine", "毕竟大三了嘛，在很紧张地写论文呢。你呢？")
    call wx_click_reveal_pending_message
    "她主动分享自己参加婚礼的感受和生活经历。"
    "聊天氛围比想象中更快升温。"
    jump act2_after_chat1
