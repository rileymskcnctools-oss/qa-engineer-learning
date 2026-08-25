# Web 自动化测试 作业

每个视频/知识点对应的练习代码放这里。

## 目录结构

```
02-Course-Notes/Web自动化测试/作业/
├── pyproject.toml                  # 依赖声明（selenium + pytest），uv sync 恢复
├── homework01-selenium-basic/      # 第1次作业（环境验证、第一个脚本）
├── homework02-selenium-basic/      # 第2次作业
└── ... homework15-selenium-basic/
```

## 环境准备（uv，Python 3.12）

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\Web自动化测试\作业"
uv sync                       # 首次/换电脑恢复环境
uv run pytest homework01-selenium-basic -v
```

新增依赖用 `uv add xxx`，不要手动 pip install。

## 打包提交

```bash
cd "C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\Web自动化测试\作业"
zip -r homework01-selenium-basic.zip homework01-selenium-basic/
```

## 注意

- Selenium 必须 4.x（自带 Selenium Manager，无需手动下 chromedriver）
- 首次运行需联网下载 driver，之后走缓存 `C:\Users\riley\.cache\selenium`
- 脚本收尾统一 `driver.quit()`，放在 fixture teardown 里，避免残留 chromedriver 进程
