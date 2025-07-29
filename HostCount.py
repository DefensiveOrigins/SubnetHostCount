import ipaddress
import argparse
import os

def count_valid_hosts_from_file(file_path):
    total_hosts = 0

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
                            total_hosts += 1
                        else:
                            num_hosts = max(network.num_addresses - 2, 0)
                            total_hosts += num_hosts
                except ValueError as e:
                    print(f"WARNING: {file_path} Line {line_number} - Invalid entry '{entry}': {e}")
    except Exception as e:
        print(f"ERROR: Could not read file {file_path}: {e}")

    return total_hosts

def main():
    parser = argparse.ArgumentParser(description="Count valid hosts in a list of CIDRs or IPs.")
    parser.add_argument("file", nargs='?', help="Path to file containing CIDR ranges or IPs, one per line.")
    parser.add_argument("-d", "--directory", help="Directory of files to process.")
    args = parser.parse_args()

    if args.directory:
        grand_total = 0
        print(f"\nProcessing directory: {args.directory}")
        for entry in os.listdir(args.directory):
            full_path = os.path.join(args.directory, entry)
            if os.path.isfile(full_path):
                count = count_valid_hosts_from_file(full_path)
                print(f"{entry}: {count} hosts")
                grand_total += count
        print(f"\nTotal hosts across all files: {grand_total}")
    elif args.file:
        total = count_valid_hosts_from_file(args.file)
        print(f"\nTotal valid hosts in {args.file} (excluding network and broadcast, except for /32 IPs): {total}")
    else:
        print("ERROR: Either a file or a directory must be specified.")
        parser.print_help()

if __name__ == "__main__":
    main()
