# 自动化漏洞复现系统

这是一个基于Kali Linux的自动化漏洞复现系统，可以自动搭建漏洞环境并使用AI Agent进行漏洞复现。

## 功能特点

- 自动搭建漏洞环境（基于Docker）
- 使用AI Agent进行漏洞复现分析
- 支持多种CVE漏洞
- 友好的命令行界面

## 系统要求

- Kali Linux
- Python 3.8+
- Docker
- OpenAI API密钥

## 安装步骤

1. 克隆仓库：
```bash
git clone [repository_url]
cd [repository_name]
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
创建 `.env` 文件并添加以下内容：
```
OPENAI_API_KEY=your_api_key_here
```

## 使用方法

1. 运行主程序：
```bash
python main.py
```

2. 输入CVE编号，系统将：
   - 自动搭建漏洞环境
   - 使用AI Agent分析漏洞
   - 提供详细的复现步骤

## 注意事项

- 本系统仅用于教育和研究目的
- 请确保在受控环境中使用
- 遵守相关法律法规

## 目录结构

```
.
├── main.py              # 主程序入口
├── vulnerability_manager.py  # 漏洞环境管理
├── ai_agent.py          # AI Agent模块
├── requirements.txt     # 依赖包列表
├── environments/        # 漏洞环境配置
└── README.md           # 说明文档
```

## 贡献指南

欢迎提交Issue和Pull Request来改进系统。

## 许可证

MIT License 