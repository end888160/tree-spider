# Tree Spider - Directory Snapshot Tool

## Description

Tree Spider is a Python script that generates a snapshot of a drive's folder structure and saves it as a compressed JSON file (.bz2). It efficiently scans directories using multithreading and provides metadata such as file attributes, MIME types, timestamps, and more.

## Requirements

- Python 3.6 or higher

- You can alos use Google Magika for more accurate MIME detection: `pip install magika`

## Installation

1. Clone this repository or download the script:

```sh
git clone https://github.com/end888160/tree-spider.git
cd tree-spider
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```sh
python tree_util_spider_thread.py
```

By default, it scans the current directory and saves the snapshot to `folder_structure.json.bz2`.

### Command-line Options

You can customize the behavior using the following options:

- `--scan <directory>`: Specify the directory to scan
- `--output <file>`: Specify the output file name
- `--no-attributes`: Disable file attribute collection
- `--threads`: Enable multithreading for faster scans
- `--force-magic`: Force MIME type detection using `magic`
- `--use-magika`: Use `magika` for MIME detection
- `--browse <file>`: Open the snapshot file

Example:

```sh
python tree_util_spider_thread.py --scan "C:\Users\User" --output snapshot.json.bz2 --threads
```

## Output Structure

The script generates a compressed JSON file containing metadata:

```json
{
  "original_path": "C:/Users/User",
  "total_size": 12345678,
  "scanned_files": 3456,
  "scanned_folders": 567,
  "structure": [
    {
      "name": "Documents",
      "path": "C:/Users/User/Documents",
      "type": "folder",
      "size": 56789,
      "children": [
        {
          "name": "file.txt",
          "path": "C:/Users/User/Documents/file.txt",
          "type": "file",
          "size": 1234,
          "mime": "text/plain"
        }
      ]
    }
  ]
}
```

## Browsing Commands

- `/sort <key>`: Sort the tree by the specified key (e.g., `name`, `size`, `type`)
- `/filter <key> <value>`: Filter the tree by the specified key and value

## License

This project is licensed under the MIT License.

## Contributions

Pull requests are welcome! If you encounter any issues, feel free to open an issue or submit improvements.
