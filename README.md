# SubnetHostCount
Simple python to count hosts in a list of subnets and ip addresses


# CIDR Host Counter

This script reads a file containing IPv4 CIDR notations or individual IP addresses and calculates the total number of valid hosts. It excludes network and broadcast addresses for subnets, but counts single IPs (e.g., `10.0.0.5`) as one valid host.

## Features

- Accepts a file containing:
  - IPv4 CIDR ranges (e.g., `192.168.1.0/24`)
  - Individual IP addresses (e.g., `10.0.0.5`)
- Excludes network and broadcast addresses from the host count
- Ignores empty lines and lines starting with `#`
- Warns about invalid lines with a descriptive message

## Usage

### Prerequisites

Python 3.6+

### Command

```bash
python count_hosts.py path/to/cidrs.txt
