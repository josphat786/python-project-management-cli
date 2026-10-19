import argparse #Passes command line options and arguments to the program
import sys #provides access to system-specific parameters and functions
from models.user import User #importing the User class from the models.user module to manage user-related operations
from models.project import Project #handles project-related operations and data management
from models.task import Task #manages task-related operations and data management
from utils.storage import Storage #provides persistent storage and retrieval of data for users, projects, and tasks

# Rich styling components to assist in high quality terminal visuals
from rich.console import Console
from rich.table import Table

# Configure rich to explicitly write to standard error when tracking logs if needed
console = Console()
error_console = Console(stderr=True) # output error messages to standard error stream

def main(): #entry point for the CLI application, orchestrating command parsing and execution
    parser = argparse.ArgumentParser(
        description="Task Management System CLI Tool - Manage users, projects, and tasks efficiently from the command line."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # --- add-user subcommand ---
    parser_user = subparsers.add_parser("add-user", help="Register a new user account")
    parser_user.add_argument("--name", required=True, help="Full name of the user")
    parser_user.add_argument("--email", required=True, help="Unique email address")

    # --- add-project subcommand ---
    parser_project = subparsers.add_parser("add-project", help="Create a new project tracking space")
    parser_project.add_argument("--title", required=True, help="Title of the project")
    parser_project.add_argument("--description", required=True, help="Detailed summary")
    parser_project.add_argument("--due-date", required=True, help="Target due date (YYYY-MM-DD)")
    parser_project.add_argument("--user-id", type=int, required=True, help="ID of the owner user")

    # --- add-task subcommand ---
    parser_task = subparsers.add_parser("add-task", help="Append a task to a project matrix")
    parser_task.add_argument("--title", required=True, help="Title of the task")
    parser_task.add_argument("--assigned-to", type=int, required=True, help="ID of user assigned")
    parser_task.add_argument("--project-id", type=int, required=True, help="ID of target project")

    # --- list-projects subcommand ---
    subparsers.add_parser("list-projects", help="Render all linked projects and internal tasks")

    # --- complete-task subcommand ---
    parser_complete = subparsers.add_parser("complete-task", help="Toggle a task status to 'Completed'")
    parser_complete.add_argument("--task-id", type=int, required=True, help="Target unique Task ID")

    args = parser.parse_args() #Parse the command line arguments and store them in the 'args' namespace for further processing

    if not args.command:
        parser.print_help()
        sys.exit(0) #Exit gracefully if no subcommand is provided, displaying the help message

    try:
        # Pre-initialize data contexts using class models
        User.load_collection()
        Project.load_collection()
        Task.load_collection()

        if args.command == "add-user":
            user = User(name=args.name, email=args.email)
            User.save_collection()
            console.print(f"[bold green]Success:[/bold green] Created {user}")

        elif args.command == "add-project":
            if not any(u.id == args.user_id for u in User.ALL_USERS):
                error_console.print(f"[bold red]Error:[/bold red] User with ID {args.user_id} does not exist.")
                sys.exit(1)
                
            project = Project(title=args.title, description=args.description, due_date=args.due_date, user_id=args.user_id)
            Project.save_collection()
            console.print(f"[bold green]Success:[/bold green] Created {project}")

        elif args.command == "add-task":
            if not any(u.id == args.assigned_to for u in User.ALL_USERS):
                error_console.print(f"[bold red]Error:[/bold red] User ID {args.assigned_to} not found.")
                sys.exit(1)
            if not any(p.id == args.project_id for p in Project.ALL_PROJECTS):
                error_console.print(f"[bold red]Error:[/bold red] Project ID {args.project_id} not found.")
                sys.exit(1)

            task = Task(title=args.title, assigned_to=args.assigned_to, project_id=args.project_id)
            Task.save_collection()
            console.print(f"[bold green]Success:[/bold green] Created {task}")

        elif args.command == "list-projects":
            if not Project.ALL_PROJECTS:
                console.print("[yellow]No projects tracked in system records.[/yellow]")
                return

            table = Table(title="System Operational Project Tree Topology")
            table.add_column("Proj ID", style="cyan", no_wrap=True)
            table.add_column("Project Details", style="white")
            table.add_column("Owner", style="magenta")
            table.add_column("Tasks Backlog Hierarchy", style="green")

            for proj in Project.ALL_PROJECTS:
                owner = next((u.name for u in User.ALL_USERS if u.id == proj.user_id), "Unknown")
                proj_tasks = [t for t in Task.ALL_TASKS if t.project_id == proj.id]
                
                if proj_tasks:
                    task_lines = []
                    for t in proj_tasks:
                        status_color = "green" if t.status == "Completed" else "yellow"
                        assignee = next((u.name for u in User.ALL_USERS if u.id == t.assigned_to), "Unknown")
                        task_lines.append(f"• ID {t.id}: {t.title} [[{status_color}]{t.status}[/{status_color}]] (Assigned: {assignee})")
                    tasks_str = "\n".join(task_lines)
                else:
                    tasks_str = "[italic gray37]No tasks added[/italic gray37]"

                table.add_row(
                    str(proj.id),
                    f"[bold]{proj.title}[/bold]\n[dim]{proj.description}[/dim]\nDue: {proj.due_date}",
                    owner,
                    tasks_str
                )
            console.print(table)

        elif args.command == "complete-task":
            target_task = next((t for t in Task.ALL_TASKS if t.id == args.task_id), None)
            if not target_task:
                error_console.print(f"[bold red]Error:[/bold red] Task with ID {args.task_id} not found.")
                sys.exit(1)
            
            target_task.status = "Completed"
            Task.save_collection()
            console.print(f"[bold green]Success:[/bold green] Task {args.task_id} status flipped to [bold]Completed[/bold].")

    except Exception as e:
        error_console.print(f"[bold red]Operational Runtime Failure:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__": #Ensures that the main function is executed only when the script is run directly, not when imported as a module
    main() #call the main function to start the CLI application
