# 成就系统接口。
# 剧情只调用 lc_grant_achievement(id)，不要直接操作 achievement API。

init python:
    def _lc_register_achievements():
        for item in LC_ACHIEVEMENTS:
            achievement.register(item["id"])


    _lc_register_achievements()


    def lc_achievement_by_id(achievement_id):
        for item in LC_ACHIEVEMENTS:
            if item["id"] == achievement_id:
                return item

        return None


    def lc_achievement_icon(item):
        icon = item.get("icon") or LC_ACHIEVEMENT_PLACEHOLDER_ICON

        if renpy.loadable(icon):
            return icon

        return LC_ACHIEVEMENT_PLACEHOLDER_ICON


    def lc_has_achievement(achievement_id):
        return achievement.has(achievement_id)


    def lc_unlocked_achievements():
        return [item for item in LC_ACHIEVEMENTS if lc_has_achievement(item["id"])]


    def lc_grant_achievement(achievement_id):
        item = lc_achievement_by_id(achievement_id)

        if item is None:
            raise ValueError("Unknown achievement id: {0}".format(achievement_id))

        if achievement.has(achievement_id):
            return False

        achievement.grant(achievement_id)
        renpy.show_screen("lc_achievement_toast", achievement_id)
        return True
