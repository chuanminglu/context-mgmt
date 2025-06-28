#!/usr/bin/env python3
"""
AI上下文自动化刷新守护进程
支持定时检查和自动刷新

使用方法:
python auto-refresh-daemon.py --start    # 启动守护进程
python auto-refresh-daemon.py --stop     # 停止守护进程
python auto-refresh-daemon.py --status   # 查看状态
"""

import os
import sys
import time
import json
import signal
import threading
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

# 定义常量
SMART_REFRESH_SCRIPT = "smart-refresh.py"

class SimpleScheduler:
    """简单的定时任务调度器"""
    def __init__(self):
        self.jobs = []
    
    def add_daily_job(self, hour, minute, func):
        """添加每日任务"""
        self.jobs.append({
            'type': 'daily',
            'hour': hour,
            'minute': minute,
            'func': func,
            'last_run': None
        })
    
    def add_weekly_job(self, weekday, hour, minute, func):
        """添加每周任务 (weekday: 0=Monday, 6=Sunday)"""
        self.jobs.append({
            'type': 'weekly',
            'weekday': weekday,
            'hour': hour,
            'minute': minute,
            'func': func,
            'last_run': None
        })
    
    def add_hourly_job(self, hour, func):
        """添加特定小时的任务"""
        self.jobs.append({
            'type': 'hourly',
            'hour': hour,
            'func': func,
            'last_run': None
        })
    
    def check_and_run(self):
        """检查并运行到期的任务"""
        now = datetime.now()
        
        for job in self.jobs:
            should_run = False
            
            if job['type'] == 'daily':
                if (now.hour == job['hour'] and 
                    now.minute == job['minute'] and
                    (job['last_run'] is None or 
                     job['last_run'].date() < now.date())):
                    should_run = True
            
            elif job['type'] == 'weekly':
                if (now.weekday() == job['weekday'] and
                    now.hour == job['hour'] and
                    now.minute == job['minute'] and
                    (job['last_run'] is None or 
                     now - job['last_run'] > timedelta(days=6))):
                    should_run = True
            
            elif job['type'] == 'hourly':
                if (now.hour == job['hour'] and
                    now.minute == 0 and
                    (job['last_run'] is None or 
                     now - job['last_run'] > timedelta(hours=1))):
                    should_run = True
            
            if should_run:
                try:
                    job['func']()
                    job['last_run'] = now
                except Exception as e:
                    print(f"执行任务时出错: {e}")

class AutoRefreshDaemon:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.ai_context_dir = self.project_root / ".ai-context"
        self.pid_file = self.ai_context_dir / "cache" / "daemon.pid"
        self.log_file = self.ai_context_dir / "logs" / "auto-refresh.log"
        self.running = False
        self.scheduler = SimpleScheduler()
        
        # 确保目录存在
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        # 写入文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # 同时输出到控制台
        print(f"{timestamp} [{level}] {message}")
    
    def start_daemon(self):
        """启动守护进程"""
        if self.is_running():
            self.log("守护进程已在运行", "WARNING")
            return False
        
        # 写入PID文件
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        self.log("AI上下文自动刷新守护进程启动")
        self.running = True
        
        # 设置定时任务
        self.setup_schedule()
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # 主循环
        try:
            while self.running:
                self.scheduler.check_and_run()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            self.stop_daemon()
    
    def setup_schedule(self):
        """设置定时任务"""
        # 每天早上9点检查
        self.scheduler.add_daily_job(9, 0, self.daily_check)
        
        # 每周一早上进行深度检查
        self.scheduler.add_weekly_job(0, 9, 30, self.weekly_deep_check)
        
        # 每小时检查代码变更（工作时间）
        for hour in range(9, 18):  # 9AM to 6PM
            self.scheduler.add_hourly_job(hour, self.hourly_change_check)
        
        self.log("定时任务已设置")
    
    def daily_check(self):
        """每日检查"""
        self.log("执行每日上下文检查")
        
        try:
            result = subprocess.run([
                sys.executable, 
                str(self.ai_context_dir / "tools" / SMART_REFRESH_SCRIPT),
                "--auto"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log("每日检查完成")
            else:
                self.log(f"每日检查失败: {result.stderr}", "ERROR")
                
        except Exception as e:
            self.log(f"每日检查异常: {e}", "ERROR")
    
    def weekly_deep_check(self):
        """每周深度检查"""
        self.log("执行每周深度检查")
        
        try:
            # 生成详细报告
            result = subprocess.run([
                sys.executable,
                str(self.ai_context_dir / "tools" / SMART_REFRESH_SCRIPT),
                "--report"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                # 保存报告
                report_file = self.ai_context_dir / "reports" / f"weekly-report-{datetime.now().strftime('%Y%m%d')}.txt"
                report_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                
                self.log(f"每周报告已保存: {report_file}")
                
                # 如果需要刷新，执行刷新
                if "需要刷新" in result.stdout:
                    self.log("根据周报告建议执行刷新")
                    subprocess.run([
                        sys.executable,
                        str(self.ai_context_dir / "tools" / SMART_REFRESH_SCRIPT),
                        "--auto"
                    ], cwd=self.project_root)
            else:
                self.log(f"每周检查失败: {result.stderr}", "ERROR")
                
        except Exception as e:
            self.log(f"每周检查异常: {e}", "ERROR")
    
    def hourly_change_check(self):
        """每小时变更检查"""
        # 只在工作日执行
        if datetime.now().weekday() >= 5:  # 周末不执行
            return
        
        try:
            # 检查Git是否有新的提交
            result = subprocess.run([
                "git", "log", "--oneline", "-n", "1", "--since='1 hour ago'"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0 and result.stdout.strip():
                self.log("检测到新提交，执行变更检查")
                
                # 执行智能检查
                check_result = subprocess.run([
                    sys.executable,
                    str(self.ai_context_dir / "tools" / SMART_REFRESH_SCRIPT),
                    "--check"
                ], capture_output=True, text=True, cwd=self.project_root)
                
                if "需要刷新" in check_result.stdout:
                    self.log("检测到需要刷新，执行自动刷新")
                    subprocess.run([
                        sys.executable,
                        str(self.ai_context_dir / "tools" / SMART_REFRESH_SCRIPT),
                        "--auto"
                    ], cwd=self.project_root)
                    
        except Exception as e:
            self.log(f"变更检查异常: {e}", "ERROR")
    
    def stop_daemon(self):
        """停止守护进程"""
        self.running = False
        
        # 删除PID文件
        if self.pid_file.exists():
            self.pid_file.unlink()
        
        self.log("AI上下文自动刷新守护进程已停止")
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        self.log(f"收到信号 {signum}，正在停止守护进程")
        self.stop_daemon()
        sys.exit(0)
    
    def is_running(self) -> bool:
        """检查守护进程是否运行"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # 检查进程是否存在
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            # 进程不存在，删除过期的PID文件
            self.pid_file.unlink()
            return False
    
    def get_status(self) -> dict:
        """获取守护进程状态"""
        status = {
            "running": self.is_running(),
            "pid_file": str(self.pid_file),
            "log_file": str(self.log_file)
        }
        
        if status["running"]:
            with open(self.pid_file, 'r') as f:
                status["pid"] = int(f.read().strip())
        
        # 获取最近的日志
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                status["recent_logs"] = lines[-10:]  # 最近10条日志
        
        return status

def create_parser():
    """创建命令行参数解析器"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI上下文自动刷新守护进程")
    parser.add_argument("--start", action="store_true", help="启动守护进程")
    parser.add_argument("--stop", action="store_true", help="停止守护进程")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--project", default=".", help="项目路径")
    
    return parser

def handle_start(daemon):
    """处理启动命令"""
    if daemon.is_running():
        print("❌ 守护进程已在运行")
        sys.exit(1)
    else:
        print("🚀 启动AI上下文自动刷新守护进程...")
        daemon.start_daemon()

def handle_stop(daemon):
    """处理停止命令"""
    if not daemon.is_running():
        print("❌ 守护进程未运行")
        sys.exit(1)
    else:
        # 发送停止信号
        with open(daemon.pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        os.kill(pid, signal.SIGTERM)
        print("✅ 守护进程停止信号已发送")

def handle_status(daemon):
    """处理状态查询命令"""
    status = daemon.get_status()
    print("\n" + "="*50)
    print("🔍 AI上下文自动刷新守护进程状态")
    print("="*50)
    
    if status["running"]:
        print(f"✅ 状态: 运行中 (PID: {status.get('pid', 'Unknown')})")
    else:
        print("❌ 状态: 未运行")
    
    print(f"📁 PID文件: {status['pid_file']}")
    print(f"📄 日志文件: {status['log_file']}")
    
    if "recent_logs" in status:
        print("\n📝 最近日志:")
        for log_line in status["recent_logs"]:
            print(f"  {log_line.strip()}")

def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    daemon = AutoRefreshDaemon(args.project)
    
    if args.start:
        handle_start(daemon)
    elif args.stop:
        handle_stop(daemon)
    elif args.status:
        handle_status(daemon)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
