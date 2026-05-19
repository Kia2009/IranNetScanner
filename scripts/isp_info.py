import requests
from rich.console import Console
from rich.table import Table

console = Console()

def get_isp_info():
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()

        table = Table(title="ISP Information")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("IP", data.get("ip"))
        table.add_row("City", data.get("city"))
        table.add_row("Region", data.get("region"))
        table.add_row("Country", data.get("country_name"))
        table.add_row("ISP", data.get("org"))
        table.add_row("ASN", data.get("asn"))

        console.print(table)
        return data
    except Exception as e:
        console.print(f"[bold red]Error fetching ISP info: {e}[/bold red]")
        return None

if __name__ == "__main__":
    get_isp_info()
