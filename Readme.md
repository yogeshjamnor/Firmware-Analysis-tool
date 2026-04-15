# 🛡️ Firmware Analysis Tool

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PySide6](https://img.shields.io/badge/UI-PySide6-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A high-performance desktop toolkit built with **PySide6** for extracting, mounting, and analyzing Android/Linux firmware images — specifically `payload.bin` and `super.img`.

Designed for developers, reverse engineers, and system analysts who need **safe, read-only firmware inspection**.

---

## 🚀 Features

### 🔍 Firmware Processing

* Extract `payload.bin` and `super.img`
* Convert firmware into multiple `.img` partitions
* Supports dynamic partition layouts

### 📦 Extraction Engine

* Uses:

  * `payload-dumper-go`
  * `lpunpack`
* Outputs raw `.img` files and filesystem data

### 🗂️ Mounting System

* Mount partitions using system `mount`
* Secure **sudo password input dialog**
* Enforced **read-only mode**

### 📁 Workspace Output

All outputs stored in:

```
workspace/
```

Includes:

* Extracted `.img` files
* Mounted filesystem
* Optional `.zip` exports

### 🧪 Analysis Engine

* Upload extracted raw files
* Run custom read-only commands
* Export results as `.txt`

---

## ⚡ Quick Start (One Command)

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python main.py
```

---

## 🛠️ Manual Setup

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
```

### 2. Activate Environment

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python main.py
```

---

## 🧩 System Dependencies

### Ubuntu / Debian / kali working 

```bash
sudo apt update && sudo apt install util-linux tar -y
```

### Fedora

```bash
sudo dnf install util-linux tar
```

---

## 🔄 Workflow

1. Load firmware (`payload.bin` / `super.img`)
2. Extract into `.img` partitions
3. Mount partitions (sudo required)
4. Browse filesystem / export data
5. Run read-only analysis → `.txt` output

---

## 📁 Project Structure

```
.
├── bin/            # External binaries (lpunpack, payload-dumper-go)
├── core/           # Backend logic
├── ui/             # PySide6 UI
├── workspace/      # Output directory
├── icon.png
├── main.py
├── requirements.txt
└── README.md
```

---

## 🔐 Security

* Read-only mounts only
* No firmware modification
* Controlled command execution
* Sudo required only when necessary

---

## 📌 Use Cases

* Firmware reverse engineering
* Android ROM analysis
* Debugging system partitions
* Security research
* File recovery

---

## ⚠️ Notes

* Linux recommended for full functionality
* Ensure required binaries exist in `bin/`
* Large firmware may need high disk space

---

## 📜 License

MIT License (or specify your license)

---

## ⭐ Support

If you find this useful, consider giving the repo a star ⭐

---
##img

<h2> Extract Payload.bin/Super.img</h2>
 <img src="/assets/image.png" alt="Profile Banner" width="100%" />
 <h2> mount .img</h2>
 <img src="/assets/mount.png" alt="Profile Banner" width="100%" />
 <h2> analysis any file  .so , libs  read only</h2>
 <img src="/assets/analysis.png" alt="Profile Banner" width="100%" />
