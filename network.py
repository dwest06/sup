import socket
import subprocess
import platform

def ping_host(host = "8.8.8.8"):
    """Ping a host to check network availability."""
    # Determine the command based on the operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    command = ["ping", param, "4", host]  # Ping the host 4 times

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        if "unreachable" in output or "Request timed out" in output:
            print(f"{host} is unreachable.")
        else:
            print(f"{host} is reachable.")
            print(output)
    except subprocess.CalledProcessError:
        print(f"Failed to reach {host}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def check_open_port(host, port):
    """Check if a given port is open on the specified host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)  # Set timeout to 0.5 seconds for faster scanning
        result = sock.connect_ex((host, port))
        return result == 0
    

def scan_ports(ports, host = "127.0.0.1"):
    """Scan a list of ports on the specified host and print their status."""
    print(f"Scanning ports on {host}...")
    for port in ports:
        if check_open_port(host, port):
            print(f"Port {port}: OPEN")
        else:
            print(f"Port {port}: CLOSED")
    print("Port scan completed.")


def scan_all_ports(host = "127.0.0.1"):
    """Scan all ports on the specified host and print their status."""
    print(f"Scanning all ports on {host}...")
    for port in range(1, 65536):  # Scan ports from 1 to 65535
        if check_open_port(host, port):
            print(f"Port {port}: OPEN")
    print("Port scan completed.")
