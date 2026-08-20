# File Counter

Simple Python CLI tool to count files recursively in any directory, broken down by extension and size.

## Features

- **Quick file count**: Total number of files with breakdown by extension
- **Size estimates**: See total storage used per file type
- **Configurable depth**: Scan shallow directories or the entire tree
- **No dependencies**: Uses only Python standard library

## Usage

```bash
# Count all files with breakdown by extension
python file-counter.py count -s /path/to/dir [-d depth]

# Show counts and size estimates per extension
python file-counter.py size -s /path/to/dir [-d depth]

# Quick summary with top extensions
python file-counter.py summary -s /path/to/dir [-d depth]
```

### Options

- `-s, --src-dir`: Starting directory to analyze (required)
- `-d, --depth`: Maximum depth to scan (0=unlimited, default=2)

### Examples

```bash
# Simple count of files in downloads folder
python file-counter.py count -s ~/Downloads

# Size breakdown for entire projects folder, deep scan
python file-counter.py size -s ~/projects -d 0

# Quick summary of current directory
python file-counter.py summary -n 10 -d 1 ./current/folder
```

## Command Breakdown

### Count Command

Shows total files and a sorted breakdown by extension. The tool groups:
- `*.py` → Python files
- `*.txt` → Text files  
- `*._no_extension` → Files without extensions
- Extension names shown as-is for common types (`.jpg`, `.png`, etc.)

Output format:
```
Files in /path/to/dir:
Total: 2847

Breakdown by extension:
  *.py                      156
  *.txt                     98
  *.sh                       45
```

### Size Command

Counts files and calculates total storage per extension:

```bash
python file-counter.py size -s ~/projects
```

Shows:
- Extension name
- File count for that type
- Total size (formatted as KB/MB/GB)
- Percentage of total space used (optional)

### Summary Command

Quick overview showing top extensions by both count and size. Useful for spotting large unused files or unexpected file types in your working directories.

## Code Examples

The tool uses `os.walk()` to traverse directories and accumulates stats per extension:

```python
def count_files(source_dir, max_depth=0):
    total_count = 0
    breakdown = {}
    
    for root, dirs, files in os.walk(source_dir):
        # Prune deep folders if limit set
        current_depth = len(root.replace(source_dir, '').split(os.sep))
        if max_depth > 0 and current_depth >= max_depth:
            dirs[:] = []
        
        for f in files:
            key = '*' + ext or '_no_extension'
            breakdown[key] = breakdown.get(key, 0) + 1
    
    return total_count, breakdown
```

Handles permission errors gracefully by skipping inaccessible files. Extensions without a suffix are grouped as `No Extension` for readability.

## Why Build This?

Before committing to Git or cleaning up storage, you often want to know "How many files and what size?" — especially by extension type. This tool provides instant answers without heavy dependencies on `find`, `du`, or external utilities. Perfect for auditing your projects folder before repository creation.

If you find this useful, you can support development: https://www.buymeacoffee.com/poolion