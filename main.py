import os
from vulnerability_manager import VulnerabilityManager
from ai_agent import AIAgent
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv

console = Console()

def main():
    # 加载环境变量
    load_dotenv()
    
    # 初始化组件
    vuln_manager = VulnerabilityManager()
    ai_agent = AIAgent()
    
    while True:
        console.print("\n[bold cyan]自动化漏洞复现系统[/bold cyan]")
        console.print("1. 输入CVE编号进行漏洞复现")
        console.print("2. 进入已启动的容器")
        console.print("3. 退出程序")
        
        choice = Prompt.ask("请选择操作", choices=["1", "2", "3"])
        
        if choice == "1":
            cve_id = Prompt.ask("请输入CVE编号")
            try:
                # 设置漏洞环境
                environment = vuln_manager.setup_environment(cve_id)
                
                # 使用AI代理进行漏洞复现
                ai_agent.exploit_vulnerability(environment)
                
            except Exception as e:
                console.print(f"[red]错误: {str(e)}[/red]")
                
        elif choice == "2":
            # 获取所有运行中的容器
            containers = vuln_manager.client.containers.list()
            if not containers:
                console.print("[yellow]没有运行中的容器[/yellow]")
                continue
                
            # 显示容器列表
            console.print("\n[bold]运行中的容器:[/bold]")
            for i, container in enumerate(containers, 1):
                # 获取容器详细信息
                container_info = vuln_manager.client.api.inspect_container(container.id)
                image_name = container_info['Config']['Image']
                # 直接使用容器名作为CVE编号
                console.print(f"{i}. [cyan]{container.name}[/cyan] (ID: {container.id[:12]}) - 镜像: {image_name}")
                
            # 选择容器
            try:
                choice = int(Prompt.ask("请选择要进入的容器编号", choices=[str(i) for i in range(1, len(containers)+1)]))
                selected_container = containers[choice-1]
                
                # 进入容器
                console.print(f"[yellow]正在进入容器 {selected_container.name}...[/yellow]")
                os.system(f"docker exec -it {selected_container.id} /bin/bash")
                
            except (ValueError, IndexError):
                console.print("[red]无效的选择[/red]")
                
        elif choice == "3":
            # 清理所有Docker环境
            vuln_manager.cleanup_all()
            console.print("[green]程序已退出[/green]")
            break

if __name__ == "__main__":
    main() 
