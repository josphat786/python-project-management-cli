import subprocess
import json
import os
from rich.console import Console

console = Console()

def run_cmd(cmd_list):
    """Helper to run a terminal command and return output."""
    result = subprocess.run(["python"] + cmd_list, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    console.print("[bold blue]🚀 Starting Automated System Verification Tests...[/bold blue]\n")

    # Clean up old data files to ensure a fresh test suite run
    for filename in ["users.json", "projects.json", "tasks.json"]:
        path = os.path.join("data", filename)
        if os.path.exists(path):
            os.remove(path)

    # -------------------------------------------------------------
    # TEST 1: Add a Valid User
    # -------------------------------------------------------------
    console.print("[bold yellow]Test 1: Adding a valid user...[/bold yellow]")
    code, out, err = run_cmd(["main.py", "add-user", "--name", "Alice Dev", "--email", "alice@example.com"])
    if code == 0:
        console.print("[green]✔ Passed: User created successfully.[/green]")
    else:
        console.print(f"[red]❌ Failed: {err}[/red]")

    # -------------------------------------------------------------
    # TEST 2: Trigger Email Validation Constraint
    # -------------------------------------------------------------
    console.print("\n[bold yellow]Test 2: Injecting an invalid email format...[/bold yellow]")
    code, out, err = run_cmd(["main.py", "add-user", "--name", "Bob", "--email", "bad-email-format"])
    if code != 0 and "Malformed structural parameter" in err:
        console.print("[green]✔ Passed: System successfully blocked the invalid email address.[/green]")
    else:
        console.print(f"[red]❌ Failed: System allowed a bad email or returned unexpected error: {err}[/red]")

    # -------------------------------------------------------------
    # TEST 3: Add a Valid Project linked to User 1
    # -------------------------------------------------------------
    console.print("\n[bold yellow]Test 3: Creating a project for User ID 1...[/bold yellow]")
    code, out, err = run_cmd(["main.py", "add-project", "--title", "Core Engine", "--description", "Building modules", "--due-date", "2026-12-31", "--user-id", "1"])
    if code == 0:
        console.print("[green]✔ Passed: Project successfully linked to user.[/green]")
    else:
        console.print(f"[red]❌ Failed: {err}[/red]")

    # -------------------------------------------------------------
    # TEST 4: Trigger Foreign Key Relationship Constraint
    # -------------------------------------------------------------
    console.print("\n[bold yellow]Test 4: Creating a project for a non-existent User ID (99)...[/bold yellow]")
    code, out, err = run_cmd(["main.py", "add-project", "--title", "Ghost Project", "--description", "No owner", "--due-date", "2026-12-31", "--user-id", "99"])
    if code != 0 and "does not exist" in err:
        console.print("[green]✔ Passed: System successfully blocked orphan project generation.[/green]")
    else:
        console.print(f"[red]❌ Failed: Orphan project creation was not blocked: {err}[/red]")

    # -------------------------------------------------------------
    # TEST 5: Add and Complete a Task
    # -------------------------------------------------------------
    console.print("\n[bold yellow]Test 5: Appending and closing a task item...[/bold yellow]")
    # Add Task
    run_cmd(["main.py", "add-task", "--title", "Initialize Git", "--assigned-to", "1", "--project-id", "1"])
    # Complete Task
    code, out, err = run_cmd(["main.py", "complete-task", "--task-id", "1"])
    if code == 0 and "flipped to Completed" in out:
        console.print("[green]✔ Passed: Task added and status toggled cleanly.[/green]")
    else:
        console.print(f"[red]❌ Failed to update task: {out} {err}[/red]")

    # -------------------------------------------------------------
    # TEST 6: Render View Topology
    # -------------------------------------------------------------
    console.print("\n[bold yellow]Test 6: Generating graphical project overview tree...[/bold yellow]")
    code, out, err = run_cmd(["main.py", "list-projects"])
    if code == 0:
        console.print("[green]✔ Passed: Table rendered without crashing. View output below:[/green]\n")
        print(out)
    else:
        console.print(f"[red]❌ Failed to display table: {err}[/red]")

if __name__ == "__main__":
    main()
