# APP 自动化测试 作业

每个视频/知识点对应的练习代码放这里。

## 目录结构

```
02-Course-Notes/APP自动化测试/作业/
├── pyproject.toml               # 共享依赖声明（pytest + Appium + selenium）
├── .python-version              # 锁 Python 3.12
├── .venv/                       # 共享虚拟环境（所有作业共用这一个）
├── homework01-appium-basic/     # 第1次作业（环境验证、第一个脚本）
│   ├── pyproject.toml           # 本作业依赖声明（打包交付用）
│   ├── .python-version          # 锁 3.12（打包交付用）
│   └── 异常.py                  # 代码
├── homework02-appium-basic/     # 第2次作业
├── ... homework07-appium-basic/ # 预建 7 个，用完再加
├── pack_homework.py             # 打包脚本（生成干净压缩包）
├── pack_all.bat                 # 一键打包全部作业
└── README.md
```

**共享环境**：所有作业共用一个 `.venv`（在 作业/ 根目录），代码仍在各自目录、互不干扰。每个作业目录里保留自己的 `pyproject.toml` + `.python-version` 只是为了打包交付时接收方能 `uv sync` 复现依赖，平时运行用不到它。

## 环境准备（共享 venv，Python 3.12）

首次或换电脑，只在 作业/ 根目录执行一次：

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\APP自动化测试\作业"
uv sync                # 生成共享 .venv
```

`.venv/` 已被根 `.gitignore` 忽略，不进 Git、不进压缩包。

## 运行作业

用共享 .venv 跑任意作业，无需在每个作业目录单独 sync：

```bash
# 在 作业/ 根目录执行
.venv/Scripts/python -m pytest homework01-appium-basic -v
```

PyCharm 里把解释器指向（7 个作业都用它，配一次即可）：

```
C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\APP自动化测试\作业\.venv\Scripts\python.exe
```

**注意**：不要在某个 `homeworkNN/` 目录里再 `uv sync`，那会又建出一个独立 .venv。统一用根目录的共享环境。

依赖说明：
- `Appium-Python-Client`：Appium 官方 Python 客户端（`from appium import webdriver`、`from appium.options.android import UiAutomator2Options`、`from appium.webdriver.common.appiumby import AppiumBy`）
- `selenium`：Appium 客户端底层依赖，`WebDriverWait` / `expected_conditions` 从它导入（单独声明，方便直接 import）
- `pytest`：用例框架（setup_class / teardown_class / 断言）

新增依赖：在 作业/ 根目录执行 `uv add xxx`（写进根目录 pyproject.toml），不要在单个作业目录单独加。

## 打包提交（压缩包只装代码 + 依赖声明）

用 `pack_homework.py`（git-bash 下没有 zip/7z，用 Python 的 zipfile 跨平台可用），自动排除 `.venv/`、`.idea/`、`.pytest_cache/`、`__pycache__/`、`*.pyc`：

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\APP自动化测试\作业"
python pack_homework.py homework01-appium-basic
```

压缩包内含该作业的 `pyproject.toml` + `.python-version`（依赖声明），接收方解压后 `uv sync` 即可复现环境。

**一键打包全部作业**：双击本目录的 `pack_all.bat`，会自动打包所有 `homeworkNN-appium-basic` 文件夹（自动跳过 `.venv`）。

## 注意

- 跑 Appium 用例前先启动 Appium Server（命令行 `appium`）和模拟器/真机（`adb devices` 能看到设备）
- `appPackage` / `appActivity` / `noReset` 等 capability 需加 `appium:` 前缀（Appium 2.x 要求）
- 脚本收尾统一 `driver.quit()`，放 fixture teardown 里，避免 session 残留占用设备
