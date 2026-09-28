# Fenbonce 🚀

**Fenbonce** is a high-performance storage acceleration utility designed to bridge the gap between slow bulk storage (HDDs/SATA SSDs) and fast memory (NVMe/Optane). 

By utilizing the Linux kernel's `dm-cache` (via LVM), Fenbonce bonds a large, slow storage drive with a small, fast cache drive to create a single hybrid volume. The most frequently accessed "hot" data is automatically promoted to the fast cache, while "cold" data stays on the bulk storage.

## ✨ Features
- **Multi-Distro Support**: Official packages for Fedora, Debian/Ubuntu, Arch Linux, and Alpine.
- **Partition Aware**: Can target whole disks or specific partitions.
- **Transparent Acceleration**: Once configured, the OS treats the combined volume as a single high-speed device.
- **Lightweight**: Written in Python, leveraging native Linux LVM tools.

## Installation is as easy as just running a command!

### Fedora
```bash
sudo dnf install fenbonce-1.0-1.fc44.x86_64.rpm
```

### Debian/Ubuntu
```bash
sudo apt install ./fenbonce_1.0_amd64.deb
```

### Arch Linux
```bash
sudo pacman -U fenbonce_arch.pkg.tar.zst
```

### Alpine
```bash
sudo apk add fenbonce_alpine.tar.gz
```

## 🚀 Usage

To create an accelerated volume, identify your storage drive (slow) and your cache drive (fast), then run:

```bash
sudo fenbonce create --storage /dev/sdb --cache /dev/nvme0n1
```

**Example with partitions:**
```bash
sudo fenbonce create --storage /dev/sdb1 --cache /dev/nvme0n1p1
```

After creation, your new volume will be available at:
`/dev/fenbonce_vg/data_lv`

Format this volume with your preferred filesystem (e.g., XFS or ext4) and mount it!

## ⚙️ How it Works
Fenbonce orchestrates the following LVM pipeline:
1. **PV Creation**: Initializes the storage and cache devices as Physical Volumes.
2. **VG Setup**: Creates a Volume Group (`fenbonce_vg`).
3. **Data Allocation**: Creates a large Logical Volume for bulk data.
4. **Cache Pooling**: Sets up a cache pool on the fast device.
5. **Binding**: Converts the data volume into a cached volume using `lvconvert`.

## 📜 License
MIT
