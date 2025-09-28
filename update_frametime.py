#!/usr/bin/env python3
"""
Script to update frametime values in Minecraft .mcmeta files to 18.
This script searches for all .mcmeta files in the resource pack and updates
the frametime value in the animation object to 18.
"""

import os
import json
import glob
from pathlib import Path


def update_frametime_in_file(file_path, new_frametime=18):
    """
    Update the frametime value in a single .mcmeta file.
    
    Args:
        file_path (str): Path to the .mcmeta file
        new_frametime (int): New frametime value (default: 18)
    
    Returns:
        bool: True if file was updated, False if no changes were needed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if the file has animation data
        if 'animation' in data and 'frametime' in data['animation']:
            old_frametime = data['animation']['frametime']
            
            # Only update if the frametime is different
            if old_frametime != new_frametime:
                data['animation']['frametime'] = new_frametime
                
                # Write back to file with proper formatting
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                print(f"Updated {file_path}: {old_frametime} → {new_frametime}")
                return True
            else:
                print(f"Skipped {file_path}: already has frametime {new_frametime}")
                return False
        else:
            print(f"Skipped {file_path}: no animation/frametime found")
            return False
            
    except json.JSONDecodeError as e:
        print(f"Error reading JSON from {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def find_mcmeta_files(root_dir="."):
    """
    Find all .mcmeta files in the given directory and subdirectories.
    
    Args:
        root_dir (str): Root directory to search (default: current directory)
    
    Returns:
        list: List of paths to .mcmeta files
    """
    mcmeta_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.mcmeta'):
                mcmeta_files.append(os.path.join(root, file))
    return mcmeta_files


def main():
    """Main function to update all .mcmeta files."""
    print("RGB Texture Pack - Frametime Updater")
    print("=" * 40)
    
    # Find the script directory (where this script is located)
    script_dir = Path(__file__).parent.absolute()
    print(f"Working directory: {script_dir}")
    
    # Find all .mcmeta files
    mcmeta_files = find_mcmeta_files(script_dir)
    
    if not mcmeta_files:
        print("No .mcmeta files found!")
        return
    
    print(f"Found {len(mcmeta_files)} .mcmeta files:")
    for file in mcmeta_files:
        print(f"  - {os.path.relpath(file, script_dir)}")
    
    print("\nProcessing files...")
    print("-" * 40)
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    # Process each file
    for file_path in mcmeta_files:
        try:
            if update_frametime_in_file(file_path, 18):
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 40)
    print("SUMMARY:")
    print(f"  Files updated: {updated_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total processed: {len(mcmeta_files)}")
    
    if updated_count > 0:
        print(f"\n✅ Successfully updated frametime to 18 in {updated_count} files!")
    else:
        print("\nℹ️  No files needed updating.")


if __name__ == "__main__":
    main()