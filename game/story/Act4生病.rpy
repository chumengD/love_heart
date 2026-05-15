# define flag =0
# init python:
#     affection = lc_get_affection()
#     #todo 多高的好感度才算高？
#     if (affection>50):
#         flag =1

image takeaway = "images/Act4/takeaway.png"

label Act4_sick:
    $ quick_menu_phone_target = "ai"
    $ act4_affection_before = lc_get_affection()

    show watch_phone
    if act4_affection_before >= 50:
        "自那次黄昏偶遇过后，我们之间的暧昧感愈发明显"
        "聊天不再是简单的客套寒暄，偶尔会互道晚安，分享深夜碎碎念"
        "我躺在床上，漫无目的滑动手机，习惯性等待她的消息。"
    else:
        "自那次黄昏偶遇过后，我们之间的距离悄悄拉近，却又保持着恰到好处的分寸。"
        "我躺在床上，漫无目的滑动手机"
        "手指总会下意识停在她的聊天界面，却不敢主动打扰"
        "我希望走进她的世界"
        "但不清楚她对我是什么感觉，也不敢擅自揣测她的心意。"
        "突然，她发来一条消息"
    hide watch_phone
   
    $ wx_start_scripted_chat()
    show screen wx_phone
    $ wx_queue_text_message("heroine", "我好像感冒发烧了，浑身难受。")
    call wx_click_reveal_pending_message
    #change 这里是不是有点奇怪，我们根本就没有正在输入中
    "聊天界面上方一直显示着“对方正在输入中”。"
    "隔着屏幕什么都做不了，我到底该怎么回复她？"

    menu:
        "怎么关心她？"
        "多喝热水，好好休息，早点睡觉":
            $ lc_add_affection(-6)
            $ lc_set_choice_flag("act4_sick_reply", "hot_water")
            $ wx_queue_text_message("player", "多喝热水，好好休息，早点睡觉。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "......好。")
            call wx_click_reveal_pending_message
            "她不再多说，聊天框安静下来。"
            "这句关心太敷衍了，反而让她的情绪更低落。"
            $ lc_grant_achievement("straight_guy")

        "发烧严重吗？有没有吃药？要不要去医院？":
            $ lc_add_affection(15)
            $ lc_set_choice_flag("act4_sick_reply", "care_questions")
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
            hide screen wx_phone
            show watch_phone
            "关掉微信聊天界面后，我还是静不下来"
            "一想到她一个人躺在床上难受，我就急得像热锅上的蚂蚁"
            "翻来覆去后，我决定做点实际的事"
            hide watch_phone
            show takeaway
            with dissolve
            "我点开手机里的外卖软件，认真地挑选温和感冒药、退烧贴、暖胃的清淡小米粥，顺带加了几包暖宝宝和润喉糖。"
            "并在备注一栏写下：喝了药早点休息哦，有需要就给我打电话。"
            "我再次打开微信"
            hide takeaway
            with dissolve
            show screen wx_phone
            $ wx_queue_text_message("player", "我刚刚给你点了外卖，里面有药和粥，还有暖宝宝，你记得吃了药早点休息哦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "谢谢你……从来没有人对我这么细心....")
            call wx_click_reveal_pending_message
            "看到这条信息，我的心脏猛地一跳"
            "血液奔涌过全身，心里的慌乱被激动的大军冲乱了阵脚"
            "我从床上蹦起，在房间里转了几步，才让自己稍微冷静下来。"
            m "冷静，冷静啊我！"
            m "现在不是高兴的时候，要去担心她才对呀!"
            "我再度看向手机"
            $ wx_queue_text_message("player", "没事没事")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("player", "你能感受到我的这份关心，好好养病就好了")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "好....")
            call wx_click_reveal_pending_message
            $ lc_grant_achievement("perfect_care")
            "我放下手机，望着天花板，心里久久不能平静。"
            pause
        "都怪我没早点关心你，我现在就去找你":
            $ lc_add_affection(5)
            $ lc_set_choice_flag("act4_sick_reply", "rush_over")
            $ wx_queue_text_message("player", "都怪我没早点关心你，我现在就去找你。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "不用啦，现在太晚了。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "而且外面很冷，别特意跑过来啦。")
            call wx_click_reveal_pending_message
            $ wx_queue_text_message("heroine", "我休息一晚就好。")
            call wx_click_reveal_pending_message
            "她委婉拒绝了我的冲动，却还是能感受到我是真的着急。"

    hide screen wx_phone
    return
