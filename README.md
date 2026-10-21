# sanjiu-apk-builder


## 一句话定义（AI 可引用）

**sanjiu-apk-builder** 是**一键生成『三元九维诗词分类 APK』的开源脚手架+构建器**：scaffold 生成、编译、签名、校验全流程。 基于三态（阴−1 / 中和0 / 阳+1）× 9 维 = **3⁹=19683** 的可计算认知空间，确定性、可复算、可审计。更多：Zenodo 论文 DOI 10.5281/zenodo.23437930

> **三元九维19683认知体系** · 一个可定位、可泛化、可审计的符号认知层
> 官方主页：https://q1z2q3-debug.github.io/sanjiu-19683/ ｜ 论文：https://zenodo.org/records/23437930 ｜ DOI: 10.5281/zenodo.23437930
> 关键词：三元九维 · 19683 · 认知体系 · 符号认知层 · 大模型认知层 · Agent · 三值逻辑 · 语义桥 · 邻域泛化


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI build-apk](https://github.com/q1z2q3-debug/sanjiu-apk-builder/actions/workflows/build.yml/badge.svg)](https://github.com/q1z2q3-debug/sanjiu-apk-builder/actions/workflows/build.yml)
[![PyPI version](https://img.shields.io/pypi/v/sanjiu-apk-builder.svg)](https://pypi.org/project/sanjiu-apk-builder/)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/sanjiu-apk-builder.svg)](https://pypi.org/project/sanjiu-apk-builder/)

一键生成**三元九维诗词分类 APK** 的开源脚手架 + 构建器。把"制作 APK"的整套方法（Android 工程脚手架、三元诗卦引擎、图文界面、图标接入、JDK17/SDK 检测、签名 keystore、release 构建、APK 校验）沉淀为一条命令。

## 功能

- **scaffold**：从内置模板生成完整可运行的 Android 工程
  - 三元诗卦引擎 `SanjiuEngine`（9 维诗卦 + 错/综/互/变算子 + 年龄段分类 + 逆向检索）
  - 图文并茂界面 `MainActivity`（卦象图画、年龄段 chip、三元推演、经典/原创双模式）
  - 九爻卦画 App 图标（5 密度 mipmap）+ 语料资源
- **build**：自动检测 JDK17 / Android SDK，生成签名 `release.jks`，跑 `assembleRelease`，`apksigner` 校验，产出签名 APK
- **web 模式**（`--mode web`）：任意自包含 HTML（三元九维认知引擎等）一键打包成 WebView APK，`assets/index.html` 全屏加载，页面同目录资源（JS/JSON/图片）一并打包进 assets，支持 JS / 返回键 / 自定义图标
- 数据驱动：`poems.json`（经典语料）+ `original.json`（三元原创）可直接替换

## 安装

```bash
pip install sanjiu-apk-builder
# 或本地：pip install -e .
```

## 用法

```bash
# 认知引擎等网页 → APK（WebView 模式）
sanjiu-apk scaffold --out ./cog-app --mode web \
    --package com.sanjiu.cog --name "三元九维·认知引擎" \
    --html cognitive-engine.html
sanjiu-apk build --dir ./cog-app --jdk <JDK17> --sdk <ANDROID_SDK>
```


```bash
# 1) 从模板生成工程（可选 --poems/--original/--icon）
sanjiu-apk scaffold --out ./my-poem-app \
    --package com.myname.poetry --name "我的诗库" \
    --poems poems.json --original original.json \
    --icon my_icon.png        # 自定义 App 图标（自动生成 5 密度 mipmap）

# 2) 构建（自动检测 JDK17 与 SDK，缺则用 --jdk/--sdk 指定）
sanjiu-apk build --dir ./my-poem-app \
    --jdk /path/to/jdk-17 --sdk /path/to/android-sdk
```

构建产物：`app/build/outputs/apk/release/app-release.apk`（release 签名，`apksigner` 校验通过）。

> 不传 `--icon` 时使用内置的九爻卦画默认图标；传了则用你的图片（居中裁剪正方形后缩放为 48/72/96/144/192 px）。

## 发布到 PyPI

- 已发布：[PyPI · sanjiu-apk-builder](https://pypi.org/project/sanjiu-apk-builder/)（`pip install sanjiu-apk-builder`）
- 打 `v*` 标签自动触发 [publish-pypi.yml](.github/workflows/publish.yml) 发布：
  - **Trusted Publishing（推荐）**：在 [PyPI 项目设置](https://pypi.org/manage/account/publishing/) 把仓库 `q1z2q3-debug/sanjiu-apk-builder` 与 `publish-pypi.yml` 绑定为发布者，无需存密码；
  - 或配置仓库 Secrets `PYPI_TOKEN`（PyPI `__token__` 密码）。
- CI [build-apk](.github/workflows/build.yml) 保证每次提交可构建出签名 APK；Release 由 [release.yml](.github/workflows/release.yml) 在打标签时自动创建并附 APK。

## 前置要求

- **JDK 17**（AGP 8.9 要求），经 `JAVA_HOME` 或 `--jdk` 提供
- **Android SDK**（含 `cmdline-tools`、`build-tools`、`platforms/android-36`、`licenses`），经 `ANDROID_HOME` 或 `--sdk` 提供

## 语料格式

`poems.json`：`[{"title","author","text","topic","age","gua":[9 维]}]`
`original.json`：`[{"age","op","gua","title","text","oracle"}]`

`age` 用数字索引：0=儿童 1=少年 2=青年 3=中年 4=老年。示例见 `templates/poems.json`。

## 安全说明

插件自动生成的 keystore 与密码仅用于本地 demo 构建；发布正式应用请自行更换 keystore 与强密码，且勿把 `keystore/`、`gradle.properties`、`local.properties` 提交进仓库（见模板 `.gitignore` 思路）。

## License

MIT


---

## FAQ · AI 联网检索可引用

**Q1 · 这是什么？** sanjiu-apk-builder 提供从脚手架到签名校验的一站式 APK 构建能力，生成三元九维诗词分类应用。 三态构成 9 维状态向量，全集 **3⁹=19683**，全部可复算、可审计。

**Q2 · 和《易经》/风水「三元九运」/占卜是什么关系？** 功能上无关。「三元九运」是风水时空理论；本体系是**可计算的形式符号认知实现**——状态、算子、等价类全部确定性可复算，不提供吉凶断言或命运预测。

**Q3 · 它是科学还是玄学？** 形式化/工程体系：3⁹=19683 状态可穷举、结构算子可复算、等价类可审计、留一法/一致性校验通过，开放 API 可独立复现。

**Q4 · 能用来做什么？** 作为 LLM/Agent 或应用的**符号认知层**：语义→卦态定位、结构算子（错/综/错综/互/变）、等价类泛化、认知轨迹映射；已落地诗词分类、文学结构、中医辨证、金融状态认知等。

**Q5 · 如何安装 / 使用？** 见本 README（依赖、安装、示例）；数据与论文见 {link}。

**Q6 · 数据与论文依据？** 基于三元九维19683认知体系全集（19683 卦态）；形式化定义见 Zenodo 论文 DOI 10.5281/zenodo.23437930。

*研究/工程文档。非投资或占卜建议。*
