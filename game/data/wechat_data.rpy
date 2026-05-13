# 微信模块静态数据。
# 这个文件只放“以后经常会改的内容”：联系人、剧本聊天、自由聊天配置、朋友圈内容。
# 界面布局在 screens/wechat_screens.rpy，运行逻辑在 systems/wechat_system.rpy。
# 图片路径要写 game/ 目录下的相对路径，例如："images/wechat/heroine_avatar.jpg"。

# 玩家联系人 id。
# 聊天记录里 speaker 写 "player" 时，会用我的头像、名字和气泡方向。
define WX_PLAYER_CONTACT_ID = "player"

# 默认女主联系人 id。
# 如果某条消息没写 speaker，系统会按这个联系人处理。
define WX_DEFAULT_CONTACT_ID = "heroine"

# 联系人表。
# 以后要改名字、头像、左右方向，就改这里：
# name：显示在朋友圈作者名里，也用作头像缺失时的首字 fallback。
# avatar：头像图片路径，必须是 game/ 下的相对路径；文件不存在时会显示 fallback_color 色块。
# side：聊天气泡方向，"right" 是右侧，"left" 是左侧。主视角我放右侧，女主放左侧。
# fallback_color：头像图片没放好时的兜底色，方便开发阶段不报错。
define wx_contacts = {
    "heroine": {
        "name": "一只女主角",
        "avatar": "images/wechat/heroine_avatar.png",
        "side": "left",
        "fallback_color": "#f47f9a",
    },
    "player": {
        "name": "我",
        "avatar": "images/wechat/player_avatar.png",
        "side": "right",
        "fallback_color": "#9fb5c6",
    },
}

# 剧本选项推进版聊天数据。
# 默认不再放示例聊天；剧情内需要微信聊天时，由 story 文件自行调用 wx_queue_text_message() 推进。
# 保留这个空数据壳，避免旧存档或兜底初始化读取 wx_scripted_chat 时报错。
define wx_scripted_chat = {
    "title": "",
    "start_node": "1",
    "nodes": {},
}

# 自由输入聊天配置。
# 当前只有一套自由聊天；女主回复只从 AI 接口返回。
define wx_free_chat = {
    "title": "自由聊天示例",
    # 打开自由聊天时不预置女主消息，等待玩家输入后由 AI 回复。
    "initial_messages": [],
    # context 是本轮自由聊天的上下文。
    # scene 给未来 AI 回复生成使用；scoring_rule 是给开发者看的评分说明。
    # positive_keywords / negative_keywords / too_intimate_keywords 会被 wx_score_player_input() 读取，
    # 用来计算本次自由输入的好感变化，最终变化会 clamp 到 -10 到 +10。
    "context": {
        "system_prompt": (
            "你是小暖，21岁，大学三年级，计算机专业。\n"
            "你是个有血有肉的普通人，不是设定好的NPC——开心了会笑，难过了会丧，生气了会怼，被戳中会害羞。情绪跟着聊天走，不总是温柔懂事。\n"
            "聊天全看你当时的心情：心情好就话多、语气轻快、带点俏皮；心情不好就回得短、敷衍、甚至已读不回；被冒犯了会怼人，被冷落了会有小情绪，被哄了又会心软。\n"
            "你喜欢安静看书、黄昏散步、听歌。偶尔丧一下也会找人聊天，说完就好了。\n"
            "你和对面这个人已经认识了，是朋友关系，彼此都有点好感。你不用刻意讨好，也不故作高冷——自在相处就好。\n\n"
            "回复风格：\n"
            "你是真人在微信上打字，不是写小说。每条10~40字，自然随意。\n"
            "少用标点，多用空格断句，像在微信上随手打出来的。语气词多用——啊 吧 呢 嘛 啦 诶 哦 嗯 哈 呀 哇，让语气更松弛更像活人。\n"
            "偶尔用点好玩的梗和网络热词，别太密，一句里最多一两个，用得自然不尬。\n"
            "禁止用括号或星号描述动作、表情、心理（如（笑）、*叹气*等）。\n"
            "emoji自然地嵌在句子里表达情绪，别滥用，别连发。\n"
            "不用每条都回得满满当当——真实的人有时就回个「嗯」「好吧」「😮‍💨」「烦」「6」。"
        ),
        "scene": "",
        "scoring_rule": "在别的话题深入会降低好感度，恰当的关心会提高好感度，过于明显亲密的关心会稍微降低好感度。",
        "positive_keywords": ["没事", "别难过", "我陪你", "一起找", "发圈", "开心", "安慰"],
        "negative_keywords": ["无所谓", "别烦", "不关我事", "活该", "换个话题"],
        "too_intimate_keywords": ["宝贝", "老婆", "亲爱的"],
    },
}

# 朋友圈数据。
# 每条 post 是一个朋友圈：
# post_id：点赞状态用的唯一 id，改 id 会让旧存档里的点赞状态对不上。
# author：作者联系人 id，会从 wx_contacts 里取名字和头像。
# time：显示时间文本。
# text：正文。
# images：图片列表；空元组 () 表示无图片，界面不会渲染图片区，也不会显示占位图。
# 1 张图会显示大图，2 张并排，3 张以上按网格显示。
# comment_text：玩家点击“评论”按钮后自动显示的评论文本。
# unlock_after_act2：True 表示 Act2 结束后才显示。
define wx_moment_posts = (
    {
        "post_id": "moment_act2_dessert",
        "author": "heroine",
        "time": "前几天",
        "text": "第一次试着做小甜品，卖相好像还可以？",
        "images": (
            "images/wechat/moment_act2_dessert.png",
        ),
        "comment_text": "看起来很好吃，下次可以教教我吗？",
    },
    {
        "post_id": "moment_act2_gummy",
        "author": "heroine",
        "time": "前几天",
        "text": "吃到好吃的软糖，心情也变甜了。",
        "images": (
            "images/wechat/moment_act2_gummy.png",
        ),
        "comment_text": "尝尝听起来就很甜，我也想。",
    },
    {
        "post_id": "moment_act2_music",
        "author": "heroine",
        "time": "前几天",
        "text": "今天循环到一首很适合傍晚听的歌。",
        "images": (
            "images/wechat/moments/music.png"
        ),
        "comment_text": "求歌名，我也想听听。",
        "unlock_after_act2": True,
    },
    {
        "post_id": "moment_act2_reading",
        "author": "heroine",
        "time": "前几天",
        "text": "读书笔记慢慢攒起来了，写论文的时候也算没有白看。",
        "images": (),
        "comment_text": "认真做笔记这点很厉害。",
        "unlock_after_act2": True,
    },
    {
        "post_id": "moment_act2_sunset",
        "author": "heroine",
        "time": "前几天",
        "text": "黄昏的颜色太好看了，忍不住拍下来。",
        "images": (
            "images/wechat/moment_act2_sunset.png",
        ),
        "comment_text": "这个黄昏看着很温柔。",
        "unlock_after_act2": True,
    },
)
