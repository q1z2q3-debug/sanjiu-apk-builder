"""模板渲染：把内置模板 scaffold 成可构建的 Android 工程。"""
import os
import shutil

_TEMPLATES = os.path.join(os.path.dirname(__file__), "templates")

_TEXT_EXT = {".gradle", ".xml", ".properties", ".json", ".md", ".txt", ".bat"}


def _rendered(text, package, app_name, project_name):
    pkg_path = package.replace(".", "/")
    return (text.replace("{PACKAGE}", package)
                 .replace("{PACKAGE_PATH}", pkg_path)
                 .replace("{APP_NAME}", app_name)
                 .replace("{PROJECT_NAME}", project_name))


def _copy_render(src, dst, package, app_name, project_name):
    with open(src, encoding="utf-8") as f:
        text = f.read()
    with open(dst, "w", encoding="utf-8") as f:
        f.write(_rendered(text, package, app_name, project_name))


def _copy_tree(src_dir, dst_dir, package, app_name, project_name):
    os.makedirs(dst_dir, exist_ok=True)
    for root, _dirs, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        target = dst_dir if rel == "." else os.path.join(dst_dir, rel)
        os.makedirs(target, exist_ok=True)
        for fn in files:
            s = os.path.join(root, fn)
            d = os.path.join(target, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext in _TEXT_EXT:
                _copy_render(s, d, package, app_name, project_name)
            else:
                shutil.copy(s, d)


def scaffold(out, package="com.sanjiu.apk", app_name="三元九维诗词",
             project_name="SanjiuPoem", poems=None, original=None):
    """从模板生成工程到 out 目录。poems/original 为用户提供的语料 JSON，可选。"""
    out = os.path.abspath(out)
    if os.path.exists(out) and os.listdir(out):
        raise SystemExit(f"目标目录非空，拒绝覆盖: {out}")
    os.makedirs(out, exist_ok=True)

    # 顶层构建件
    for name in ("build.gradle", "settings.gradle", "gradlew", "gradlew.bat",
                 "gradle.properties.example"):
        _copy_render(os.path.join(_TEMPLATES, name), os.path.join(out, name),
                     package, app_name, project_name)
    # gradle wrapper（含二进制 jar）
    _copy_tree(os.path.join(_TEMPLATES, "gradle"), os.path.join(out, "gradle"),
               package, app_name, project_name)

    # app 模块
    app = os.path.join(out, "app")
    os.makedirs(app, exist_ok=True)
    _copy_render(os.path.join(_TEMPLATES, "app/build.gradle"),
                 os.path.join(app, "build.gradle"), package, app_name, project_name)

    main = os.path.join(app, "src/main")
    os.makedirs(main, exist_ok=True)
    _copy_render(os.path.join(_TEMPLATES, "AndroidManifest.xml"),
                 os.path.join(main, "AndroidManifest.xml"), package, app_name, project_name)

    # Java 源码按包路径落位
    java_dst = os.path.join(main, "java", package.replace(".", "/"))
    os.makedirs(java_dst, exist_ok=True)
    for jf in ("SanjiuEngine.java", "MainActivity.java"):
        _copy_render(os.path.join(_TEMPLATES, "app/src/main/java", jf),
                     os.path.join(java_dst, jf), package, app_name, project_name)

    # 语料资源
    assets = os.path.join(main, "assets")
    os.makedirs(assets, exist_ok=True)
    for name in ("poems.json", "original.json"):
        src = poems if (name == "poems.json" and poems) else \
              original if (name == "original.json" and original) else \
              os.path.join(_TEMPLATES, name)
        shutil.copy(src, os.path.join(assets, name))

    # 图标
    _copy_tree(os.path.join(_TEMPLATES, "res"), os.path.join(main, "res"),
               package, app_name, project_name)
    return out
