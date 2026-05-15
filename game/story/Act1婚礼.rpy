image chapter1:
    contains:
        Solid("#FFFFFF")

    contains:
        Text(
            "Act 1",
            color="#000000",
            size=100,
            font="fonts/aa幸运星.ttf"
        )
        xalign 0.5
        yalign 0.41

    contains:
        Text(
            "初遇・心动伊始",
            color="#000000",
            size=120,
            font="fonts/aa幸运星.ttf"
        )
        xalign 0.5
        yalign 0.52
    
    contains:
        Text(
            "・",
            color="#000000",
            size=80
        )
        xalign 0.435
        yalign 0.52

image bird= "images/Act1/鸽子.png"
image wedding ="images/Act1/婚礼现场1.png"
image flower = "images/Act1/捧花1.png"
image peng = "images/Act1/撞.png"

image sorry1 = "images/Act1/sorry1.png"
image sorry2 = "images/Act1/道歉2.png"

image get_flower1= "images/Act1/接花.png"
image get_flower2= "images/Act1/接花高兴.jpg"

default act1_wechat_unlocked = False

label Act1_wedding:
    #结婚场景
    $ renpy.music.play(audio.wedding_music, channel="music", relative_volume=0.4,fadein=1.0)
    scene black

    show chapter1
    with Dissolve(0.8)
    pause 60.0
    hide chapter1
    with dissolve

    show wedding
    with Dissolve(0.8)

    "洁白的拱门缠绕着香槟色玫瑰，铺着白色蕾丝的长桌摆着精致的花艺"
    "宾客们穿着得体的衣服，三三两两交谈着，脸上都带着笑意"
    "今天是表哥的婚礼"
    "我在一周前就收到了邀请"
    # show m normal at left
    m "啊，又要被迫吃一波狗粮了啊......"
    # hide m normal

    # hide bird
    # with dissolve
    # show wedding

    "舞台上，表哥牵着新娘的手，正温柔地说着誓词"
    "阳光透过宴会厅的落地窗，洒在两人身上，连空气里都飘着甜腻的浪漫气息。"
    "看着两位新人眼里的笑意，我突然有点羡慕。"
    "我的那个“她”什么时候会出现呢？"
    
    hide wedding
    with dissolve
    show flower
    with dissolve

    #PS：这里是抛捧花环节，需要两张图(美工愿意的话可以画3张)，第一张是抛花的场景描写
    #可以不画新娘，注重的是氛围，第二张是男女主相撞，偷懒的话可以不画出角色，甚至不画
    #第三张是两人初次见面了
    
    "新娘誓词结束，主持人笑着宣布激动人心的抛捧花环节。"
    "宴会厅里的女生们纷纷起身，笑着涌向舞台下方"
    "有的整理着裙摆，有的互相推搡着，眼里满是期待。"

    # show m normal at left
    "怎么大家都这么积极?"
    "我本就是来凑热闹的......"
    "要不我也去试试看，要是能抢到捧花，说不定还能跟表哥讨个好彩头。"
    "我跟着人群往前凑"
    "眼里只有在空中的捧花，完全没有注意到周围的情况。"
    "我踮起脚往前一探"
    "就在这时，手腕突然被旁边的人撞了一下"
    "在撞击的影响下，我下意识转身"
    "结果————"
    
    hide m 
    hide flower
    show peng
    with vpunch 
    "咚！"
    m "啊！"
    g "呀！"
    "两声惊呼同时响起"
    "我踉跄着往后退了半步，手还下意识扶住了对方的胳膊"
    hide peng
    with dissolve
    show sorry1

    # show m normal at left
    # show g normal at right
    "就在我缓过神来，抬头的瞬间"
    "刚好对上对方的眼睛"
    m "啊......"
    "我惊讶于面前人的美丽，不由得忘记了如何说话"
    "长长的睫毛,细腻白嫩的脸蛋"
    "眸子澄澈如一剪秋水，不染俗气，又不失灵动"
    "更令人惊叹的是，秋水里微波粼粼，如枫叶飘落其中"
    "她的脸颊也微微泛红，像熟透的桃子。"
    "......表哥......我好像恋爱了......"
    "她先反应过来，轻轻松开扶着我肩膀的手"
    "往后退了半步，脸上带着歉意的笑容，声音软软的说道"
    
    g "对不起对不起！"
    g "我刚才太急着往前凑了，没看到你转身，没撞疼你吧？"


    "我这才回过神来，为我的失态不堪，脸颊瞬间涨红"
    "急急忙忙松开扶着对方的手，连忙道歉"
    m "没、没撞疼我,应该是我说对不起才对，我转身太急了，没注意到你。"
    "我弯腰捡起地上的捧花"
    hide sorry1
    show get_flower1
    "递到她面前，指尖都有些微微发抖"
    m "这个，你的捧花，掉了。"

    hide get_flower1
    show get_flower2
    "她脸更红了，小声说"
    g "谢谢......"
    "她低头看着手里的捧花，嘴角忍不住微微上扬"

    "我看着她的笑容，心里的勇气突然多了几分。"
    m "那个...... 其实，我觉得我们还挺有缘分的，刚才撞在一起，又一起捡到了捧花。"
    m "能不能… 加个微信？以后说不定还有机会再见面呢。"

    "她抬起头，眼里闪过一丝笑意"
    "又轻轻点了点头，拿出手机，解锁屏幕"
    g "好呀，确实挺有缘分的。"
    g "你来扫我吧"
    hide g
    hide m
    hide bird 
    with dissolve
    stop music fadeout 1.0
    #我觉得这里不用再描写动作，
    $ lc_set_affection(25)
    $ act1_wechat_unlocked = True
    $ lc_grant_achievement("first_encounter")
    return 
