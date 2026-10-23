========================================================================
【免费分享声明】
本项目（技能说明、作曲引擎代码、示例曲与项目文档）由创作者 reaesteve 免费分享，仅供个人学习与非商业使用。
禁止以任何名义出售、转售或打包售卖本项目，禁止通过付费下载、付费会员、付费课程、付费社群、
“打赏/关注后获取”、引流收费等任何形式收取费用或设置付费门槛。
可以免费转发与修改，但必须注明出处、保留本声明，并以相同许可免费分享。
用本技能创作的音乐归创作者本人所有；以上限制针对的是本项目本身。
许可：知识共享 署名-非商业性使用-相同方式共享 4.0 国际（CC BY-NC-SA 4.0）
https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans
第三方组件（GeneralUser GS 音色库、TinySoundFont）沿用其各自的原始许可。
如果你是付费获得本项目的，请注意：它本来就是免费的。
========================================================================

代码作曲技能（公开版）

用途：根据提示词，用代码写出原创乐曲，并用免费音色库渲染成 song.wav。
本文件夹只包含技能、通用作曲引擎和音色库，不包含任何具体作品的总谱、音频、画面或提示词。

目录
  SKILL.md                         技能说明（可直接装进 Claude，或给人阅读）
  engine\                          作曲引擎
      compose_kit.py               作曲函数库：速度变化、旋律、和弦、低音、鼓、表情、导出
      example_song.py              一首约 47 秒的原创示例曲，复制它开始写自己的曲子
      render.c、tsf.h              SoundFont 渲染器（TinySoundFont，MIT 许可）
      mix_kit.py                   混音：音量、声像、混响、压缩、限幅
      build.bat / build.sh         一键生成：python 曲子脚本 → 分轨渲染 → song.wav
      requirements.txt             Python 依赖（numpy、scipy）
  sound_library\GeneralUser-GS\   音色库 GeneralUser GS v2.0.3（S. Christian Collins，可免费用于个人和商业音乐）
                                   分为 4 段，首次构建时自动合并；也可双击「合并音色库.bat」

使用（Windows）
  1. 安装 Python 3.10+ 和一个 C 编译器（推荐 w64devkit 或 MinGW 的 gcc）。
  2. 在 engine 文件夹中运行：build.bat example_song.py
  3. 写自己的曲子：复制 example_song.py，改名修改后运行 build.bat 新文件名.py
