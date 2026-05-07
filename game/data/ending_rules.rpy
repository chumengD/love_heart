# 隐藏好感度的统一规则表。
# 以后只要想改“多少好感进入哪个结局”，优先改这个文件，不要去剧情文件里散落写判断。

# 好感度允许范围。所有写入最终都会被 lc_set_affection() clamp 到这个区间。
# 如果以后想改成 0-200，先改这里，再同步检查剧情阈值是否覆盖完整范围。
define LC_AFFECTION_MIN = 0
define LC_AFFECTION_MAX = 100

# 好感度分层规则。
# 每条格式固定为：
# ("分层key", 最小值_包含, 最大值_包含, "结局key")
# 例：("high", 60, 84, "high_affection") 表示 60-84 是高好感，对应结局 key 为 high_affection。
# 以后调结局阈值时，只改第二、第三个数字；改结局跳转目标时，只改第四个字符串。
# 注意：区间要连续覆盖 LC_AFFECTION_MIN 到 LC_AFFECTION_MAX，避免某个好感值找不到结局。
define LC_AFFECTION_TIER_RULES = (
    ("low", 0, 24, "low_affection"),
    ("normal", 25, 59, "normal_affection"),
    ("high", 60, 84, "high_affection"),
    ("true", 85, 100, "true_ending"),
)

# 兜底规则。只有当上面的阈值表漏配时才会用到。
# 正常剧情里请调用 lc_get_affection_tier() 或 lc_get_ending_key()，不要直接读这两个默认值。
define LC_DEFAULT_AFFECTION_TIER = "normal"
define LC_DEFAULT_ENDING_KEY = "normal_affection"
