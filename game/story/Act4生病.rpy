# define flag =0
# init python:
#     affection = lc_get_affection()
#     #todo 多高的好感度才算高？
#     if (affection>50):
#         flag =1



label Act4_sick:
    $ quick_menu_phone_target = "ai"
    $ act4_affection_before = lc_get_affection()

    if act4_affection_before >= 50:
        "自那次黄昏偶遇过后，我们之间的暧昧感愈发明显"
        "聊天不再是简单的客套寒暄，偶尔会互道晚安，分享深夜碎碎念"
        #change 感觉这里也得添加一些微信聊天动画
        "我躺在床上，漫无目的滑动手机，习惯性等待她的消息。"
    else:
        "自那次黄昏偶遇过后，我们之间的距离悄悄拉近，却又保持着恰到好处的分寸。"
        "我躺在床上，漫无目的滑动手机"
        "手指总会下意识停在她的聊天界面，却不敢主动打扰"
        "我希望走进她的世界"
        "但不清楚她对我是什么感觉，也不敢擅自揣测她的心意。"
    "突然，她发来一条消息"
    #todo 微信聊天的内容
    $ wx_start_scripted_chat()
    show screen wx_phone
    pause 0.4
    $ wx_queue_text_message("heroine", "我好像感冒发烧了，浑身难受。")
    call wx_click_reveal_pending_message
    $ quick_menu_phone_target = "takeaway_cg"
    "聊天界面上方一直显示着“对方正在输入中”。"
    "隔着屏幕什么都做不了，我到底该怎么回复她？"

    menu:
        "怎么关心她？"
        "多喝热水，好好休息，早点睡觉":
            $ lc_add_affection(-6)
            $ wx_queue_text_message("player", "多喝热水，好好休息，早点睡觉。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "......好。")
            call wx_click_reveal_pending_message
            "她不再多说，聊天框安静下来。"
            "这句关心太敷衍了，反而让她的情绪更低落。"

        "发烧严重吗？有没有吃药？要不要去医院？":
            $ lc_add_affection(10)
            $ wx_queue_text_message("player", "发烧严重吗？有没有吃药？要不要去医院？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "我好像只是低烧，暂时还没有吃退烧药。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "但是我浑身酸酸痛痛的，好难受呀。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "怎么突然发烧啦？是着凉感冒了吗？还是哪里有炎症呀？")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "我感觉是感冒了......鼻子堵堵的。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "那先喝点感冒药哦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "晚上睡觉枕头可以垫高一点，鼻子会舒服一些。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "嗯嗯。")
            call wx_click_reveal_pending_message
            "她耐心回应着每一句，像是真的从我的关心里得到了一点安慰。"

        "都怪我没早点关心你，我现在就去找你":
            $ lc_add_affection(5)
            $ wx_queue_text_message("player", "都怪我没早点关心你，我现在就去找你。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "不用啦，现在太晚了。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "而且外面很冷，别特意跑过来啦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "我休息一晚就好。")
            call wx_click_reveal_pending_message
            "她委婉拒绝了我的冲动，却还是能感受到我是真的着急。"

    menu:
        "要不要再做点实际的事？"
        "点外卖送药和清淡小米粥":
            $ lc_add_affection(12)
            "我没有急着继续打字安慰，指尖点开手机里的外卖软件。"
            "我认真挑选温和感冒药、退烧贴、暖胃的清淡小米粥，顺带加了几包暖宝宝和润喉糖。"
            "备注一栏写下：喝了药早点休息哦，有需要就给我打电话。"
            "半小时后，聊天框弹出一张实拍照片。"
            $ wx_queue_text_message("heroine", "【照片】外卖袋整齐摆在桌面，药品、热粥摆放清晰，灯光柔和。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "谢谢你……从来没有人对我这么细心....")
            call wx_click_reveal_pending_message
            "这一刻，只想好好守护她。"
            "触发成就：【满分关怀】"
        "先让她好好休息":
            $ wx_queue_text_message("player", "那你先好好休息，醒了记得告诉我一声。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "好。")
            call wx_click_reveal_pending_message
            "我把手机放在枕边，直到屏幕暗下去还在担心她。"

    hide screen wx_phone
    $ quick_menu_phone_target = "ai"
    return
