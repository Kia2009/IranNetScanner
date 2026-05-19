import ipaddress
import random
import sys
import threading
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

try:
    from utils import load_ips
except ImportError:
    from scripts.utils import load_ips

console = Console()


def test_ip(ip, sni, timeout=2):
    url = f"https://{ip}/"
    headers = {"Host": sni}
    start_time = time.time()
    try:
        # We use a HEAD request with no-cors equivalent logic
        # Actually in Python requests, we just check if we can establish a connection
        response = requests.head(url, headers=headers, timeout=timeout, verify=False)
        latency = (time.time() - start_time) * 1000
        return ip, True, latency
    except Exception:
        return ip, False, None


def scan_cdn(cdn_name, sni_list, selected_items, max_threads=50, limit=100):
    all_ips = []

    # Calculate how many IPs to take from each range to be "fair"
    if selected_items:
        per_range_limit = max(1, limit // len(selected_items))

        for item in selected_items:
            if "/" in item:
                try:
                    network = ipaddress.ip_network(item)
                    hosts = list(network.hosts())
                    sample_size = min(len(hosts), per_range_limit)
                    all_ips.extend(
                        [str(ip) for ip in random.sample(hosts, sample_size)]
                    )
                except Exception:
                    pass
            else:
                all_ips.append(item)

    if not all_ips:
        console.print(f"[bold red]No IPs to scan.[/bold red]")
        return

    sni = sni_list[0]  # Default to first SNI
    results = []

    console.print(
        f"[bold yellow]Scanning {cdn_name} ({len(all_ips)} IPs) using SNI: {sni}...[/bold yellow]"
    )

    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=len(all_ips))
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_ip = {executor.submit(test_ip, ip, sni): ip for ip in all_ips}
            for future in as_completed(future_to_ip):
                res = future.result()
                if res[1]:
                    results.append(res)
                progress.update(task, advance=1)

    if results:
        results.sort(key=lambda x: x[2])
        table = Table(title=f"Working {cdn_name} IPs")
        table.add_column("IP Address", style="cyan")
        table.add_column("Latency (ms)", style="green")

        for ip, _, lat in results[:20]:
            table.add_row(ip, f"{lat:.2f}")

        console.print(table)

        # Save results
        with open(f"{cdn_name.lower()}_results.txt", "w") as f:
            f.write(",".join([r[0] for r in results]))
        console.print(
            f"[bold green]Results saved to {cdn_name.lower()}_results.txt[/bold green]"
        )
    else:
        console.print("[bold red]No working IPs found.[/bold red]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cdn_scanner.py <cdn_type>")
        sys.exit(1)

    cdn_type = sys.argv[1].lower()

    cdns = {
        "cloudflare": (["www.cloudflare.com"], "cf_ips.txt"),
        "akamai": (["a248.e.akamai.net", "a77.net.akamai.net"], "akamai_ips.txt"),
        "google": (["fonts.googleapis.com", "ajax.googleapis.com"], "google_ips.txt"),
        "amazon": (["d1.cloudfront.net", "aws.cloudfront.net"], "amazon_ips.txt"),
        "azure": (["ajax.aspnetcdn.com", "cdn.office.net"], "azure_ips.txt"),
    }

    if cdn_type in cdns:
        sni, ip_file = cdns[cdn_type]

        # New selection logic
        available_ranges = load_ips(ip_file)

        # Check if custom_ips.txt exists
        custom_path = "custom_ips.txt"
        if os.path.exists(custom_path):
            with open(custom_path, "r") as f:
                custom_ips = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
            if custom_ips:
                available_ranges.append("--- CUSTOM IPS FROM FILE ---")
                available_ranges.extend(custom_ips)

        # In a real TUI we'd use a better picker, but for simplicity here:
        console.print(
            f"[bold cyan]Available ranges for {cdn_type.capitalize()}:[/bold cyan]"
        )
        for i, r in enumerate(available_ranges):
            console.print(f"{i + 1}) {r}")

        choice = console.input(
            "[bold yellow]Enter numbers to scan (comma separated, or 'all'): [/bold yellow]"
        )
        limit_input = (
            console.input(
                "[bold yellow]Max IPs to scan in total (default 100): [/bold yellow]"
            )
            or "100"
        )

        try:
            scan_limit = int(limit_input)
        except:
            scan_limit = 100

        selected_ranges = []
        if choice.lower() == "all":
            selected_ranges = [r for r in available_ranges if not r.startswith("---")]
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]
                selected_ranges = [
                    available_ranges[i]
                    for i in indices
                    if i < len(available_ranges)
                    and not available_ranges[i].startswith("---")
                ]
            except:
                console.print(
                    "[bold red]Invalid choice, scanning all default ranges.[/bold red]"
                )
                selected_ranges = load_ips(ip_file)

        scan_cdn(cdn_type.capitalize(), sni, selected_ranges, limit=scan_limit)
    else:
        print(f"Unknown CDN type: {cdn_type}")
