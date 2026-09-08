# APP 自动化测试 作业

每个视频/知识点对应的练习代码放这里。

## 目录结构

```
02-Course-Notes/APP自动化测试/作业/
├── homework01-appium-basic/      # 第1次作业（环境验证、第一个脚本）
├── homework02-appium-basic/      # 第2次作业
├── ... homework07-appium-basic/  # 预建 7 个，用完再加
├── pack_homework.py              # 打包脚本（生成干净压缩包）
└── README.md
```

每个作业是**独立的 uv 项目**：各自的 `pyproject.toml` + `uv.lock` + `.venv`，互不依赖。

## 环境准备（逐作业 uv，Python 3.12）

每个作业在自己的目录里 `uv sync`，首次/换电脑都是同一条命令：

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\APP自动化测试\作业\homework01-appium-basic"
uv sync                # 重建 .venv + uv.lock
uv run pytest -v       # 跑测试
```

`.venv/` 已被根 `.gitignore` 忽略，不进 Git、不进压缩包。uv 用全局缓存，多个作业的相同依赖只在磁盘存一份（硬链接），不会 7 倍膨胀。

新增依赖用 `uv add xxx`，不要手动 pip install。

依赖说明：
- `Appium-Python-Client`：Appium 官方 Python 客户端（`from appium import webdriver`、`from appium.options.android import UiAutomator2Options`、`from appium.webdriver.common.appiumby import AppiumBy`）
- `selenium`：Appium 客户端底层依赖，`WebDriverWait` / `expected_conditions` 从它导入（单独声明，方便直接 import）
- `pytest`：用例框架（setup_class / teardown_class / 断言）

## 打包提交（压缩包只装代码 + 依赖声明）

用 `pack_homework.py`（git-bash 下没有 zip/7z，用 Python 的 zipfile 跨平台可用），自动排除 `.venv/`、`.idea/`、`.pytest_cache/`、`__pycache__/`、`*.pyc`：

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\APP自动化测试\作业"
python pack_homework.py homework01-appium-basic
```

接收方解压后 `uv sync` 即可复现环境。

**一键打包全部作业**：双击本目录的 `pack_all.bat`，会自动打包所有 `homeworkNN-appium-basic` 文件夹（自动跳过 `.venv`），每个产物约 9KB。

## 注意

- 跑 Appium 用例前先启动 Appium Server（命令行 `appium`）和模拟器/真机（`adb devices` 能看到设备）
- `appPackage` / `appActivity` / `noReset` 等 capability 需加 `appium:` 前缀（Appium 2.x 要求）
- 脚本收尾统一 `driver.quit()`，放 fixture teardown 里，避免 session 残留占用设备
