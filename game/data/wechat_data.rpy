# 微信模块静态数据。
# 这个文件只放“以后经常会改的内容”：联系人、聊天剧本、自由聊天配置、朋友圈内容。
# 界面布局在 screens/wechat_screens.rpy，运行逻辑在 systems/wechat_system.rpy。
# 图片路径要写 game/ 目录下的相对路径，例如："images/wechat/heroine_avatar.jpg"。

# 玩家联系人 id。
# 聊天记录里 speaker 写 "player" 时，会用男主的头像、名字和气泡方向。
define WX_PLAYER_CONTACT_ID = "player"

# 默认女主联系人 id。
# 如果某条消息没写 speaker，系统会按这个联系人处理。
define WX_DEFAULT_CONTACT_ID = "heroine"

# 联系人表。
# 以后要改名字、头像、左右方向，就改这里：
# name：显示在朋友圈作者名里，也用作头像缺失时的首字 fallback。
# avatar：头像图片路径，必须是 game/ 下的相对路径；文件不存在时会显示 fallback_color 色块。
# side：聊天气泡方向，"right" 是右侧，"left" 是左侧。
# fallback_color：头像图片没放好时的兜底色，方便开发阶段不报错。
define wx_contacts = {
    "heroine": {
        "name": "一只女主角",
        "avatar": "images/wechat/heroine_avatar.jpg",
        "side": "right",
        "fallback_color": "#f47f9a",
    },
    "player": {
        "name": "男主",
        "avatar": "images/wechat/player_avatar.png",
        "side": "left",
        "fallback_color": "#9fb5c6",
    },
}

# 剧本选项推进版聊天数据。
# 外层 key 是 chat_id，剧情里用 wx_start_scripted_chat("1", "1") 打开。
# start_node 是默认起始节点；nodes 里每个 key 是 node_id。
define wx_scripted_chats = {
    "1": {
        "title": "微信聊天示例",
        "start_node": "1",
        "nodes": {
            "1": {
                # messages 是进入这个节点时自动追加的聊天记录。
                # speaker 必须对应 wx_contacts 里的联系人 id；text 是气泡文字。
                "messages": [
                    {"speaker": "heroine", "text": "上司又乱朝我发脾气了"},
                    {"speaker": "heroine", "text": "明明不是我的错"},
                    {"speaker": "player", "text": "不是你的错"},
                ],
                # choices 是底部选项。
                # text：按钮上看到的文字。
                # player_text：玩家点选后，男主真正发出去的气泡文字。
                # reply_messages：选项后女主追加回复。
                # affection_delta：这次选择对好感度的影响，会调用 lc_add_affection()。
                # next：跳到同一个 chat_id 下的下一个 node_id。
                # next_label：如果以后要直接跳剧情 label，可加这个字段，逻辑层会优先 renpy.jump(next_label)。
                "choices": [
                    {
                        "text": "明天出去玩吧",
                        "player_text": "明天要不要出去玩？",
                        "reply_messages": [
                            {"speaker": "heroine", "text": "好啊，去哪里玩"},
                        ],
                        "affection_delta": 5,
                        "next": "2",
                    },
                    {
                        "text": "讲个笑话",
                        "player_text": "这是一个笑话",
                        "reply_messages": [
                            {"speaker": "heroine", "text": "这个笑话有点冷。"},
                        ],
                        "affection_delta": -3,
                        "next": "2",
                    },
                ],
            },
            "2": {
                # choices 为空时，底部会显示“暂无可选回复”。
                # 以后想让这个节点继续分支，就在 choices 里继续加选项字典。
                "messages": [
                    {"speaker": "heroine", "text": "那就先这样，之后再聊。"},
                ],
                "choices": [],
            },
        },
    },
}

# 自由输入聊天配置。
# 外层 key 是 chat_id，剧情里用 wx_start_free_chat("91") 打开。
# AI 接入暂时不写真实网络请求，后续只需要替换 systems/wechat_system.rpy 里的 wx_generate_ai_reply()。
define wx_free_chats = {
    "91": {
        "title": "自由聊天示例",
        # 打开自由聊天时先显示这些初始消息。
        "initial_messages": [
            {"speaker": "heroine", "text": "我的发圈丢了"},
        ],
        # context 是本轮自由聊天的上下文。
        # scene 给未来 AI 回复生成使用；scoring_rule 是给开发者看的评分说明。
        # positive_keywords / negative_keywords / too_intimate_keywords 会被 wx_score_player_input() 读取，
        # 用来计算本次自由输入的好感变化，最终变化会 clamp 到 -10 到 +10。
        "context": {
            "scene": "男主要安慰女主，想办法逗女主开心，忘掉不高兴，不能偏离主题太远。",
            "scoring_rule": "在别的话题深入会降低好感度，恰当的关心会提高好感度，过于明显亲密的关心会稍微降低好感度。",
            "positive_keywords": ["没事", "别难过", "我陪你", "一起找", "发圈", "开心", "安慰"],
            "negative_keywords": ["无所谓", "别烦", "不关我事", "活该", "换个话题"],
            "too_intimate_keywords": ["宝贝", "老婆", "亲爱的"],
        },
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
define wx_moment_posts = (
    {
        "post_id": "moment_001",
        "author": "heroine",
        "time": "昨天",
        "text": "今天好累啊，终于下班了",
        "images": (),
    },
    {
        "post_id": "moment_002",
        "author": "heroine",
        "time": "20分钟前",
        "text": "我想去看一下猫~",
        "images": (
            "images/wechat/moment_sample_1.png",
            "images/wechat/moment_sample_2.png",
        ),
    },
)
