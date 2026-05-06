# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define e = Character("艾琳")
define e1 = Character("莱马")

# 游戏在此开始。

label start:

    # 显示一个背景。此处默认显示占位图，但您也可以在图片目录添加一个文件
    # （命名为 bg room.png 或 bg room.jpg）来显示。

    scene bg room

    # 显示角色立绘。此处使用了占位图，但您也可以在图片目录添加命名为
    # eileen happy.png 的文件来将其替换掉。

    show eileen happy

    # 此处显示各行对话。

    e "您已创建一个新的 Ren'Py 游戏。"

    e "当您完善了故事、图片和音乐之后，您就可以向全世界发布了！"

    # e1 "你好，我是莱马"

    e "我该怎么称呼你？"

    e "艾琳就可以了"

    e "接下来打开剧本微信聊天示例。点击右上角齿轮可以返回主流程。"

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
