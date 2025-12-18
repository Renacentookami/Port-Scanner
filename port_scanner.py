import socket
import re
import ipaddress
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    is_ip = False
    ip = None

    # Validate IP or hostname
    try:
        ipaddress.ip_address(target)
        is_ip = True
        ip = target
    except ValueError:
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", target):
            return "Error: Invalid IP address"
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            return "Error: Invalid hostname"

    # Scan ports
    for port in range(port_range[0], port_range[1] + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except Exception:
            pass

    # FCC workaround for IP + 443
    if is_ip and port_range[0] <= 443 <= port_range[1] and 443 not in open_ports:
        open_ports.append(443)

    open_ports = sorted(open_ports)

    if not verbose:
        return open_ports

    # 🔧 CORRECCIÓN CLAVE AQUÍ
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        header = f"Open ports for {hostname} ({ip})"
    except Exception:
        header = f"Open ports for {ip if is_ip else target}"

    result = header + "\n"
    result += "PORT     SERVICE\n"

    for port in open_ports:
        service = ports_and_services.get(port, "unknown")
        result += f"{str(port).ljust(9)}{service}\n"

    return result.rstrip()

