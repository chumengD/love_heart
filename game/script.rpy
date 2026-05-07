# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define e = Character("艾琳")
define e1 = Character("莱马")

# 游戏在此开始。

label start:


    $ wx_start_scripted_chat("1", "1")

    call screen wx_phone

    e "接下来打开自由输入微信聊天示例。"

    $ wx_start_free_chat("91")

    call screen wx_phone

    e "最后打开朋友圈示例。"

    $ wx_set_view("moments")

    call screen wx_phone

    # 此处为游戏结尾。

    return
