# define flag =0
# init python:
#     affection = lc_get_affection()
#     #todo 多高的好感度才算高？
#     if (affection>50):
#         flag =1

image wandering ="images/Act5/wandering.png"
image learn = "images/Act5/学习.png"
image wandering_bg = "images/Act5/wandering_bg.png"

label Act5_wander:
    show learn
    with dissolve
    "几天过后，她的感冒彻底痊愈"
    "身体好转之后，她的语气重新变得轻快活泼"
    "隔着屏幕，我都能感受到她恢复元气的模样"
    hide learn
    with dissolve
    show wandering_bg
    "抓住天气舒适的傍晚，我鼓起勇气发出散步邀约"
    $ act5_affection_before = lc_get_affection()

    if act5_affection_before >= 60:
        "出乎意料，她没有犹豫，爽快答应。"
    else:
        "她犹豫了一下，最终还是答应了我的请求。"
 
    hide wandering_bg
    show wandering
    with dissolve
    
    "夜色慢慢笼罩城市，路边路灯逐一点亮。"
    "我们并肩走在河边步道，晚风轻轻吹动发丝。"
    "没有喧闹人群，没有嘈杂车流"
    "只有安静的晚风、脚下的石板路。"
    "世界好像被隔绝在外，月光幽幽"
    "只余两片沉默的身影与我们相伴"
    "这样的氛围太安静了，反而让我更加在意自己说出口的每一句话。"

    menu:
        "深夜谈心时，我要怎么把控聊天节奏？"
        "聊自己的工作、学习和爱好":
            $ lc_add_affection(-4)
            $ lc_set_choice_flag("act5_walk_reply", "self_talk")
            "紧张之下，我不停寻找话题。"
            "我下意识只顾着讲述自己的学习压力、日常趣事、个人爱好。"
            "我滔滔不绝，没有留意她的状态。"
            "她脚步放缓，眼神飘向河面，频频走神。"
            "偶尔简单附和两声，语气平淡敷衍，找不到融入话题的切入点。"
            "原本温柔的散步氛围，变得单调枯燥。"

        "认真倾听她说话，适时回应":
            $ lc_add_affection(10)
            $ lc_set_choice_flag("act5_walk_reply", "listen")
            "我刻意放慢语速，把说话的主动权交给她。"
            "我安静听她讲述小时候的趣事、喜欢的音乐、对未来的小期待。"
            "在她停顿的时候，我简单附和、温柔回应，偶尔分享相似经历。"
            "一来一回，节奏舒服又自然。"
            "她嘴角一直保持浅浅笑意，说话语气越来越放松。"
            "两个人距离悄悄拉近，暧昧气息包裹在晚风之中。"

        "刻意讨好，夸赞她":
            $ lc_add_affection(-6)
            $ lc_set_choice_flag("act5_walk_reply", "overpraise")
            "害怕气氛冷淡，我刻意寻找夸奖的话术。"
            "我过度夸赞她的长相、性格、穿搭，言语直白又刻意。"
            "空洞又泛滥的赞美，没有一丝真诚。"
            "她轻轻抿嘴，笑意变淡，眼神略带不自然。"
            "刻意的奉承让人产生距离感，心底生出一丝抵触。"

    "晚风从河面吹来，把没有说出口的心事揉进夜色里。"
    "我开始意识到，靠近一个人不只是表达喜欢，也要学会认真听见她。"
    hide wandering
    with dissolve
    return
