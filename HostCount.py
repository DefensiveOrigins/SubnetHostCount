import ipaddress
import argparse

def count_valid_hosts_from_file(file_path):
    total_hosts = 0

    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            entry = line.strip()
            if not entry or entry.startswith("#"):
                continue  # Skip empty lines or comments

            try:
                # Treat plain IPs as /32
                if '/' not in entry:
                    entry += '/32'
                network = ipaddress.ip_network(entry, strict=False)
                if isinstance(network, ipaddress.IPv4Network):
                    if network.prefixlen == 32:
                        total_hosts += 1
                    else:
                        num_hosts = max(network.num_addresses - 2, 0)
                        total_hosts += num_hosts
            except ValueError as e:
                print(f"WARNING: Line {line_number} - Invalid entry '{entry}': {e}")

    return total_hosts

def main():
    parser = argparse.ArgumentParser(description="Count valid hosts in a list of CIDRs or IPs.")
    parser.add_argument("file", help="Path to file containing CIDR ranges or IPs, one per line.")
    args = parser.parse_args()

    total = count_valid_hosts_from_file(args.file)
    print(f"\nTotal valid hosts (excluding network and broadcast, except for /32 IPs): {total}")

if __name__ == "__main__":
    main()
