import requests
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

IRAN_NODES = ["ir1.node.check-host.net", "ir2.node.check-host.net", "ir3.node.check-host.net", "ir4.node.check-host.net"]

def check_host_iran(target, check_type="ping"):
    api_url = f"https://check-host.net/check-{check_type}"
    params = {
        "host": target,
        "node": IRAN_NODES
    }
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        request_data = response.json()
        request_id = request_data.get("request_id")
        
        if not request_id:
            console.print("[bold red]Failed to initialize check-host request.[/bold red]")
            return

        console.print(f"[bold yellow]Check initialized (ID: {request_id}). Waiting for results...[/bold yellow]")
        
        results_url = f"https://check-host.net/check-result/{request_id}"
        
        results = {}
        with Live(console=console, refresh_per_second=1) as live:
            for _ in range(30): # Timeout after 30 seconds
                time.sleep(2)
                res = requests.get(results_url, headers=headers)
                data = res.json()
                
                table = Table(title=f"Check-Host Results for {target}")
                table.add_column("Node", style="cyan")
                table.add_column("Status", style="magenta")
                table.add_column("Result", style="green")
                
                nodes_finished = 0
                for node, node_res in data.items():
                    if node_res:
                        nodes_finished += 1
                        # Format result based on check_type
                        if check_type == "ping":
                            # Ping returns a list of results
                            successes = [r for r in node_res if r[0] == "OK"]
                            if successes:
                                avg_lat = sum([r[1] for r in successes]) / len(successes)
                                table.add_row(node, "[green]Online[/green]", f"{avg_lat*1000:.2f} ms")
                            else:
                                table.add_row(node, "[red]Offline[/red]", "-")
                        elif check_type == "http":
                            status = node_res[0][2]
                            table.add_row(node, f"[blue]{status}[/blue]", f"{node_res[0][1]}s")
                    else:
                        table.add_row(node, "[yellow]Waiting...[/yellow]", "-")
                
                live.update(table)
                if nodes_finished >= len(IRAN_NODES):
                    break
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_host.py <target> [ping|http]")
        sys.exit(1)
    
    target = sys.argv[1]
    ctype = sys.argv[2] if len(sys.argv) > 2 else "ping"
    check_host_iran(target, ctype)
