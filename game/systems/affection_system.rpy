# Hidden affection state and shared mutation API.

default lc_affection = 0

init python:
    def _lc_int(value, value_name):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError("{0} must be an integer-compatible value.".format(value_name))


    def _lc_clamp_affection(value):
        numeric_value = _lc_int(value, "affection")
        return max(LC_AFFECTION_MIN, min(LC_AFFECTION_MAX, numeric_value))


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


    def _lc_log_affection_change(old_value, new_value, source):
        if source:
            renpy.log(
                "lc_affection {0}->{1} source={2}".format(
                    old_value,
                    new_value,
                    source,
                )
            )


    def lc_get_affection():
        return _lc_clamp_affection(lc_affection)


    def lc_add_affection(delta, source=""):
        current_value = lc_get_affection()
        numeric_delta = _lc_int(delta, "delta")
        return lc_set_affection(current_value + numeric_delta, source)


    def lc_set_affection(value, source=""):
        global lc_affection

        old_value = lc_get_affection()
        new_value = _lc_clamp_affection(value)
        lc_affection = new_value
        _lc_log_affection_change(old_value, new_value, source)
        return lc_affection


    def lc_get_affection_tier():
        tier_key, min_value, max_value, ending_key = _lc_affection_rule_for(lc_get_affection())
        return tier_key


    def lc_get_ending_key():
        tier_key, min_value, max_value, ending_key = _lc_affection_rule_for(lc_get_affection())
        return ending_key
