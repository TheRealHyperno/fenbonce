#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os

def run(cmd):
    print(f"Executing: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def setup_fenbonce(storage_dev, cache_dev, vg_name="fenbonce_vg"):
    # 1. Create Physical Volumes
    # Using the devices provided (which can now be partitions like /dev/sdb1)
    run(["pvcreate", "-y", storage_dev])
    run(["pvcreate", "-y", cache_dev])

    # 2. Create Volume Group
    run(["vgcreate", vg_name, storage_dev])

    # 3. Create the Data Logical Volume (The big storage)
    # We use 95% of storage to leave some room for metadata/snapshots
    run(["lvcreate", "-l", "95%FREE", "-n", "data_lv", vg_name])

    # 4. Add the cache device to the VG
    run(["vgextend", vg_name, cache_dev])

    # 5. Create the Cache Pool
    # This creates both the data part of the cache and the metadata part
    run(["lvcreate", "-n", "cache_pool", "-l", "100%FREE", vg_name])

    # 6. Convert data_lv to a cached volume
    # 'writethrough' is safer; 'writeback' is faster (true Optane style)
    run(["lvconvert", "--type", "cache", "--cachepool", f"{vg_name}/cache_pool", f"{vg_name}/data_lv"])

    print("\n🚀 Success! Your 'Fenbonce' volume is ready.")
    print(f"Device: /dev/{vg_name}/data_lv")
    print("Format this device with your preferred filesystem (e.g., xfs or ext4).")

def main():
    if os.geteuid() != 0:
        print("This tool must be run as root (sudo).")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Fenbonce: Hardware acceleration for slow storage.")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a cached volume")
    create_parser.add_argument("--storage", required=True, help="The slow storage device or partition (e.g. /dev/sdb or /dev/sdb1)")
    create_parser.add_argument("--cache", required=True, help="The fast cache device or partition (e.g. /dev/nvme0n1 or /dev/nvme0n1p1)")
    create_parser.add_argument("--vg", default="fenbonce_vg", help="Name of the Volume Group")

    args = parser.parse_args()

    if args.command == "create":
        setup_fenbonce(args.storage, args.cache, args.vg)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
