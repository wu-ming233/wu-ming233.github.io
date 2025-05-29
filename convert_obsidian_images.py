import re
import sys
import os
from pathlib import Path

def convert_obsidian_images(text):
    pattern = r'!\\?\[\\?\[([^]]+\.(png|jpg|jpeg|gif|svg|webp))\\?\]\\?\]'
    
    def replace_match(match):
        filename = match.group(1)
        return f'![](/images/{filename})'
    
    converted_text = re.sub(pattern, replace_match, text, flags=re.IGNORECASE)
    return converted_text

def process_file(file_path, output_path=None, in_place=False):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        converted_content = convert_obsidian_images(content)
        
        original_matches = re.findall(r'!\\?\[\\?\[([^]]+\.(png|jpg|jpeg|gif|svg|webp))\\?\]\\?\]', content, re.IGNORECASE)
        num_conversions = len(original_matches)
        
        if in_place:
            output_file = file_path
        elif output_path:
            output_file = output_path
        else:
            path_obj = Path(file_path)
            output_file = path_obj.parent / f"{path_obj.stem}_converted{path_obj.suffix}"
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(converted_content)
        
        print(f"Processed: {file_path}")
        print(f"Output: {output_file}")
        print(f"Conversions made: {num_conversions}")
        
        if num_conversions > 0:
            print("Converted references:")
            for match in original_matches:
                print(f"  !\\[\\[{match[0]}]] -> ![](/images/{match[0]})")
        
        return num_conversions
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return 0
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return 0

def process_directory(directory_path, pattern="*.md", in_place=False):
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' not found.")
        return
    
    files = list(directory.glob(pattern))
    
    if not files:
        print(f"No files matching pattern '{pattern}' found in '{directory_path}'.")
        return
    
    total_conversions = 0
    
    for file_path in files:
        print(f"\n{'='*50}")
        conversions = process_file(str(file_path), in_place=in_place)
        total_conversions += conversions
    
    print(f"\n{'='*50}")
    print(f"Total files processed: {len(files)}")
    print(f"Total conversions made: {total_conversions}")

def main():
    target_path = sys.argv[1]
    in_place = '--in-place' in sys.argv or '-i' in sys.argv
    
    output_path = None
    if '--output' in sys.argv or '-o' in sys.argv:
        try:
            output_index = sys.argv.index('--output') if '--output' in sys.argv else sys.argv.index('-o')
            output_path = sys.argv[output_index + 1]
        except (IndexError, ValueError):
            print("Error: --output option requires a filename.")
            return
    
    pattern = "*.md"
    if '--pattern' in sys.argv or '-p' in sys.argv:
        try:
            pattern_index = sys.argv.index('--pattern') if '--pattern' in sys.argv else sys.argv.index('-p')
            pattern = sys.argv[pattern_index + 1]
        except (IndexError, ValueError):
            print("Error: --pattern option requires a pattern.")
            return
    
    if os.path.isfile(target_path):
        process_file(target_path, output_path, in_place)
    elif os.path.isdir(target_path):
        if output_path:
            print("Warning: --output option ignored for directory processing.")
        process_directory(target_path, pattern, in_place)
    else:
        print(f"Error: '{target_path}' is not a valid file or directory.")

if __name__ == "__main__":
    main() 