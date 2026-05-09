# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

image m normal ="images/Characters/_asuka.png1"
image g normal = "images/Characters/_ayalin.png1"

transform left:
    zoom 0.65
    xanchor 0.5
    yanchor 0.5
    xpos 180
    ypos 1150

transform right:
    zoom 0.65
    xanchor 0.5
    yanchor 0.5
    xpos 1760
    ypos 1150


#使角色图层高于文本框   
init -2 python:
    renpy.add_layer("character_front", above="screens")

    config.tag_layer["m"] = "character_front"
    config.tag_layer["g"] = "character_front"

    config.tag_zorder["m"] = 100
    config.tag_zorder["g"] = 100



define m = Character("男主", image="m",what_color="#4874CB")
define g = Character("女主", image="g",what_color="#EF939E")
define g_right =Character("女主", 
    image="g",
    what_color="#EF939E",
    namebox_xpos=1600,
    namebox_xanchor=1.0,
    who_xalign=1.0,)


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
    call Act1_wedding

    call Act2_wx
    
    $ wx_start_scripted_chat()

    show screen wx_phone

    call wx_scripted_chat_flow

    hide screen wx_phone

    $ wx_start_free_chat()

    call screen wx_phone

    # 此处为游戏结尾。

    return


