#!/usr/bin/env python3
"""
智能上下文刷新工具
自动检测项目变化，智能决定何时刷新AI上下文

使用方法:
python smart-refresh.py --check        # 检查是否需要刷新
python smart-refresh.py --auto         # 自动刷新（如果需要）
python smart-refresh.py --force        # 强制刷新
"""

import os
import sys
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class SmartContextRefresher:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.ai_context_dir = self.project_root / ".ai-context"
        self.cache_dir = self.ai_context_dir / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置文件
        self.config = self._load_config()
        self.last_refresh_file = self.cache_dir / "last_refresh.json"
        self.change_tracking_file = self.cache_dir / "change_tracking.json"
    
    def _load_config(self) -> Dict:
        """加载刷新配置"""
        config_file = self.ai_context_dir / "config" / "refresh-config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "thresholds": {
                "max_days_without_refresh": 7,
                "max_code_changes": 500,
                "max_new_files": 10,
                "max_config_changes": 3,
                "max_dependency_changes": 3
            },
            "patterns": {
                "critical_files": [
                    "package.json", "requirements.txt", "Cargo.toml",
                    "docker-compose.yml", "Dockerfile",
                    "*.config.js", "*.config.ts", "*.config.py"
                ],
                "architecture_files": [
                    "README.md", "ARCHITECTURE.md", "docs/",
                    "migrations/", "schemas/"
                ],
                "exclude_patterns": [
                    "node_modules/", "__pycache__/", ".git/",
                    "*.log", "*.tmp", ".env*"
                ]
            },
            "refresh_triggers": {
                "team_changes": True,
                "architecture_changes": True,
                "dependency_changes": True,
                "significant_code_changes": True,
                "time_based": True
            }
        }
    
    def check_refresh_needed(self) -> Tuple[bool, List[str]]:
        """检查是否需要刷新上下文"""
        reasons = []
        
        # 1. 检查时间间隔
        if self._check_time_threshold():
            reasons.append("⏰ 距离上次刷新时间过长")
        
        # 2. 检查代码变更
        code_changes = self._analyze_code_changes()
        if code_changes["needs_refresh"]:
            reasons.extend(code_changes["reasons"])
        
        # 3. 检查配置文件变更
        config_changes = self._check_config_changes()
        if config_changes:
            reasons.append(f"⚙️ 关键配置文件变更: {', '.join(config_changes)}")
        
        # 4. 检查依赖变更
        dependency_changes = self._check_dependency_changes()
        if dependency_changes:
            reasons.append(f"📦 依赖包变更: {', '.join(dependency_changes)}")
        
        # 5. 检查团队变更
        team_changes = self._check_team_changes()
        if team_changes:
            reasons.append(f"👥 团队配置变更: {team_changes}")
        
        return len(reasons) > 0, reasons
    
    def _check_time_threshold(self) -> bool:
        """检查时间阈值"""
        if not self.last_refresh_file.exists():
            return True
        
        try:
            with open(self.last_refresh_file, 'r') as f:
                last_refresh_data = json.load(f)
            
            last_refresh = datetime.fromisoformat(last_refresh_data["timestamp"])
            threshold_days = self.config["thresholds"]["max_days_without_refresh"]
            
            return datetime.now() - last_refresh > timedelta(days=threshold_days)
        except:
            return True
    
    def _analyze_code_changes(self) -> Dict:
        """分析代码变更情况"""
        try:
            # 获取Git变更统计
            result = subprocess.run([
                "git", "diff", "--stat", "HEAD~10..HEAD"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                return {"needs_refresh": False, "reasons": []}
            
            lines = result.stdout.strip().split('\n')
            if not lines or lines == ['']:
                return {"needs_refresh": False, "reasons": []}
            
            # 解析变更统计
            total_files = 0
            total_insertions = 0
            total_deletions = 0
            new_files = 0
            
            for line in lines[:-1]:  # 最后一行是总计
                if 'file changed' in line or 'files changed' in line:
                    continue
                
                parts = line.split('|')
                if len(parts) >= 2:
                    total_files += 1
                    if 'new file' in line:
                        new_files += 1
                    
                    # 统计插入和删除行数
                    stats = parts[1].strip()
                    if '+' in stats:
                        total_insertions += stats.count('+')
                    if '-' in stats:
                        total_deletions += stats.count('-')
            
            # 检查阈值
            reasons = []
            thresholds = self.config["thresholds"]
            
            total_changes = total_insertions + total_deletions
            if total_changes > thresholds["max_code_changes"]:
                reasons.append(f"📝 代码变更过多: {total_changes}行")
            
            if new_files > thresholds["max_new_files"]:
                reasons.append(f"📁 新增文件过多: {new_files}个")
            
            return {
                "needs_refresh": len(reasons) > 0,
                "reasons": reasons,
                "stats": {
                    "total_files": total_files,
                    "new_files": new_files,
                    "total_changes": total_changes
                }
            }
            
        except Exception as e:
            print(f"⚠️ 分析代码变更时出错: {e}")
            return {"needs_refresh": False, "reasons": []}
    
    def _check_config_changes(self) -> List[str]:
        """检查关键配置文件变更"""
        changed_configs = []
        
        try:
            # 检查关键配置文件
            critical_patterns = self.config["patterns"]["critical_files"]
            
            for pattern in critical_patterns:
                # 使用git检查文件变更
                result = subprocess.run([
                    "git", "diff", "--name-only", "HEAD~5..HEAD", "--", pattern
                ], capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode == 0 and result.stdout.strip():
                    changed_files = result.stdout.strip().split('\n')
                    changed_configs.extend(changed_files)
            
        except Exception as e:
            print(f"⚠️ 检查配置变更时出错: {e}")
        
        return list(set(changed_configs))  # 去重
    
    def _check_dependency_changes(self) -> List[str]:
        """检查依赖包变更"""
        dependency_files = [
            "package.json", "package-lock.json",
            "requirements.txt", "Pipfile", "Pipfile.lock",
            "Cargo.toml", "Cargo.lock",
            "go.mod", "go.sum"
        ]
        
        changed_deps = []
        
        try:
            for dep_file in dependency_files:
                if (self.project_root / dep_file).exists():
                    result = subprocess.run([
                        "git", "diff", "--name-only", "HEAD~3..HEAD", "--", dep_file
                    ], capture_output=True, text=True, cwd=self.project_root)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        changed_deps.append(dep_file)
        
        except Exception as e:
            print(f"⚠️ 检查依赖变更时出错: {e}")
        
        return changed_deps
    
    def _check_team_changes(self) -> Optional[str]:
        """检查团队配置变更"""
        team_files = [
            ".ai-context/team/",
            "CODEOWNERS",
            ".github/CODEOWNERS",
            "team.json",
            "contributors.md"
        ]
        
        try:
            for team_file in team_files:
                if (self.project_root / team_file).exists():
                    result = subprocess.run([
                        "git", "diff", "--name-only", "HEAD~3..HEAD", "--", team_file
                    ], capture_output=True, text=True, cwd=self.project_root)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        return f"团队文件变更: {team_file}"
        
        except Exception as e:
            print(f"⚠️ 检查团队变更时出错: {e}")
        
        return None
    
    def refresh_context(self, reason: str = "manual") -> bool:
        """执行上下文刷新"""
        print(f"🔄 开始刷新AI上下文...")
        print(f"📝 刷新原因: {reason}")
        
        try:
            # 运行上下文生成器
            context_generator = self.ai_context_dir / "tools" / "context-generator.py"
            
            if not context_generator.exists():
                print(f"❌ 找不到上下文生成器: {context_generator}")
                return False
            
            result = subprocess.run([
                sys.executable, str(context_generator),
                "--auto-refresh",
                f"--reason={reason}"
            ], cwd=self.project_root)
            
            if result.returncode == 0:
                # 记录刷新信息
                self._record_refresh(reason)
                print("✅ 上下文刷新完成")
                return True
            else:
                print("❌ 上下文刷新失败")
                return False
                
        except Exception as e:
            print(f"❌ 刷新过程中出错: {e}")
            return False
    
    def _record_refresh(self, reason: str):
        """记录刷新信息"""
        refresh_data = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "project_state": self._get_project_state()
        }
        
        with open(self.last_refresh_file, 'w', encoding='utf-8') as f:
            json.dump(refresh_data, f, ensure_ascii=False, indent=2)
    
    def _get_project_state(self) -> Dict:
        """获取当前项目状态快照"""
        try:
            # Git信息
            git_hash = subprocess.run([
                "git", "rev-parse", "HEAD"
            ], capture_output=True, text=True, cwd=self.project_root).stdout.strip()
            
            # 文件统计
            total_files = len(list(self.project_root.rglob("*")))
            
            return {
                "git_commit": git_hash,
                "total_files": total_files,
                "timestamp": datetime.now().isoformat()
            }
        except:
            return {"error": "无法获取项目状态"}
    
    def generate_refresh_report(self) -> Dict:
        """生成刷新需求报告"""
        needs_refresh, reasons = self.check_refresh_needed()
        
        # 获取详细分析
        code_analysis = self._analyze_code_changes()
        config_changes = self._check_config_changes()
        dependency_changes = self._check_dependency_changes()
        
        # 最后一次刷新信息
        last_refresh_info = "未知"
        if self.last_refresh_file.exists():
            try:
                with open(self.last_refresh_file, 'r') as f:
                    last_data = json.load(f)
                    last_refresh_info = last_data["timestamp"]
            except:
                pass
        
        return {
            "需要刷新": needs_refresh,
            "刷新原因": reasons,
            "最后刷新时间": last_refresh_info,
            "代码变更分析": code_analysis,
            "配置文件变更": config_changes,
            "依赖变更": dependency_changes,
            "建议": self._get_recommendations(needs_refresh, reasons)
        }
    
    def _get_recommendations(self, needs_refresh: bool, reasons: List[str]) -> List[str]:
        """获取刷新建议"""
        recommendations = []
        
        if needs_refresh:
            recommendations.append("建议立即执行上下文刷新")
            
            if any("时间过长" in reason for reason in reasons):
                recommendations.append("定期刷新有助于保持AI协作质量")
            
            if any("代码变更" in reason for reason in reasons):
                recommendations.append("大量代码变更可能影响AI理解项目状态")
            
            if any("配置" in reason for reason in reasons):
                recommendations.append("配置变更可能改变项目架构和约束")
        else:
            recommendations.append("当前上下文状态良好，无需刷新")
            recommendations.append("建议继续监控项目变化")
        
        return recommendations

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="智能上下文刷新工具")
    parser.add_argument("--check", action="store_true", help="检查是否需要刷新")
    parser.add_argument("--auto", action="store_true", help="自动刷新（如果需要）")
    parser.add_argument("--force", action="store_true", help="强制刷新")
    parser.add_argument("--report", action="store_true", help="生成详细报告")
    parser.add_argument("--project", default=".", help="项目路径")
    
    args = parser.parse_args()
    
    refresher = SmartContextRefresher(args.project)
    
    if args.report:
        # 生成详细报告
        report = refresher.generate_refresh_report()
        print("\n" + "="*60)
        print("🔍 AI上下文刷新需求分析报告")
        print("="*60)
        
        for key, value in report.items():
            print(f"\n📋 {key}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  • {item}")
            elif isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {value}")
        
    elif args.check:
        # 检查是否需要刷新
        needs_refresh, reasons = refresher.check_refresh_needed()
        
        if needs_refresh:
            print("🔄 需要刷新AI上下文")
            print("\n原因:")
            for reason in reasons:
                print(f"  • {reason}")
            print(f"\n建议运行: python {__file__} --auto")
        else:
            print("✅ AI上下文状态良好，无需刷新")
    
    elif args.auto:
        # 自动刷新
        needs_refresh, reasons = refresher.check_refresh_needed()
        
        if needs_refresh:
            reason_summary = "; ".join(reasons)
            success = refresher.refresh_context(f"自动刷新: {reason_summary}")
            if success:
                print("🎉 上下文已成功刷新")
            else:
                print("❌ 上下文刷新失败")
                sys.exit(1)
        else:
            print("✅ 无需刷新，上下文状态良好")
    
    elif args.force:
        # 强制刷新
        success = refresher.refresh_context("强制刷新")
        if success:
            print("🎉 强制刷新完成")
        else:
            print("❌ 强制刷新失败")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
