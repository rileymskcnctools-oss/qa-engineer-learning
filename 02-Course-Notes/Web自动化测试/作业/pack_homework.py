#!/usr/bin/env python
"""把单个作业文件夹打成干净的压缩包，排除 .venv/.idea/.pytest_cache/__pycache__/*.pyc。

用法（在 作业/ 目录下）：
    python pack_homework.py homework03-selenium-basic

为什么不用 zip 命令：git-bash 下没有 zip/7z，Python 的 zipfile 跨平台可用。
接收方解压后 `uv sync` 即可复现环境。
"""
import os
import sys
import zipfile

EXCLUDE_DIRS = {".venv", ".idea", ".pytest_cache", "__pycache__", ".git"}


def pack(folder: str) -> str:
    folder = folder.rstrip("/\\")
    if not os.path.isdir(folder):
        raise SystemExit(f"目录不存在: {folder}")
    out = folder + ".zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(folder):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                full = os.path.join(dirpath, fn)
                z.write(full, full)
    size = os.path.getsize(out)
    print(f"已生成 {out}（{size} 字节，{size / 1024:.1f} KB）")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    pack(sys.argv[1])
