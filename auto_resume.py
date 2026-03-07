"""
Auto-Resume System for Bharat GST AI Development
Reads project memory and provides context for daily work sessions
"""

import os
import re
import json
from datetime import datetime

class ProjectMemory:
    """Project memory manager for persistent context"""
    
    def __init__(self, project_dir='.'):
        self.project_dir = project_dir
        self.markdown_file = os.path.join(project_dir, 'PROJECT_MEMORY.md')
        self.json_file = os.path.join(project_dir, 'project_memory.json')
        
        # Try JSON first, fallback to markdown
        if os.path.exists(self.json_file):
            self.data = self.read_json()
        elif os.path.exists(self.markdown_file):
            self.data = self.parse_markdown()
        else:
            self.data = None
    
    def read_json(self):
        """Read JSON memory file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def parse_markdown(self):
        """Parse markdown memory file"""
        try:
            with open(self.markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract project info
            data = {
                'project_name': 'Bharat GST AI',
                'goal': 'India ka automated GST return assistant',
                'phases': [],
                'daily_logs': [],
                'current_phase': 1
            }
            
            # Extract goal
            goal_match = re.search(r'\*\*Goal:\*\* (.+)', content)
            if goal_match:
                data['goal'] = goal_match.group(1)
            
            # Extract daily logs
            day_logs = re.findall(r'### Day (\d+)\s*\(([\d\-]+)\)([^#]+)', content)
            for day_num, date, log_content in day_logs:
                day_data = {
                    'day': int(day_num),
                    'date': date,
                    'status': 'complete',
                    'content': log_content.strip()
                }
                
                # Extract completed tasks
                completed = re.findall(r'- \[x\] (.+)', log_content)
                day_data['tasks_completed'] = completed
                
                # Extract pending tasks
                pending = re.findall(r'- \[ \] (.+)', log_content)
                day_data['pending_tasks'] = pending
                
                # Extract next step
                next_step = re.search(r'\*\*Next Step:\*\* (.+)', log_content)
                if next_step:
                    day_data['next_step'] = next_step.group(1)
                
                data['daily_logs'].append(day_data)
            
            # Find current phase
            latest_day = max(data['daily_logs'], key=lambda x: x['day'], default={'day': 0})
            data['current_day'] = latest_day['day']
            data['next_step'] = latest_day.get('next_step', 'Continue Phase 2')
            data['pending_tasks'] = latest_day.get('pending_tasks', [])
            
            return data
            
        except FileNotFoundError:
            return None
    
    def get_current_phase(self):
        """Get current development phase"""
        if self.data:
            if 'phases' in self.data:
                # Find last completed phase
                for phase in reversed(self.data['phases']):
                    if phase.get('status') == 'complete':
                        return phase['phase_id']
            return self.data.get('current_phase', 1)
        return 1
    
    def get_next_phase(self):
        """Get next phase to work on"""
        current = self.get_current_phase()
        return current + 1
    
    def get_pending_tasks(self):
        """Get pending tasks from current phase"""
        if self.data:
            return self.data.get('pending_tasks', [])
        return []
    
    def get_next_step(self):
        """Get next step from latest log"""
        if self.data:
            return self.data.get('next_step', 'Continue development')
        return 'Start Phase 1'
    
    def print_context(self):
        """Print project context for work session"""
        print("\n" + "=" * 70)
        print("🚀 Bharat GST AI - Project Context")
        print("=" * 70)
        
        if not self.data:
            print("⚠️  No project memory found. Starting fresh!\n")
            print("Follow these steps:")
            print("1. Define project goal in PROJECT_MEMORY.md")
            print("2. Create project phases")
            print("3. Start Phase 1 tasks")
            print("=" * 70 + "\n")
            return False
        
        # Print project info
        print(f"\n📋 Project: {self.data.get('project_name', 'Bharat GST AI')}")
        print(f"🎯 Goal: {self.data.get('goal', 'Unknown')}")
        
        # Print current progress
        current_phase = self.get_current_phase()
        current_day = self.data.get('current_day', 1)
        print(f"\n📊 Current Phase: {current_phase}")
        print(f"📅 Day: {current_day}")
        
        # Print pending tasks
        pending = self.get_pending_tasks()
        if pending:
            print(f"\n📝 Pending Tasks ({len(pending)}):")
            for i, task in enumerate(pending, 1):
                print(f"   {i}. {task}")
        else:
            print("\n✅ All tasks complete! Moving to next phase.")
        
        # Print next step
        next_step = self.get_next_step()
        print(f"\n💡 Next Step:")
        print(f"   {next_step}")
        
        print("\n" + "=" * 70 + "\n")
        return True
    
    def update_progress(self, task_completed, notes=""):
        """Update progress when a task is completed"""
        if not self.data:
            return False
        
        # Update pending tasks (remove completed task)
        pending = self.data.get('pending_tasks', [])
        if task_completed in pending:
            pending.remove(task_completed)
            self.data['pending_tasks'] = pending
        
        # Update next step
        if notes:
            self.data['next_step'] = notes
        else:
            # Update next task
            if pending:
                self.data['next_step'] = pending[0]
        
        # Write back to JSON
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        
        return True


def resume_work():
    """Auto-resume function - called when starting daily work session"""
    print("\n" + "=" * 70)
    print("🔄 AUTO-RESUME: Bharat GST AI Project")
    print("=" * 70 + "\n")
    
    memory = ProjectMemory()
    
    if not memory.data:
        print("⚠️  No project memory found!\n")
        print("Initializing new project...")
        
        # Create initial JSON structure
        initial_data = {
            "project_info": {
                "name": "Bharat GST AI",
                "goal": "India ka automated GST return assistant - #1 GST automation tool",
                "timeline": "1-2 months",
                "start_date": "2026-03-07",
                "expected_launch": "2026-04-07 to 2026-05-07",
                "status": "Development Phase"
            },
            "phases": [],
            "daily_logs": [
                {
                    "day": 1,
                    "date": "2026-03-07",
                    "status": "complete",
                    "tasks_completed": [
                        "Created GitHub repository",
                        "Built GST calculation engine",
                        "Implemented GSTIN validation",
                        "Created invoice management system",
                        "Built GSTR-1 report generation",
                        "Built GSTR-3B tax calculation",
                        "Created beautiful web UI",
                        "Implemented persistent memory system"
                    ],
                    "pending_tasks": [
                        "Add PDF invoice generation",
                        "Create Excel export",
                        "Add multi-item invoice support"
                    ],
                    "next_step": "Implement PDF invoice generation using ReportLab library"
                }
            ],
            "metadata": {
                "created_date": "2026-03-07",
                "last_updated": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                "version": "0.1"
            }
        }
        
        # Write initial JSON
        with open('project_memory.json', 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=4, ensure_ascii=False)
        
        print("✅ Project initialized successfully!\n")
        print("=" * 70 + "\n")
        return False
    
    memory.print_context()
    
    print(f"📅 Today's Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"⏰ Current Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📁 Working Directory: {os.getcwd()}\n")
    
    print("💡 Tip: Update progress after completing each task")
    print("   Use: python -c 'from auto_resume import ProjectMemory; m = ProjectMemory(); m.update_progress(\"task\")'\n")
    
    return True


# Command-line interface
if __name__ == '__main__':
    resume_work()
