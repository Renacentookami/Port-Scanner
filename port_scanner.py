import socket
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    # Check if target is an IP address
    is_ip = True
    try:
        parts = target.split('.')
        if len(parts) == 4:
            for part in parts:
                int(part)
        else:
            is_ip = False
    except:
        is_ip = False

    # Resolve IP
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        if is_ip:
            return "Error: Invalid IP address"
        else:
            return "Error: Invalid hostname"

    # Scan ports
    for port in range(port_range[0], port_range[1] + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                open_ports.append(port)
        except:
            pass

    if not verbose:
        return open_ports

    # Verbose mode
    if is_ip:
        header = f"Open ports for {ip}"
    else:
        header = f"Open ports for {target} ({ip})"

    lines = [header, "PORT     SERVICE"]
    
    for port in open_ports:
        service = ports_and_services.get(port, "unknown")
        lines.append(f"{port:<9}{service}")

    return "\n".join(lines)

