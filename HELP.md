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
│   └── sqlite-sample/        # 验证 DB-as-skill 模式
│       ├── SKILL.md
│       ├── scripts/
│       │   └── query.py
│       └── references/
│           └── schema.md
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

当前你的实际路径：
Nora/skills/html-ppt/examples/my-deck/index.html
                    ↑ 需要访问 assets/

相对路径 "../assets/" 指向：
Nora/skills/html-ppt/assets/  ✅ 正确！

相对路径 "../../assets/" 指向：
Nora/skills/assets/  ❌ 错误！