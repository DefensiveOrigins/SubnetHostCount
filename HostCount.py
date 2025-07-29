import ipaddress
import argparse
import os

def extract_unique_hosts_from_file(file_path):
    unique_hosts = set()

    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                entry = line.strip()
                if not entry or entry.startswith("#"):
                    continue  # Skip empty lines or comments

                try:
                    if '/' not in entry:
                        entry += '/32'
                    network = ipaddress.ip_network(entry, strict=False)
                    if isinstance(network, ipaddress.IPv4Network):
                        if network.prefixlen == 32:
                            unique_hosts.add(str(network.network_address))
                        else:
                            # Add usable hosts only (skip network and broadcast)
                            for host in network.hosts():
                                unique_hosts.add(str(host))
                except ValueError as e:
                    print(f"WARNING: {file_path} Line {line_number} - Invalid entry '{entry}': {e}")
    except Exception as e:
        print(f"ERROR: Could not read file {file_path}: {e}")

    return unique_hosts

def main():
    parser = argparse.ArgumentParser(description="Count unique valid hosts from CIDRs or IPs in files.")
    parser.add_argument("file", nargs='?', help="Path to file containing CIDR ranges or IPs, one per line.")
    parser.add_argument("-d", "--directory", help="Directory of files to process.")
    args = parser.parse_args()

    if args.directory:
        grand_total_hosts = set()
        print(f"\nProcessing directory: {args.directory}")
        for entry in os.listdir(args.directory):
            full_path = os.path.join(args.directory, entry)
            if os.path.isfile(full_path):
                file_hosts = extract_unique_hosts_from_file(full_path)
                print(f"{entry}: {len(file_hosts)} unique hosts")
                grand_total_hosts.update(file_hosts)
        print(f"\nTotal unique hosts across all files: {len(grand_total_hosts)}")

    elif args.file:
        unique_hosts = extract_unique_hosts_from_file(args.file)
        print(f"\nTotal unique hosts in {args.file} (excluding network and broadcast): {len(unique_hosts)}")

    else:
        print("ERROR: Either a file or a directory must be specified.")
        parser.print_help()

if __name__ == "__main__":
    main()
