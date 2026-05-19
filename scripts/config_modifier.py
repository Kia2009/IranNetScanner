import base64
import json
import re
import sys

from rich.console import Console

console = Console()


def modify_vless(config, new_ips):
    # vless://uuid@host:port?params#name
    try:
        if config.startswith("vless://"):
            parts = re.split(r"[@:/?#]", config[8:])
            # uuid is parts[0]
            # host is parts[1]
            # port is parts[2]

            uuid = parts[0]
            old_host = parts[1]
            port = parts[2]

            # Find the original name (after #)
            name_match = re.search(r"#(.*)$", config)
            original_name = name_match.group(1) if name_match else "Modified"

            # Find params (between ? and #)
            params_match = re.search(r"\?(.*?)($|#)", config)
            params = params_match.group(1) if params_match else ""

            modified_configs = []
            for ip in new_ips:
                new_config = f"vless://{uuid}@{ip}:{port}?{params}#{original_name}_{ip}"
                modified_configs.append(new_config)

            return modified_configs
        else:
            console.print("[bold red]Not a valid VLESS config[/bold red]")
            return []
    except Exception as e:
        console.print(f"[bold red]Error modifying config: {e}[/bold red]")
        return []


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 config_modifier.py <vless_link> <ips_comma_separated>")
        sys.exit(1)

    link = sys.argv[1]
    ips = sys.argv[2].split(",")

    modified = modify_vless(link, ips)
    for c in modified:
        print(c)
