import ipaddress
import random
import sys
import threading
import time
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


def scan_cdn(cdn_name, sni_list, ip_file, max_threads=50, limit=100):
    ips_or_cidrs = load_ips(ip_file)
    all_ips = []
    for item in ips_or_cidrs:
        if "/" in item:
            try:
                network = ipaddress.ip_network(item)
                # Just take a sample if it's too large to be practical
                if network.num_addresses > 1000:
                    all_ips.extend(
                        [str(ip) for ip in random.sample(list(network.hosts()), 50)]
                    )
                else:
                    all_ips.extend([str(ip) for ip in network.hosts()])
            except Exception:
                pass
        else:
            all_ips.append(item)

    if not all_ips:
        console.print(f"[bold red]No IPs found for {cdn_name}[/bold red]")
        return

    random.shuffle(all_ips)
    test_ips = all_ips[:limit]

    sni = sni_list[0]  # Default to first SNI
    results = []

    console.print(
        f"[bold yellow]Scanning {cdn_name} ({len(test_ips)} IPs) using SNI: {sni}...[/bold yellow]"
    )

    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=len(test_ips))
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_ip = {executor.submit(test_ip, ip, sni): ip for ip in test_ips}
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
        scan_cdn(cdn_type.capitalize(), sni, ip_file)
    else:
        print(f"Unknown CDN type: {cdn_type}")
