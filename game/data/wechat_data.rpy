# WeChat module static data.
#
# Image paths should point to files under game/, for example:
# "images/wechat/heroine_avatar.jpg".

define WX_PLAYER_CONTACT_ID = "player"
define WX_DEFAULT_CONTACT_ID = "heroine"

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

define wx_scripted_chats = {
    "1": {
        "title": "微信聊天示例",
        "start_node": "1",
        "nodes": {
            "1": {
                "messages": [
                    {"speaker": "heroine", "text": "上司又乱朝我发脾气了"},
                    {"speaker": "heroine", "text": "明明不是我的错"},
                    {"speaker": "player", "text": "不是你的错"},
                ],
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
                "messages": [
                    {"speaker": "heroine", "text": "那就先这样，之后再聊。"},
                ],
                "choices": [],
            },
        },
    },
}

define wx_free_chats = {
    "91": {
        "title": "自由聊天示例",
        "initial_messages": [
            {"speaker": "heroine", "text": "我的发圈丢了"},
        ],
        "context": {
            "scene": "男主要安慰女主，想办法逗女主开心，忘掉不高兴，不能偏离主题太远。",
            "scoring_rule": "在别的话题深入会降低好感度，恰当的关心会提高好感度，过于明显亲密的关心会稍微降低好感度。",
            "positive_keywords": ["没事", "别难过", "我陪你", "一起找", "发圈", "开心", "安慰"],
            "negative_keywords": ["无所谓", "别烦", "不关我事", "活该", "换个话题"],
            "too_intimate_keywords": ["宝贝", "老婆", "亲爱的"],
        },
    },
}

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
