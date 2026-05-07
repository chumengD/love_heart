# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define e = Character("艾琳")
define e1 = Character("莱马")

image logo ="images/logo.png"

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
    "首先展示一下我的screen"
    show screen mysc
    
    pause 2.0

    $ wx_start_scripted_chat()

    show screen wx_phone

    call wx_scripted_chat_flow

    hide screen wx_phone

    $ wx_start_free_chat()

    call screen wx_phone

    # 此处为游戏结尾。

    return
