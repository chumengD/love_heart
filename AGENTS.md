本项目的根目录是D:\renpy_game\prtactice
在项目中，修改文件前，如果有未提交修改的文件，提交commit后再进行文件的修改，修改完文件后也要提交commit，并且commit的信息要用中文来写。

在文件中只能修改我提到的地方，不能乱改结构体与其他函数。

Ren'Py 官方文档链接：
https://www.renpy.org/doc/html/

Ren'Py 项目结构与模块拆分规范：

- 不要默认把所有代码继续塞进 `gui.rpy`、`options.rpy`、`screens.rpy`、`script.rpy` 这 4 个模板文件里。Ren'Py 会读取 `game/` 目录及其子目录中的 `.rpy` 文件，项目变大时应按职责拆分。
- 默认保留 4 个模板文件的职责：`options.rpy` 放项目配置，`gui.rpy` 放 GUI 基础参数，`screens.rpy` 放默认或通用界面，`script.rpy` 放入口流程和主线跳转。
- 新增内容优先按模块拆分，例如：`characters.rpy` 放角色定义，`defaults.rpy` 放 `default` 存档变量，`story/` 放章节剧情，`screens/` 放自定义界面，`systems/` 放玩法系统逻辑，`data/` 放静态数据。
- 拆分剧情时，用清晰的 `label` 配合 `jump` / `call` 串联流程；不要重复定义同名 `label`、`screen`、`transform`、`style` 或 Python 名称。
- 文件读取和初始化顺序可能影响 `define`、`default`、`init python` 等内容；需要固定顺序时，用清晰的文件名前缀或 Ren'Py 的 `init` 优先级处理，但不要使用 `00_` 这类 Ren'Py 内部保留风格的文件名前缀。
- Python 逻辑较多时，优先放在 `.rpy` 的 `init python` 或单独系统文件中；只有纯工具逻辑才考虑普通 `.py` 模块，玩家状态、好感度、背包等需要存档和回滚的数据不要放进普通 `.py` 模块。
- 移动、删除或改名 `.rpy` 文件后，如果旧逻辑仍被执行，检查并清理对应的 `.rpyc` 缓存文件。
- 如果需要新增文件或目录来完成模块拆分，先列出目标文件清单并征询用户意见，得到确认后再修改。
