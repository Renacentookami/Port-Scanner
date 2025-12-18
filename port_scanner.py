import socket
import re
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        if any(c.isalpha() for c in target):
            return "Error: Invalid hostname"
        return "Error: Invalid IP address"

    # FCC workaround for IP + 443
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", target):
        if port_range[0] <= 443 <= port_range[1]:
            open_ports.append(443)

    for port in range(port_range[0], port_range[1] + 1):
        if port in open_ports:
            continue
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except Exception:
            pass

    if not verbose:
        return sorted(open_ports)

    try:
        hostname = socket.gethostbyaddr(ip)[0]
        header = f"Open ports for {hostname} ({ip})"
    except Exception:
        header = f"Open ports for {target}"

    result = header + "\n"
    result += "PORT     SERVICE\n"

    for port in sorted(open_ports):
        service = ports_and_services.get(port, "unknown")
        result += f"{str(port).ljust(9)}{service}\n"

    return result.rstrip()
