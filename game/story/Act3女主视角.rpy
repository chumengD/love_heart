# image chapter3_heroine_view:
#     contains:
#         Solid("#FFFFFF")

#     contains:
#         Text(
#             "Act 3.5",
#             color="#000000",
#             size=100,
#             font="fonts/aa幸运星.ttf"
#         )
#         xalign 0.5
#         yalign 0.41

#     contains:
#         Text(
#             "女主视角・心动回响",
#             color="#000000",
#             size=120,
#             font="fonts/aa幸运星.ttf"
#         )
#         xalign 0.5
#         yalign 0.52

#     contains:
#         Text(
#             "・",
#             color="#000000",
#             size=80
#         )
#         xalign 0.382
#         yalign 0.52

image heroine_memory_open = "images/hiroine/memory1.png"
image heroine_memory_run = "images/hiroine/跑步1.png"
image heroine_memory_flower = "images/hiroine/浇花.png"
image heroine_memory_stars = "images/hiroine/仰望星空1.png"
image heroine_memory_expect = "images/hiroine/期待.png"

label Act3_heroine_view:
    scene black
    with dissolve

    scene heroine_memory_open
    with Dissolve(0.8)

    "自那天傍晚的河边散步结束，我回到宿舍，坐在书桌前，脑海里反复回放着并肩而行的每一个瞬间。"
    "我点开和他的聊天框，从婚礼初识的拘谨，到日常分享的自然，再到生病时的牵挂，原来我们已经走近了这么多。"
    g "他到底是怎么想的？"
    g "对我，是朋友间的照顾，还是藏着和我一样的心动？"
    "我翻看着这段时间的相处片段，那些选择、那些回应，一点点拼凑出他在我心里的样子。"

    "微信初识的时候，他对我的态度，从第一句话就藏着分寸。"
    $ act2_first_chat = lc_get_choice_flag("act2_first_chat", "")
    if act2_first_chat == "ask_identity":
        "他一上来就直白问我的名字和学校，话题干巴巴的，没有顾及我的感受。"
        "聊了没几句就草草结束，总觉得有点尴尬，不想多聊。"
    elif act2_first_chat == "apology_care":
        "他先关心我有没有被撞疼，态度温和又有礼貌。"
        "聊天很舒服，我愿意主动接话，慢慢和他多说几句。"
    elif act2_first_chat == "bouquet_fate":
        "他提起婚礼的缘分，语气轻松又浪漫。"
        "我忍不住主动分享自己的事，越聊越放松，对他的好感悄悄多了一点。"
    else:
        "第一次聊天的细节已经有些模糊，只记得那时的我还在小心试探他的距离。"

    if lc_get_choice_flag("act2_sticker", False):
        "还有那个可爱的奶茶表情包，一下子就打破了陌生感。"
        g "原来他也有这么可爱的一面。"

    scene heroine_memory_run
    with Dissolve(0.6)

    "接着，是朋友圈里的细小互动。"
    "我偶尔会发甜品、晚霞、音乐和阅读碎片，其实也在悄悄看他会不会留意。"
    if lc_get_choice_flag("moments_commented", False):
        "他认真评论我的日常，夸我做的甜品、拍的晚霞。"
        "被放在心上的感觉很好，我会忍不住想主动回复他。"
    elif lc_get_choice_flag("moments_liked", False):
        "他给我点了赞，至少是注意到我了，心里轻轻动了一下。"
    else:
        "可是他完全没理会我的动态，就像没看见一样。"
        "那一瞬间，我们好像还是和之前一样陌生。"

    "然后，是那节无聊的水课。"
    "老师只是照着 PPT 念，还不让我们看手机，我烦得忍不住向他吐槽。"
    $ act2_class_reply = lc_get_choice_flag("act2_class_reply", "")
    if act2_class_reply == "simple_comfort":
        "他简单安慰我让我坚持，虽然客气，但总觉得不够贴心。"
    elif act2_class_reply == "empathy_help":
        "他懂我的累，还说愿意帮我。"
        "被人放在心上的感觉很暖，忍不住想依赖他。"
    elif act2_class_reply == "funny_video":
        "他给我发搞笑视频，一下子就把坏心情赶跑了。"
        g "和他聊天，好像真的会变得轻松开心。"
    else:
        "那时我只是想找个人说说话，也想看看他会不会认真接住我的情绪。"

    scene heroine_memory_flower
    with Dissolve(0.6)

    "再后来，就是那天傍晚的校园偶遇。"
    "放学路上突然看见他，我又惊喜又紧张。"
    $ act3_encounter = lc_get_choice_flag("act3_encounter", "")
    if act3_encounter == "natural_route":
        "他说刚好顺路，语气自然不刻意。"
        "我觉得我们真的很有缘分，开心地和他并肩走路聊天。"
    elif act3_encounter == "direct_wait":
        "他直接说特意等我，来得太突然了。"
        "我有点尴尬，也有点不知所措，不知道该怎么接话。"
    elif act3_encounter == "avoid_eye":
        "他低头玩手机不理我，还是我主动打招呼。"
        "气氛怪怪的，简单聊两句就分开了。"
    else:
        "那次相遇像是意外，又像是有人悄悄安排好的巧合。"

    if lc_get_choice_flag("act3_give_candy", False):
        "他看出我很累，还贴心给我软糖补充能量。"
        "细节里全是温柔，心里一下子就被打动了。"

    scene heroine_memory_stars
    with Dissolve(0.6)

    "发烧浑身难受的时候，我最需要的是真心的关心。"
    $ act4_sick_reply = lc_get_choice_flag("act4_sick_reply", "")
    if act4_sick_reply == "hot_water":
        "他只让我多喝热水、好好休息，客套又敷衍。"
        "明明很难受，却感觉不到真正的在意。"
    elif act4_sick_reply == "care_questions":
        "他仔细问我的症状，提醒我吃药、垫高枕头。"
        "句句都很用心，我能真切感受到他的担心，越来越想依赖他。"
    elif act4_sick_reply == "rush_over":
        "他很自责，还想立刻来找我。"
        "心意很足，但有点太冲动了，我怕他麻烦，只能委婉拒绝。"
    else:
        "那天夜里，我隔着屏幕等他的回复，也在等一份真正落到心上的在意。"

    if lc_get_choice_flag("act4_takeaway", False):
        "他没有只说空话，而是默默给我点了药、粥和暖宝宝。"
        "收到外卖的时候特别感动，从来没有人对我这么细心。"

    "最后，是黄昏河边的散步。"
    "河边晚风很舒服，和他一起散步，我期待着更走心的交流。"
    $ act5_walk_reply = lc_get_choice_flag("act5_walk_reply", "")
    if act5_walk_reply == "self_talk":
        "他一直说自己的事，完全不听我说话，气氛也慢慢变得冷淡。"
    elif act5_walk_reply == "listen":
        "他安静听我说话，温柔回应我，还分享自己的经历。"
        "和他相处特别安心，暧昧的感觉越来越浓。"
    elif act5_walk_reply == "overpraise":
        "他不停刻意夸我，话说得很空，一点都不真诚。"
        "我觉得很不自在，心里有点抵触。"
    else:
        "那样的晚风里，每一句话都会被放大，也更容易看清一个人的真心。"

    $ act3_heroine_affection = lc_get_affection()

    if act3_heroine_affection >= 45:
        "这些回忆一点点叠起来，心动的答案已经变得很清楚。"
        "当前好感度：[act3_heroine_affection]。"
        g "原来我早就开始期待下一次见面了。"
        $ lc_grant_achievement("heartbeat_echo")
    elif act3_heroine_affection >= 25:
        "这些回忆一点点叠起来，我还不能完全确定他的心意。"
        "当前好感度：[act3_heroine_affection]。"
        g "可是只要想到他，心里还是会变得柔软。"
    else:
        "这些回忆一点点叠起来，我仍然有些犹豫。"
        "当前好感度：[act3_heroine_affection]。"
        g "如果想靠近我，他还需要更真诚、更细心一点。"

    scene heroine_memory_expect
    with Dissolve(0.6)

    "我关掉手机，趴在桌上。"
    g "下一次见面，会是什么样子呢？"

    scene black
    with dissolve

    return
