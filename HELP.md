## Nora智能体目录结构

```text
Nora/
├── core/
│   ├── __init__.py
│   ├── agent.py              # Agent 主循环
│   ├── llm.py                # LLM 抽象(Kimi/Qwen/DeepSeek)
│   ├── skills.py             # Skill 扫描 + 加载
│   └── tools.py              # 工具注册表
│
├── tools_builtin/
│   ├── __init__.py
│   ├── file_ops.py           # read, write
│   ├── shell.py              # bash
│   └── skill_ops.py          # activate_skill
│
├── skills/                   # ⭐ 可插拔 skills 目录
│   ├── hello-world/          # 验证 skill 机制
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── hello.py
│   ├── sqlite-sample/        # 验证 DB-as-skill 模式
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── query.py
│   │   └── references/
│   │       └── schema.md
│   ├── markitdown/        # 主流格式转md
│       ├── SKILL.md
│       ├── scripts/
│       │   └── convert.py              # 主转换脚本
│       │   └── batch_convert.py        # 批量转换脚本
│       │   └── __init__.py             # Python 包标识
│       └── references/
│           └── formats.md              # 支持格式参考文档
│
├── adapters/
│   ├── __init__.py
│   ├── cli.py                # 命令行入口
│   └── server.py             # FastAPI(WebUI + 预留 ClawBot HTTP)
│
├── webui/
│   └── index.html            # 单文件 UI
│
├── uploads/                  # 运行时上传文件目录(.gitignore 掉内容)
├── logs/                     # 日志目录(.gitignore 掉内容)
├── data/
│   └── sample.db             # 示例 SQLite
│
├── .env.example              # 密钥模板
├── .gitignore
├── config.yaml               # 主配置
├── requirements.txt
├── README.md                 # 用户文档
└── main.py                   # 统一入口:python main.py cli/webui
```



现在已经可以正常使用markitdown，并安装了markitdown-ocr。我需要把它包装成一个skill，在我的智能体里调用。这个skill需要遵守 [agentskills.io](https://agentskills.io) 开放标准。并且放在Nora/skills/markitdown文件夹下。我的系统已经安装了markitdown，并且加入了path。你帮我写skill.md 和/script文件夹下必要的文档。并且发给我下载。Nora目录结构如下：