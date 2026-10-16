# 贡献指南 · sanjiu-apk-builder

感谢你愿意参与贡献！请先阅读本指南，让协作顺畅高效。

## 项目定位

`sanjiu-apk-builder` 把"制作三元九维诗词分类 APK"的整套流程（脚手架、诗卦引擎、图文界面、图标、JDK/SDK 检测、签名、release 构建、APK 校验）沉淀为两条命令。**核心约定：数理公理（三元九爻：阳+1/中和0/阴−1，9 维）与算子映射固定，AI 与贡献者都不得擅自修改底层数理，只能在此基础上扩展创作、界面、数据与工程能力。**

## 目录结构

```
sanjiu_apk/
  render.py    模板渲染（templates → Android 工程）
  builder.py   JDK/SDK 检测、签名 keystore、Gradle 构建、APK 校验
  cli.py       argparse 命令入口（scaffold / build）
  templates/   可运行 Android 工程模板（Java/资源/gradle）
tests/         单元测试（如新增）
```

## 环境准备

- Python ≥ 3.8
- JDK 17（AGP 8.9 要求）
- Android SDK（cmdline-tools / build-tools 37.0.0 / platforms;android-36 / licenses）

```bash
pip install -e ".[dev]"
sanjiu-apk scaffold --out ./demo && sanjiu-apk build --dir ./demo
```

## 怎么贡献

1. **提 Issue 优先**：报告 bug、讨论功能、反馈文档，先开 issue 描述清楚（复现步骤 / 期望 / 实际）。
2. **提 PR**：
   - 从 `main` 切分支，命名如 `feat/xxx`、`fix/xxx`、`docs/xxx`
   - 改动聚焦单一主题，一次一个 PR
   - 新增功能须带对应自测（跑通 `scaffold` + `build` 产出签名 APK）
   - 更新 README（如 CLI/行为变化）
3. **风格**：Python 遵循 PEP 8；CLI 参数命名与现有一致；模板 Java 遵循现有 `SanjiuEngine`/`MainActivity` 的命名习惯。

## 验证

- 本地：`sanjiu-apk scaffold` + `build` 产出 `app-release.apk` 且 `apksigner verify` 通过
- CI：push 后 GitHub Actions 自动跑 `build-apk`，徽章转绿即通过
- 打包：`python -m build` 生成 sdist + wheel，`twine check dist/*` 无警告

## 安全红线

- **不提交**：签名 keystore、`gradle.properties` 真实密码、`local.properties`、`.env`、构建产物
- 修改数理公理 / 算子的 PR 将不被接受（见"项目定位"）

## 许可

本仓库为 MIT 协议，贡献即视为同意在 MIT 协议下授权你的改动。
