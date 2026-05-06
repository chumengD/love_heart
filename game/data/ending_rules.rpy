# Hidden affection tier and ending rules.
#
# Each rule is:
# (tier_key, min_inclusive, max_inclusive, ending_key)
# Keep these thresholds here so later story files only read lc_get_ending_key().

define LC_AFFECTION_MIN = 0
define LC_AFFECTION_MAX = 100

define LC_AFFECTION_TIER_RULES = (
    ("low", 0, 24, "low_affection"),
    ("normal", 25, 59, "normal_affection"),
    ("high", 60, 84, "high_affection"),
    ("true", 85, 100, "true_ending"),
)

define LC_DEFAULT_AFFECTION_TIER = "normal"
define LC_DEFAULT_ENDING_KEY = "normal_affection"
