# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

image m normal ="images/Characters/_asuka.png1"
image g normal = "images/Characters/_ayalin.png1"

transform left_half:

    zoom 0.6

    xalign 0.0
    yalign 1.0

    xpos -50

define m = Character("男主", image="m")
define g = Character("女主", image="g")

image bird= "images/Act1/鸽子.png"
image wedding ="images/Act1/婚礼现场1.png"
image flower = "images/Act1/捧花1.png"
image peng = "images/Act1/撞.png"
image chapter1:
    contains:
        Solid("#FFFFFF")

    contains:
        Text(
            "chapter 1",
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

image logo ="images/logo.png"
define trans="images/转场.png"



#转场效果SceneTransition("src") src为转场图片链接
init python:

    def SceneTransition(img,
                        fadeout=0.5,
                        hold=0.2,
                        fadein=0.5):

        return MultipleTransition([

            False,
            Dissolve(fadeout),

            img,
            Pause(hold),

            img,
            Dissolve(fadein),

            True
        ])

#开场动画
label splashscreen:
    scene black
    show logo
    with dissolve
    
    pause 1.0

    hide logo
    with dissolve
    return 


# 游戏在此开始。
label start:
    call Act1

    $ wx_start_scripted_chat()

    show screen wx_phone

    call wx_scripted_chat_flow

    hide screen wx_phone

    $ wx_start_free_chat()

    call screen wx_phone

    # 此处为游戏结尾。

    return


label Act1:
    #结婚场景
    scene black

    show chapter1
    with Dissolve(0.8)
    pause 60.0
    hide chapter1
    with dissolve

    show bird
    with Dissolve(0.8)

    "洁白的拱门缠绕着香槟色玫瑰，铺着白色蕾丝的长桌摆着精致的花艺"
    "宾客们穿着得体的衣服，三三两两交谈着，脸上都带着笑意"
    "今天是表哥的婚礼"
    "我在一周前就收到了邀请"
    show m normal at left_half
    m "啊，又要被迫吃一波狗粮了啊......"
    hide m normal

    hide bird
    with dissolve
    show wedding

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

    "怎么大家都这么积极?"
    "我本就是来凑热闹的......"
    "要不我也去试试看，要是能抢到捧花，说不定还能跟表哥讨个好彩头。"
    #这里少了点动作和对人群的描写
    
    with Vpunch(1.0)
    show peng
    "! !"
    "(撞到人了！)"
    #经典的惊呼呢，动作的描写呢？
    hide peng 
    with dissolve
    show bird
    
    "我低头时刚好对上她抬头看过来的，带有一丝慌乱害羞眼睛。"
    "睫毛好长......"
    "她的脸颊也微微泛红，像熟透的桃子。"
    "......表哥......我好像恋爱了......"
    "她先反应过来，轻轻松开扶着我肩膀的手"
    "往后退了半步，脸上带着歉意的笑容，声音软软的说道"
    
    show g normal
    g "对不起对不起！"
    g "我刚才太急着往前凑了，没看到你转身，没撞疼你吧？"
    hide g normal

    "我这才回过神来，脸颊瞬间涨红"
    m "没、没撞疼我,应该是我说对不起才对，我转身太急了，没注意到你。"
    "我弯腰捡起地上的捧花"
    "递到她面前，指尖都有些微微发抖"
    m "这个，你的捧花，掉了。"

    "她脸更红了，小声说"
    g "谢谢......"
    "她低头看着手里的捧花，嘴角忍不住微微上扬"

    "我看着她的笑容，心里的勇气突然多了几分。"
    m "那个...... 其实，我觉得我们还挺有缘分的，刚才撞在一起，又一起捡到了捧花。"
    m "能不能… 加个微信？以后说不定还有机会再见面呢。"

    "她抬起头，眼里闪过一丝笑意"
    "又轻轻点了点头，拿出手机，解锁屏幕"
    "好呀，确实挺有缘分的。"
    g "你来扫我吧"
    hide bird 
    with dissolve

    #我觉得这里不用再描写动作，
    pause 60.0
    return 