# 隐藏好感度系统。
# 这个文件只负责“保存好感度”和“提供统一读写接口”，不负责 UI 展示。

# 玩家当前好感度。
# 用 default 而不是普通 Python 全局变量，是为了让 Ren'Py 存档和回滚能正确记录这个状态。
# 以后不要在普通 .py 文件里另建第二套好感度变量，剧情、微信、结局都应该通过下面的 lc_* 函数访问。
default lc_affection = 0

init python:
    # 把外部传入的值转成整数。
    # 这样剧情里写 lc_add_affection("5") 也能工作；如果完全不能转，会抛出明确错误。
    def _lc_int(value, value_name):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError("{0} must be an integer-compatible value.".format(value_name))


    # 统一限制好感度范围。
    # 所有设置和增减都必须经过这里，保证最终不会低于 LC_AFFECTION_MIN，也不会高于 LC_AFFECTION_MAX。
    def _lc_clamp_affection(value):
        numeric_value = _lc_int(value, "affection")
        return max(LC_AFFECTION_MIN, min(LC_AFFECTION_MAX, numeric_value))


    # 根据当前好感度查找分层和结局。
    # 阈值不写死在函数里，而是从 data/ending_rules.rpy 的 LC_AFFECTION_TIER_RULES 读取，方便之后集中调整。
    def _lc_affection_rule_for(value):
        affection_value = _lc_clamp_affection(value)

        for tier_key, min_value, max_value, ending_key in LC_AFFECTION_TIER_RULES:
            if min_value <= affection_value <= max_value:
                return tier_key, min_value, max_value, ending_key

        return (
            LC_DEFAULT_AFFECTION_TIER,
            LC_AFFECTION_MIN,
            LC_AFFECTION_MAX,
            LC_DEFAULT_ENDING_KEY,
        )


    # 开发排查日志。
    # source 只写入 Ren'Py log，不会显示给玩家；调用时建议写明来源，例如 "wechat:1:choice:0"。
    def _lc_log_affection_change(old_value, new_value, source):
        if source:
            renpy.log(
                "lc_affection {0}->{1} source={2}".format(
                    old_value,
                    new_value,
                    source,
                )
            )


    # 读取当前好感度。
    # 剧情判断、开发控制台检查都用这个函数，不要直接读 lc_affection，避免读到未来改动前的内部实现。
    def lc_get_affection():
        return _lc_clamp_affection(lc_affection)


    # 增减好感度。
    # delta 可以是正数或负数，例如 lc_add_affection(5, source="chapter_01_help")。
    # 微信剧本选项和自由输入评分都走这个函数，保证所有入口逻辑一致。
    def lc_add_affection(delta, source=""):
        current_value = lc_get_affection()
        numeric_delta = _lc_int(delta, "delta")
        return lc_set_affection(current_value + numeric_delta, source)


    # 直接设置好感度。
    # 主要用于初始化、测试或特殊剧情事件；普通选项更推荐用 lc_add_affection()。
    # value 会被 clamp 到 0-100，source 只用于日志排查，不显示给玩家。
    def lc_set_affection(value, source=""):
        global lc_affection

        old_value = lc_get_affection()
        new_value = _lc_clamp_affection(value)
        lc_affection = new_value
        _lc_log_affection_change(old_value, new_value, source)
        return lc_affection


    # 获取当前好感分层 key。
    # 返回值来自 LC_AFFECTION_TIER_RULES 的第一项，例如 "low"、"normal"、"high"、"true"。
    # 适合剧情里做轻量分支：if lc_get_affection_tier() == "high": ...
    def lc_get_affection_tier():
        tier_key, min_value, max_value, ending_key = _lc_affection_rule_for(lc_get_affection())
        return tier_key


    # 获取当前结局 key。
    # 结局路由 label 里建议只调用这个函数，再根据返回字符串 jump 到不同结局。
    # 以后改阈值或结局 key 时，只需要改 data/ending_rules.rpy。
    def lc_get_ending_key():
        tier_key, min_value, max_value, ending_key = _lc_affection_rule_for(lc_get_affection())
        return ending_key
