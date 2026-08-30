# Web 自动化测试 作业

每个视频/知识点对应的练习代码放这里。

## 目录结构

```
02-Course-Notes/Web自动化测试/作业/
├── homework01-selenium-basic/      # 第1次作业（环境验证、第一个脚本）
├── homework02-selenium-basic/      # 第2次作业
├── ... homework10-selenium-basic/  # 预建 10 个，用完再加
├── pack_homework.py                # 打包脚本（生成干净压缩包）
└── README.md
```

每个作业是**独立的 uv 项目**：各自的 `pyproject.toml` + `uv.lock` + `.venv`，互不依赖。

## 环境准备（逐作业 uv，Python 3.12）

每个作业在自己的目录里 `uv sync`，首次/换电脑都是同一条命令：

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\Web自动化测试\作业\homework03-selenium-basic"
uv sync                # 重建 .venv + uv.lock
uv run pytest -v       # 跑测试
```

`.venv/` 已被根 `.gitignore` 忽略，不进 Git、不进压缩包。uv 用全局缓存，多个作业的相同依赖只在磁盘存一份（硬链接），不会 10 倍膨胀。

新增依赖用 `uv add xxx`，不要手动 pip install。

## 打包提交（压缩包只装代码 + 依赖声明，约 9KB）

用 `pack_homework.py`（git-bash 下没有 zip/7z，用 Python 的 zipfile 跨平台可用），自动排除 `.venv/`、`.idea/`、`.pytest_cache/`、`__pycache__/`、`*.pyc`：

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\Web自动化测试\作业"
python pack_homework.py homework03-selenium-basic
```

接收方解压后 `uv sync` 即可复现环境。

## 注意

- Selenium 必须 4.x（自带 Selenium Manager，无需手动下 chromedriver）
- 首次运行需联网下载 driver，之后走缓存 `C:\Users\riley\.cache\selenium`
- 脚本收尾统一 `driver.quit()`，放在 fixture teardown 里，避免残留 chromedriver 进程
