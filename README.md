# automation-tool-60

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

automation-tool-60 is a Python CLI tool that automates repetitive file and system tasks to improve productivity. It provides a simple interface for creating and running automated workflows without complex scripting.

## Features
- Rule-based file organization that sorts files by type, date, or custom patterns
- Incremental backups with compression and versioning for local directories
- Disk usage monitoring with threshold alerts and automated cleanup suggestions
- Support for running user-defined Python scripts on schedules or file events

## Installation

```bash
git clone https://github.com/Developer/automation-tool-60.git
cd automation-tool-60
pip install -r requirements.txt
pip install -e .
```

## Usage

Organize files in a directory:

```bash
automation-tool-60 organize --source ~/Downloads --rules rules.yaml
```

Run a backup task:

```bash
automation-tool-60 backup --source ~/Projects --dest /mnt/backup
```

For all available commands:

```bash
automation-tool-60 --help
```