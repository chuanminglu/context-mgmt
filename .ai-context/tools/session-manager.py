#!/usr/bin/env python3
"""
工作会话管理器
记录和管理开发工作会话，提供修改文件的上下文信息
"""
import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

class SessionManager:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.ai_context_dir = self.project_root / ".ai-context"
        self.sessions_dir = self.ai_context_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
    def start_session(self, title, description="", tags=None):
        """开始新的工作会话"""
        if tags is None:
            tags = []
        
        # 检查是否有活跃会话
        active_session = self.get_active_session()
        if active_session:
            print(f"⚠️  警告: 已有活跃会话 '{active_session['title']}'")
            response = input("是否结束当前会话并开始新会话? (y/N): ")
            if response.lower() == 'y':
                self.end_session()
            else:
                print("❌ 取消开始新会话")
                return None
        
        session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        session_data = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "title": title,
            "description": description,
            "status": "active",
            "files_modified": [],
            "git_commits": [],
            "tags": tags,
            "updates": []
        }
        
        session_file = self.sessions_dir / f"{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 开始新会话: {title}")
        print(f"📋 会话ID: {session_id}")
        if description:
            print(f"📝 描述: {description}")
        
        # 自动生成上下文
        self._auto_generate_context()
        
        return session_data
    
    def update_session(self, update_text):
        """更新当前活跃会话的进展"""
        active_session = self.get_active_session()
        if not active_session:
            print("❌ 没有活跃的会话")
            return False
        
        update_entry = {
            "time": datetime.now().isoformat(),
            "text": update_text
        }
        
        active_session["updates"].append(update_entry)
        
        session_file = self.sessions_dir / f"{active_session['session_id']}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(active_session, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 会话更新已记录: {update_text}")
        return True
    
    def end_session(self):
        """结束当前活跃会话"""
        active_session = self.get_active_session()
        if not active_session:
            print("❌ 没有活跃的会话")
            return False
        
        active_session["end_time"] = datetime.now().isoformat()
        active_session["status"] = "completed"
        
        session_file = self.sessions_dir / f"{active_session['session_id']}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(active_session, f, indent=2, ensure_ascii=False)
        
        duration = self._calculate_duration(active_session["start_time"], active_session["end_time"])
        print(f"✅ 会话已结束: {active_session['title']}")
        print(f"⏱️  持续时间: {duration}")
        
        # 自动生成上下文
        self._auto_generate_context()
        
        return True
    
    def get_active_session(self):
        """获取当前活跃的会话"""
        for session_file in self.sessions_dir.glob("session-*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                    if session.get("status") == "active":
                        return session
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        return None
    
    def list_sessions(self, limit=10):
        """列出最近的会话"""
        sessions = []
        for session_file in self.sessions_dir.glob("session-*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                    sessions.append(session)
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        
        # 按开始时间排序
        sessions.sort(key=lambda x: x["start_time"], reverse=True)
        
        print("📋 最近的工作会话:")
        for i, session in enumerate(sessions[:limit]):
            status_icon = "🟢" if session["status"] == "active" else "✅"
            start_time = datetime.fromisoformat(session["start_time"]).strftime("%m-%d %H:%M")
            
            if session["end_time"]:
                duration = self._calculate_duration(session["start_time"], session["end_time"])
                print(f"{status_icon} {session['title']} ({start_time}, {duration})")
            else:
                print(f"{status_icon} {session['title']} ({start_time}, 进行中)")
            
            if session.get("description"):
                print(f"    📝 {session['description']}")
            
            if session.get("tags"):
                tags_str = " ".join([f"#{tag}" for tag in session["tags"]])
                print(f"    🏷️  {tags_str}")
            
            print()
        
        if not sessions:
            print("暂无会话记录")
    
    def get_recent_sessions(self, days=7):
        """获取最近几天的会话，用于上下文生成"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)
        sessions = []
        
        for session_file in self.sessions_dir.glob("session-*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                    start_timestamp = datetime.fromisoformat(session["start_time"]).timestamp()
                    if start_timestamp > cutoff_time:
                        sessions.append(session)
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        
        return sorted(sessions, key=lambda x: x["start_time"], reverse=True)
    
    def _calculate_duration(self, start_time, end_time):
        """计算会话持续时间"""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = end - start
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _auto_generate_context(self):
        """自动生成上下文"""
        try:
            context_generator_path = self.ai_context_dir / "tools" / "context-generator.py"
            if not context_generator_path.exists():
                print("⚠️  警告: 找不到context-generator.py，跳过自动生成上下文")
                return False
            
            print("🔄 自动生成最新上下文...")
            
            # 执行上下文生成
            result = subprocess.run([
                sys.executable, 
                str(context_generator_path)
            ], 
            cwd=str(self.project_root),
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'  # 忽略编码错误
            )
            
            if result.returncode == 0:
                print("✅ 上下文生成完成")
                return True
            else:
                print(f"⚠️  上下文生成警告: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"⚠️  自动生成上下文时出错: {e}")
            return False

    def start_session_interactive(self):
        """交互式开始会话"""
        print("🚀 开始新的工作会话")
        print("━━━━━━━━━━━━━━━━━━━━")
        
        # 检查是否有活跃会话
        active_session = self.get_active_session()
        if active_session:
            print(f"⚠️  当前有活跃会话: '{active_session['title']}'")
            print(f"📅 开始时间: {datetime.fromisoformat(active_session['start_time']).strftime('%Y-%m-%d %H:%M')}")
            print()
            response = input("❓ 是否结束当前会话并开始新会话? (y/N): ").strip().lower()
            if response == 'y':
                self.end_session()
                print()
            else:
                print("❌ 取消开始新会话")
                return None
        
        # 获取会话标题
        while True:
            title = input("📋 请输入会话标题 (例如：用户认证模块开发): ").strip()
            if title:
                break
            print("⚠️  会话标题不能为空，请重新输入")
        
        # 获取会话描述（可选）
        print("📝 请输入详细描述 (可选，直接回车跳过):")
        description = input("   ").strip()
        
        # 获取标签（可选）
        print("🏷️  请输入标签，用空格分隔 (可选，直接回车跳过):")
        tags_input = input("   ").strip()
        tags = tags_input.split() if tags_input else []
        
        # 开始会话
        return self.start_session(title, description, tags)
    
    def end_session_interactive(self):
        """交互式结束会话"""
        print("🔚 结束工作会话")
        print("━━━━━━━━━━━━━━")
        
        active_session = self.get_active_session()
        if not active_session:
            print("❌ 当前没有活跃的会话")
            return False
        
        print(f"📋 当前会话: {active_session['title']}")
        start_time = datetime.fromisoformat(active_session['start_time']).strftime("%Y-%m-%d %H:%M")
        print(f"⏰ 开始时间: {start_time}")
        
        if active_session.get('description'):
            print(f"📝 描述: {active_session['description']}")
        
        print()
        confirm = input("❓ 确认结束此会话? (Y/n): ").strip().lower()
        if confirm in ['', 'y', 'yes']:
            return self.end_session()
        else:
            print("❌ 取消结束会话")
            return False
    
    def update_session_interactive(self):
        """交互式更新会话"""
        print("📝 更新会话进展")
        print("━━━━━━━━━━━━━━")
        
        active_session = self.get_active_session()
        if not active_session:
            print("❌ 当前没有活跃的会话")
            return False
        
        print(f"📋 当前会话: {active_session['title']}")
        print()
        
        while True:
            update_text = input("📄 请输入进展描述: ").strip()
            if update_text:
                break
            print("⚠️  进展描述不能为空，请重新输入")
        
        return self.update_session(update_text)

def main():
    parser = argparse.ArgumentParser(description="工作会话管理器")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 开始会话
    start_parser = subparsers.add_parser("start", help="开始新的工作会话")
    start_parser.add_argument("title", nargs='?', help="会话标题")
    start_parser.add_argument("-d", "--description", help="会话描述")
    start_parser.add_argument("-t", "--tags", nargs="*", help="会话标签")
    start_parser.add_argument("-i", "--interactive", action="store_true", help="交互式输入")
    
    # 更新会话
    update_parser = subparsers.add_parser("update", help="更新当前会话进展")
    update_parser.add_argument("text", nargs='?', help="进展描述")
    update_parser.add_argument("-i", "--interactive", action="store_true", help="交互式输入")
    
    # 结束会话
    end_parser = subparsers.add_parser("end", help="结束当前会话")
    end_parser.add_argument("-i", "--interactive", action="store_true", help="交互式确认")
    
    # 列出会话
    list_parser = subparsers.add_parser("list", help="列出最近的会话")
    list_parser.add_argument("-n", "--limit", type=int, default=10, help="显示数量限制")
    
    # 查看状态
    subparsers.add_parser("status", help="查看当前会话状态")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = SessionManager()
    
    if args.command == "start":
        # 交互式模式或缺少标题时使用交互式
        if args.interactive or not args.title:
            manager.start_session_interactive()
        else:
            manager.start_session(args.title, args.description or "", args.tags or [])
    elif args.command == "update":
        # 交互式模式或缺少文本时使用交互式
        if args.interactive or not args.text:
            manager.update_session_interactive()
        else:
            manager.update_session(args.text)
    elif args.command == "end":
        # 交互式模式时使用交互式确认
        if args.interactive:
            manager.end_session_interactive()
        else:
            manager.end_session()
    elif args.command == "list":
        manager.list_sessions(args.limit)
    elif args.command == "status":
        active = manager.get_active_session()
        if active:
            print(f"🟢 活跃会话: {active['title']}")
            start_time = datetime.fromisoformat(active['start_time']).strftime("%Y-%m-%d %H:%M")
            print(f"⏰ 开始时间: {start_time}")
            if active.get('description'):
                print(f"📝 描述: {active['description']}")
        else:
            print("⚪ 当前没有活跃会话")

if __name__ == "__main__":
    main()
