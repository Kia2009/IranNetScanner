import time

import dns.resolver
from rich.console import Console
from rich.table import Table

console = Console()

DNS_PROVIDERS = {
    "Cloudflare": "1.1.1.1",
    "Google": "8.8.8.8",
    "Quad9": "9.9.9.9",
    "OpenDNS": "208.67.222.222",
    "Shecan (IR)": "178.22.122.100",
    "403.online (IR)": "10.202.10.10",
    "Electro (IR)": "78.157.42.100",
}


def test_dns_latency():
    table = Table(title="DNS Latency Test")
    table.add_column("Provider", style="cyan")
    table.add_column("IP", style="magenta")
    table.add_column("Latency (ms)", style="green")

    for name, ip in DNS_PROVIDERS.items():
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        resolver.timeout = 2
        resolver.lifetime = 2

        start = time.time()
        try:
            resolver.resolve("google.com", "A")
            latency = (time.time() - start) * 1000
            table.add_row(name, ip, f"{latency:.2f}")
        except Exception:
            table.add_row(name, ip, "[red]Timeout[/red]")

    console.print(table)


def dns_hunter(domain):
    console.print(f"[bold yellow]DNS Hunter for: {domain}[/bold yellow]")
    table = Table(title=f"Resolution across providers")
    table.add_column("Provider", style="cyan")
    table.add_column("Resolved IP", style="magenta")

    for name, ip in DNS_PROVIDERS.items():
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        resolver.timeout = 2
        resolver.lifetime = 2
        try:
            answers = resolver.resolve(domain, "A")
            ips = [str(rdata) for rdata in answers]
            table.add_row(name, ", ".join(ips))
        except Exception as e:
            table.add_row(name, f"[red]Error: {str(e)}[/red]")

    console.print(table)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "latency":
            test_dns_latency()
        elif sys.argv[1] == "hunter" and len(sys.argv) > 2:
            dns_hunter(sys.argv[2])
    else:
        test_dns_latency()
