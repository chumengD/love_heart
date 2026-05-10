default act2_flag=0

label Act2_wx:
    scene black
    show bird
    "婚礼结束回到家，窗外天色慢慢暗了下来。"
    "我躺在床上，反复点开微信界面。"
    "聊天框顶端，静静躺着她的头像，还没有备注。"
    "xx,真是个好听的名字"
    "加完好友之后，我们一直没有说话。"
    "聊天框上干干净净，只有系统提示：你们已成为好友，可以开始聊天"
    show m normal at left
    m  "怎么办……要不要先发消息？"
    m  "第一次主动加女生微信，我完全不知道该说什么"
    #change 是不是写一下打完字又删的样子？
    "指尖悬停在屏幕上方，迟迟不敢按下发送"
    "脑海里又想起白天相撞的那一瞬间"

    hide m normal
    hide bird
    with dissolve
    show peng
    with pixellate

    "她泛红的脸颊、软软的声音，还有那束躺在她怀里的捧花"
    #change 下定决心要发送
    hide peng
    with pixellate
    show screen wx_phone
    pause 2.0
    

    menu chat1:
        "要发什么……？"
        "你叫什么名字？也是大学生吗？":
            $ lc_add_affection(-3)
            $ act2_flag = 1
        "白天撞疼你了吧？实在不好意思，婚礼人多太乱了":
            $ lc_add_affection(4)
            $ act2_flag = 2
        "今天婚礼的捧花寓意超好，没想到我们这么有缘分":
            $ lc_add_affection(6)
            $ act2_flag = 3
 
        
    













