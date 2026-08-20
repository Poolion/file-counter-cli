#!/usr/bin/env python3
"""File Counter - Count files and estimate size by extension recursively."""

import sys
import os


def count_files(source_dir, max_depth=0):
    """Count files in a directory, returning breakdown by extension."""
    total_count = 0
    breakdown = {}

    for root, dirs, files in os.walk(source_dir):
        current_depth = len(root.replace(source_dir, '').split(os.sep))
        if max_depth > 0 and current_depth >= max_depth:
            dirs[:] = []

        for f in files:
            fp = os.path.join(root, f)
            try:
                if not os.path.isfile(fp):
                    continue

                ext = os.path.splitext(f)[1].lower() or ''
                
                # Create display key
                if ext:
                    key = '*' + ext
                else:
                    key = '_no_extension'

                total_count += 1
                breakdown[key] = breakdown.get(key, 0) + 1

            except (OSError, IOError):
                continue

    return total_count, breakdown


def get_directories_and_sizes(source_dir, max_depth=0):
    """Walk directory and collect per-directory stats."""
    results = []

    for root, dirs, files in os.walk(source_dir):
        current_depth = len(root.replace(source_dir, '').split(os.sep))
        
        # Prune deep folders
        if max_depth > 0 and current_depth >= max_depth:
            dirs[:] = []
            continue

        dir_count = len(files)
        dir_size = 0
        
        for f in files:
            fp = os.path.join(root, f)
            try:
                ext = os.path.splitext(f)[1].lower() or ''
                if ext:
                    key = '*' + ext
                else:
                    key = '_no_extension'
                
                size = os.path.getsize(fp)
                dir_size += size
                
                # Update breakdown for this directory level
                results.append({
                    'path': root,
                    'count': dir_count,
                    'size': dir_size,
                    'depth': current_depth
                })
            except (OSError, IOError):
                continue

    return results


def format_size(size_bytes):
    """Format bytes as human-readable."""
    if size_bytes >= 1e12:
        return f"{size_bytes / 1e12:.1f} TB"
    elif size_bytes >= 1e9:
        return f"{size_bytes / 1e9:.1f} GB"
    elif size_bytes >= 1e6:
        return f"{size_bytes / 1e6:.1f} MB"
    elif size_bytes >= 1e3:
        return f"{size_bytes / 1e3:.1f} KB"
    else:
        return f"{size_bytes:.0f} bytes"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Count files and estimate size by extension.')

    subparsers = parser.add_subparsers(dest='command')

    # Count command - simple file count with breakdown
    p_count = subparsers.add_parser('count', help='Count files by extension')
    p_count.add_argument('-s', '--src-dir', required=True, type=str,
                         help='Starting directory to scan')
    p_count.add_argument('-d', '--depth', type=int, default=0,
                         help='Max depth (0=unlimited)')

    # Size command - count files and show size estimates per extension
    p_size = subparsers.add_parser('size',
                                    help='Show file counts with size totals by extension')
    p_size.add_argument('-s', '--src-dir', required=True, type=str,
                        help='Starting directory to scan')
    p_size.add_argument('-d', '--depth', type=int, default=0)

    # Summary command - quick stat: total files, total size, top extensions
    p_summary = subparsers.add_parser('summary', help='Quick summary stats')
    p_summary.add_argument('-s', '--src-dir', required=True, type=str,
                           help='Starting directory to scan')
    p_summary.add_argument('-d', '--depth', type=int, default=0)

    args = parser.parse_args()

    if not hasattr(args, 'command'):
        print("Usage: file-counter.py <count|size|summary> -s <dir>")
        sys.exit(1)

    command = args.command
    src_dir = getattr(args, 'src_dir', '.')
    max_depth = getattr(args, 'depth', 0)

    if not os.path.isdir(src_dir):
        print(f"Error: Directory does not exist: {src_dir}")
        sys.exit(1)

    total_count, breakdown = count_files(src_dir, max_depth=max_depth)

    # Calculate extension sizes
    ext_sizes = {}
    for root, dirs, files in os.walk(src_dir):
        current_depth = len(root.replace(src_dir, '').split(os.sep))
        if max_depth > 0 and current_depth >= max_depth:
            continue
        for f in files:
            fp = os.path.join(root, f)
            try:
                ext = os.path.splitext(f)[1].lower() or ''
                key = '*' + ext if ext else '_no_extension'
                size = os.path.getsize(fp)
                ext_sizes[key] = ext_sizes.get(key, 0) + size
            except (OSError, IOError):
                continue

    print(f"\nFile Counter for: {src_dir}")
    
    # Show counts
    if command == 'count' or command == 'summary':
        print(f"Total files: {total_count}")
        print("\nBreakdown by extension:")
        sorted_exts = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_exts[:20]:  # Top 20
            display_name = ext.replace('*', '').replace('_no_extension', 'No Extension')
            print(f"  {ext:<35} {count:>6}")

    if command == 'size' or command == 'summary':
        total_size = sum(ext_sizes.values())
        print(f"\nTotal size: {format_size(total_size)}")
        
        print("\nSize by extension:")
        for key, size in sorted(ext_sizes.items(), key=lambda x: x[1], reverse=True):
            if key != '_no_extension':
                display_name = ext.replace('*', '', '').replace('_no_extension', 'No Extension')
            else:
                display_name = 'No Extension'
            
            pct = f"{size / total_size * 100:.1f}%" if total_size > 0 else ''
            print(f"  {display_name:<35} {format_size(size):>10} {pct}")


if __name__ == '__main__':
    main()