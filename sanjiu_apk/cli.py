"""sanjiu-apk-builder 命令行入口。"""
import argparse
import sys

from . import __version__
from .render import scaffold
from .builder import build


def _cmd_scaffold(args):
    out = scaffold(args.out, args.package, args.name, args.project,
                   args.poems, args.original, args.icon)
    print(f"已生成工程: {out}")
    print(f"  包名={args.package}  应用名={args.name}"
          + (f"  图标={args.icon}" if args.icon else "  图标=默认九爻卦画"))
    print("下一步: sanjiu-apk build --dir <out> --jdk <JDK17> --sdk <ANDROID_SDK>")


def _cmd_build(args):
    apk = build(args.dir, args.jdk, args.sdk)
    print("构建完成 ✅", apk)


def main(argv=None):
    p = argparse.ArgumentParser(prog="sanjiu-apk",
                                description="一键生成三元九维诗词分类 APK 的开源脚手架 + 构建器")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scaffold", help="从模板生成 Android 工程")
    s.add_argument("--out", required=True, help="工程输出目录")
    s.add_argument("--package", default="com.sanjiu.apk", help="包名（默认 com.sanjiu.apk）")
    s.add_argument("--name", default="三元九维诗词", help="应用名（默认 三元九维诗词）")
    s.add_argument("--project", default="SanjiuPoem", help="工程名（默认 SanjiuPoem）")
    s.add_argument("--poems", default=None, help="经典语料 poems.json 路径（可选）")
    s.add_argument("--original", default=None, help="三元原创 original.json 路径（可选）")
    s.add_argument("--icon", default=None, help="自定义 App 图标图片路径（可选，自动生成 5 密度 mipmap）")
    s.set_defaults(func=_cmd_scaffold)

    b = sub.add_parser("build", help="检测 JDK/SDK、生成签名并构建 APK")
    b.add_argument("--dir", required=True, help="工程目录")
    b.add_argument("--jdk", default=None, help="JDK17 路径（默认取 JAVA_HOME）")
    b.add_argument("--sdk", default=None, help="Android SDK 路径（默认取 ANDROID_HOME）")
    b.set_defaults(func=_cmd_build)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
