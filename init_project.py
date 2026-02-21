import os
import re
import sys
import subprocess
from pathlib import Path

# Template defaults to look for
DEFAULT_PROJECT_NAME = "mlops-blueprint"
DEFAULT_SNAKE_CASE_NAME = "mlops_blueprint"

# Directories to skip during find-and-replace
SKIP_DIRS = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".vscode",
    ".azure",
    ".databricks",
    "__pycache__",
    "dist",
    "build",
}

# Files to skip
SKIP_FILES = {
    "uv.lock",
    os.path.basename(__file__)  # skip this script itself
}

def prompt_user():
    print("Welcome to the Databricks MLOps Blueprint initialized setup!")
    print("Please provide the required details for your new project.\n")
    
    project_name = ""
    while not project_name:
        project_name = input("Enter the new Project Name (e.g. my-awesome-project): ").strip()
        if not project_name:
            print("Project Name is required. Please try again.")

    sandbox_url = input(f"Enter Databricks Sandbox Workspace URL [optional, press Enter to keep placeholder]: ").strip()
    if not sandbox_url:
        sandbox_url = "<YOUR_SANDBOX_WORKSPACE_URL>"

    prod_url = input(f"Enter Databricks Prod Workspace URL [optional, press Enter to keep placeholder]: ").strip()
    if not prod_url:
        prod_url = "<YOUR_PROD_WORKSPACE_URL>"

    return project_name, sandbox_url, prod_url

def to_snake_case(s):
    # Very simple kebab-case to snake_case converter assuming standard input
    return s.replace("-", "_")

def replace_in_file(file_path, replacements):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        for old_text, new_text in replacements.items():
            new_content = new_content.replace(old_text, new_text)
            
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or unreadable files
        pass

def update_databricks_yml(file_path, sandbox_url, prod_url):
    """Specific targeted update for databricks.yml host urls to avoid overlapping string issues"""
    if not os.path.exists(file_path):
        return
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        new_lines = []
        target_mode = None
        for line in lines:
            if line.strip() == "sandbox:":
                target_mode = "sandbox"
            elif line.strip() == "prod:":
                target_mode = "prod"
            
            # If we see the host line, replace based on the current block we're in
            if "host:" in line and target_mode:
                if target_mode == "sandbox" and sandbox_url:
                    line = re.sub(r'host:\s*.*', f'host: {sandbox_url}', line)
                elif target_mode == "prod" and prod_url:
                    line = re.sub(r'host:\s*.*', f'host: {prod_url}', line)
                    
            new_lines.append(line)
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"Warning: Failed to update databricks.yml workspace URLs: {e}")

def main():
    project_name, sandbox_url, prod_url = prompt_user()
    snake_case_name = to_snake_case(project_name)
    
    replacements = {
        DEFAULT_PROJECT_NAME: project_name,
        DEFAULT_SNAKE_CASE_NAME: snake_case_name
    }
    
    root_dir = Path(__file__).parent.resolve()
    
    print("\nApplying text replacements across repository files...")
    for path in root_dir.rglob("*"):
        if not path.is_file():
            continue
            
        # Check if file is in skipped directories
        parts = path.relative_to(root_dir).parts
        if any(part in SKIP_DIRS for part in parts):
            continue
            
        if path.name in SKIP_FILES:
            continue
            
        # Standard replacements
        replace_in_file(path, replacements)
        
    # Explicitly update databricks.yml for workspace urls
    databricks_yml_path = root_dir / "databricks.yml"
    update_databricks_yml(str(databricks_yml_path), sandbox_url, prod_url)
        
    print("Updating locked dependencies with 'uv lock'...")
    try:
        subprocess.run(["uv", "lock"], cwd=str(root_dir), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Warning: 'uv lock' failed. You may need to run it manually. Error: {e}")
    except FileNotFoundError:
        print("Warning: 'uv' executable not found. Please run 'uv lock' manually later.")
        
    # Delete self
    self_path = os.path.abspath(__file__)
    print(f"Deleting setup script ({self_path})...")
    os.remove(self_path)
    
    # Auto-commit
    print("Committing initialization changes to Git...")
    try:
        subprocess.run(["git", "add", "-A"], cwd=str(root_dir), check=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: initialized project from mlops-blueprint template"],
            cwd=str(root_dir), check=True
        )
        print(f"\n✨ Project '{project_name}' initialized successfully! ✨\n")
        
        print("="*60)
        print("NEXT STEPS:")
        print(f"1. Setup environment: uv sync --extra local-dev")
        print(f"2. Start interactive development in notebooks/scratchpad.py")
        print(f"3. Databricks job entry points are pre-defined in: src/{snake_case_name}/main.py")
        print("="*60 + "\n")
        
    except subprocess.CalledProcessError as e:
        print(f"Warning: Git commit failed. You may need to commit manually. Error: {e}")
    except FileNotFoundError:
        print("Warning: Git executable not found. Please commit changes manually.")

if __name__ == "__main__":
    main()
