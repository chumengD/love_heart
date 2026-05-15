image encounter ="images/Act3/encounter.jpg"
image encounter_bg ="images/Act3/encounter_bg.jpg"
image sayHi ="images/Act3/sayHi.jpg"
image give_candy = "images/Act3/give_candy.png"

label act3_encounter_first_branch:
    hide encounter
    show sayHi
    $ lc_add_affection(6)
    $ lc_set_choice_flag("act3_encounter", "natural_route")
    m "好巧啊，你也走这条路？我刚好顺路"
    g "哇，好巧！你也这边回去吗！"
    m "哈哈哈对呀。今天正好在你学校附近帮领导办事，没想到能遇见你。"
    g "看来我们真的真的很有缘分呢！"
    return

label act3_encounter_walk_together:
    "我们一路并肩走着，晚风轻轻吹过，气氛温柔又轻松。"
    "从校园里的趣事聊到日常的小烦恼，从喜欢的食物说到最近的心情......"
    "每一句对话都像早就约定好一样舒服自在。"
    return

label act3_encounter_give_candy:
    show give_candy
    with dissolve

    "我打开背包，里面是一小袋甜甜的软糖。"
    "我上前一步，轻轻把东西递到她面前。"
    m "看你放学挺累的，补充点能量。"
    g "谢谢你……你也太细心了。"
    m "哈哈哈对呀。你看晚霞，是不是很漂亮呀？"
    $ lc_add_affection(8)
    $ lc_set_choice_flag("act3_give_candy", True)
    $ lc_grant_achievement("warm_encounter")
    hide give_candy
    with dissolve
    return

label act3_encounter_bag_branch:
    $ act3_bag_choice_ready = False
    call act3_encounter_first_branch
    call act3_encounter_give_candy
    call act3_encounter_walk_together
    hide sayHi
    return

label Act3_encounter:
    $ act3_bag_choice_ready = False
    show watch_phone
    with dissolve

    "微信断断续续聊天，我们分享生活、吐槽琐事、偶尔互发表情包。"
    "陌生感慢慢消散，聊天框里的语气也越来越自然。"
    "我总会忍不住点开她的朋友圈，一遍一遍翻看。"
    m "好想见她一面……哪怕只是短短一会儿也好。"
    "我悄悄向表哥打听，记下了她下课回宿舍的必经路线。"
    
    hide watch_phone
    with dissolve
    show encounter_bg
    with dissolve
    "为了制造偶遇，今天傍晚，我刻意提前半小时来到这条街道。"
    "晚风轻轻吹过，落日把地面拉出长长的人影。"
    "我站在路边，假装随意，视线却一直停留在路口。" 
    hide encounter_bg
    show encounter
    "没过多久,那个小小的身影慢慢出现在视线里"
    "她背着双肩包，发丝被风吹起，走路慢悠悠的，神色带着一点上课后的疲惫"
    m "看见了……真人比照片还要好看"
    "心口咚咚作响,心跳开始乱了"
    "要不要上前搭话？"
    "我该怎么开口？"
    $ act3_bag_choice_ready = True
   
    menu:
        "你选择"
       
        "好巧啊，你也走这条路？我刚好顺路":
            $ act3_bag_choice_ready = False
            call act3_encounter_first_branch
            call act3_encounter_walk_together

        "我特意等你的，就是想跟你多见一面":
            $ act3_bag_choice_ready = False
            hide encounter
            show sayHi
            $ lc_add_affection(-5)
            $ lc_set_choice_flag("act3_encounter", "direct_wait")
            "（当前好感度：[4]）"
            m "我特意等你的，就是想跟你多见一面"
            g "啊……这样吗？"
            m "刚下课吗？"
            g "嗯......"
            $ lc_grant_achievement("clumsy_encounter")
            "沉默悄然而至。空气里飘着尴尬的安静。"
            "为什么她不开口了？难道我这句话太冒失了吗？"
            "我偷偷看她，她低着头，手指轻轻绞着书包带，似乎对这次相遇并不比惊喜"
            #change 沉默悄然而至，为什么她不开口了？balabala
        "低头玩手机，假装没看见，等女主主动打招呼":
            $ act3_bag_choice_ready = False
            $ lc_set_choice_flag("act3_encounter", "avoid_eye")
            hide encounter
            show sayHi
            "我紧张到不敢对视"
            "慌忙低下头假装滑动手机，刻意装作没有看见她"
            "好巧，你也在这里？"
            "嗯......是呀。今天正好在你学校附近帮领导办事，没想到能遇见你。"
            "哈哈哈真巧呀！那你先去忙吧，我先走了哦，拜拜！"
            "望着她渐行渐远的背影，我恨不得甩自己一巴掌。"
            "刚才那几分钟，我到底在干什么？"
            "明明来之前在心里演练了一百遍开场白，结果真的见到她，却连一句打招呼的话都说不出口。"
            "她的背影越走越远，我站在原地，只剩下满心的懊恼和后悔。"
            #change 望着她渐行渐远的背影，我恨不得甩自己一巴掌

    $ act3_bag_choice_ready = False
    hide sayHi
