import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

console = Console()

DOMAINS = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "whatsapp.com",
    "telegram.org",
    "github.com",
    "netflix.com",
    "spotify.com",
    "twitch.tv",
    "wikipedia.org",
]


def check_domain(domain):
    try:
        start = time.time()
        response = requests.get(f"https://{domain}", timeout=5)
        latency = (time.time() - start) * 1000
        return domain, True, response.status_code, latency
    except Exception:
        return domain, False, None, None


def run_checker():
    results = []
    console.print("[bold yellow]Checking common domains reachability...[/bold yellow]")

    with Progress() as progress:
        task = progress.add_task("[cyan]Checking...", total=len(DOMAINS))
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_domain = {executor.submit(check_domain, d): d for d in DOMAINS}
            for future in as_completed(future_to_domain):
                results.append(future.result())
                progress.update(task, advance=1)

    table = Table(title="Domain Reachability")
    table.add_column("Domain", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Code", style="magenta")
    table.add_column("Latency (ms)", style="green")

    for domain, success, code, lat in results:
        status = "[green]OK[/green]" if success else "[red]Blocked[/red]"
        table.add_row(
            domain, status, str(code) if code else "-", f"{lat:.2f}" if lat else "-"
        )

    console.print(table)


if __name__ == "__main__":
    run_checker()
