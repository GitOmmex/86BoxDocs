import os
import re

def convert_txt_to_md(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    title = ""
    history = ""
    notes = []
    general_info = {}

    current_section = None

    for line in lines:
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1].lower()
            continue

        if current_section is None and line.startswith('['):
            match = re.match(r'\[(.*?)\]\s+(.*)', line)
            if match:
                _, title = match.groups()
        elif current_section == 'history':
            history = line
        elif current_section == 'notes':
            notes.append(line.lstrip('0123456789. ').strip())
        elif current_section == 'basic details':
            if ':' in line:
                key, value = [s.strip() for s in line.split(':', 1)]
                general_info[key] = value

    # Prepare Markdown content
    md_lines = []

    md_lines.append(f"# {title}")
    md_lines.append(f"The [{title}] was a mostly IBM PC-compatible machine launched in **1986**.\n")

    if notes:
        md_lines.append("## Notes")
        for note in notes:
            md_lines.append(f"- {note}")
        md_lines.append("")

    if general_info:
        md_lines.append("## General Info")
        md_lines.append("| Category | Values | Notes |")
        md_lines.append("| --- | --- | --- |")

        def add_info(category, keys, transform=None):
            values = []
            for key in keys:
                val = general_info.get(key)
                if val:
                    values.append(val)
            if values:
                val_str = '; '.join(values)
                if transform:
                    val_str = transform(val_str)
                md_lines.append(f"| {category} | {val_str} | |")

        add_info("Chipset", ["Chipset"])
        add_info("CPU types", ["Supported CPUs"])
        add_info("FPU", ["FPU"])
        add_info("Memory", ["Minimum RAM", "Maximum RAM"], lambda v: v.replace("Minimum RAM: ", "").replace("Maximum RAM: ", "to "))
        add_info("Floppy Controller", ["Floppy Controller"])
        add_info("Hard Disk Controller", ["Hard Disk Controller"])
        add_info("Floppy Drive Support", ["Floppy Drive Support"])
        add_info("RTC", ["RTC"])
        add_info("Expansion Slots", ["Expansion Slots"])
        add_info("Ports", ["Ports"])
        add_info("Supported OSes", ["Supported OSes"], lambda v: v.replace(", ", "; "))
        md_lines.append("")

    md_lines.append("## Links")

    # Write to .md file
    base_name = os.path.splitext(os.path.basename(txt_file_path))[0]
    md_file_path = f"{base_name}.md"
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(f"Converted: {txt_file_path} -> {md_file_path}")


# Example usage
if __name__ == "__main__":
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    for txt_file in txt_files:
        convert_txt_to_md(txt_file)
