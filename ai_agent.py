import os
import time
import requests
from rich.console import Console
from typing import Dict, Any

console = Console()

class AIAgent:
    def __init__(self):
        # 直接使用os.getenv()获取环境变量
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("未设置DEEPSEEK_API_KEY环境变量")
            
        self.api_url = os.getenv('DEEPSEEK_API_URL', "https://api.deepseek.com/v1/chat/completions")
        self.model = os.getenv('DEEPSEEK_MODEL', "deepseek-chat")
        self.max_retries = int(os.getenv('DEEPSEEK_MAX_RETRIES', "3"))
        self.retry_delay = int(os.getenv('DEEPSEEK_RETRY_DELAY', "2"))  # 秒
        self.temperature = float(os.getenv('DEEPSEEK_TEMPERATURE', "0.7"))
        self.max_tokens = int(os.getenv('DEEPSEEK_MAX_TOKENS', "4000"))
        
    def exploit_vulnerability(self, environment: Dict[str, Any]) -> str:
        """
        使用AI Agent进行漏洞复现分析
        """
        for attempt in range(self.max_retries):
            try:
                # 构建提示词
                prompt = self._build_prompt(environment)
                
                # 调用DeepSeek API
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的网络安全专家，擅长漏洞复现。请提供可执行的命令和代码，我会自动执行这些命令。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                }
                
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                
                # 解析响应
                result = response.json()['choices'][0]['message']['content']
                console.print(f"\n[green]AI分析结果:[/green]\n{result}")
                
                return result
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    console.print(f"[yellow]API调用失败，{self.retry_delay}秒后重试... (尝试 {attempt + 1}/{self.max_retries})[/yellow]")
                    time.sleep(self.retry_delay)
                else:
                    console.print(f"[red]AI Agent执行失败: {str(e)}[/red]")
                    raise
            
    def _build_prompt(self, environment: Dict[str, Any]) -> str:
        """
        构建AI提示词
        """
        vuln_info = environment['vulnerability_info']
        cve_data = vuln_info.get('cve_data', {})
        
        # 获取漏洞的详细信息
        description = vuln_info['description']
        affected_versions = vuln_info['affected_versions']
        exploit_type = vuln_info['exploit_type']
        
        # 获取漏洞的CVSS评分（如果存在）
        cvss_score = None
        if 'metrics' in cve_data:
            for metric in cve_data['metrics'].values():
                if 'cvssData' in metric:
                    cvss_score = metric['cvssData']['baseScore']
                    break
        
        # 构建提示词
        prompt = f"""
        请帮我分析以下漏洞，并提供复现步骤：

        CVE编号：{vuln_info['cve_id']}
        漏洞描述：{description}
        受影响版本：{', '.join(affected_versions)}
        漏洞类型：{exploit_type}
        CVSS评分：{cvss_score if cvss_score else '未知'}
        
        环境说明：
        - 这是一个已经启动的Docker容器
        - 容器中已经安装了基本的工具（git, make, gcc等）
        - 容器以root权限运行
        - 工作目录在/app下
        
        请提供以下格式的命令：
        1. 环境准备命令（如克隆代码、编译等）
        2. 漏洞利用命令（具体的攻击命令）
        3. 验证命令（确认漏洞是否成功利用）
        
        请确保：
        - 所有命令都在容器内执行
        - 提供完整的命令，包括所有必要的参数
        - 每个命令单独一行
        - 使用$作为命令提示符
        - 提供清晰的命令说明
        
        例如：
        $ git clone https://github.com/example/exploit.git
        $ cd exploit
        $ make
        $ ./exploit
        
        请确保提供的命令是安全的，仅用于教育目的。
        """
        
        return prompt 
