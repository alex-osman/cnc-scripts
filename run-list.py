import os

import xml.etree.ElementTree as ET
from xml.dom import minidom
from tkinter import Tk, filedialog
import re


real_computer_base_path = "G:\\.shortcut-targets-by-id\\0B3FEOP395MGKbXlxdXdURm1YVjA"
old_base_path = "G:\\My Drive\\Loubier Design"


def replace_path_prefix(filepath, old_prefix, new_prefix):
    # Check if the old prefix is in the filepath
    if old_prefix in filepath:
        # Replace the part before "ACTIVE" with the new prefix
        return filepath.replace(old_prefix, new_prefix, 1)
    return filepath


def extract_dimensions_from_file(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if "::UNm" in line:
                # Use regex to find DL, DH, and DS values
                match = re.search(r'DL=([\d.]+)\s+DH=([\d.]+)\s+DS=([\d.]+)', line)
                if match:
                    length = match.group(1)
                    height = match.group(2)
                    thickness = match.group(3)
                    return length, height, thickness
    # Return None if the line is not found
    return None, None, None

def add_footer(root):
    devices = ET.SubElement(root, 'Devices')
    for dev_id in [88, 75, 114, 116, 101, 104, 102, 103, 99, 100, 76, 77]:
        ET.SubElement(devices, 'Dev', id=str(dev_id), value="0")
    
    devices.find('.//Dev[@id="99"]').set('value', '1')

def generate_xlmst_file(directory):
    filename_input = input("Enter a filename for the output (without extension): ")
    output_filename = os.path.normpath(os.path.join(directory, f"{filename_input}.xmlst"))
    updated_output_filename = replace_path_prefix(output_filename, old_base_path, real_computer_base_path)

    print(f"Output File: {output_filename}")
    
    root = ET.Element('List')

    # Create the Rows element with the specified attributes
    rows = ET.SubElement(root, 'Rows', Name=updated_output_filename, Repetitions="1", TL="0", TH="0", TS="0", Criterion="", ThicknessSpoilBoardLeft="15.5", ThicknessSpoilBoardRight="19", ThicknessPodsOnSpoilBoard="54", EnabledSpoilBoardLeft="1", EnabledSpoilBoardRight="1")
    index = 1

    # Iterate over files in the specified directory
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith(".tcn"):
            print(f"Processing: {filename}")
            # // update the index
            normalized_filename = os.path.normpath(os.path.join(directory, filename))
            updated_filename = replace_path_prefix(normalized_filename, old_base_path, real_computer_base_path)


            row = ET.SubElement(rows, 'Row', Index=str(index), SavedID="13", FileName=updated_filename)
            index += 1

            length, height, thickness = extract_dimensions_from_file(normalized_filename)
            if not length or not height or not thickness:
                print(f"Error: Could not extract dimensions from {filename}. Skipping file.")
                continue

            # Add cells
            ET.SubElement(row, 'Cell', Name="DRAW", DataType="281").text = "1"
            ET.SubElement(row, 'Cell', Name="ESEC", DataType="165").text = "1"
            ET.SubElement(row, 'Cell', Name="NAME", DataType="161").text = updated_filename
            ET.SubElement(row, 'Cell', Name="REPETITIONS", DataType="164").text = "1"
            ET.SubElement(row, 'Cell', Name="EXECUTED", DataType="288").text = "0"

            # Check if filename ends with 'Z' to change the FIELD value
            if filename.lower().endswith('z.tcn'):
                field_value = '1'
            else:
                field_value = '7'

            ET.SubElement(row, 'Cell', Name="FIELD", DataType="171").text = field_value
            ET.SubElement(row, 'Cell', Name="ROTATION", DataType="286").text = "1"
            ET.SubElement(row, 'Cell', Name="MIRROR", DataType="284").text = "0"
            ET.SubElement(row, 'Cell', Name="HOOKOPTI", DataType="600").text = "0"
            
            # genrerate from the inside of each file
            # L/H/Width or thickness is S 
            ET.SubElement(row, 'Cell', Name="LENGTH", DataType="168").text = length
            ET.SubElement(row, 'Cell', Name="HEIGHT", DataType="169").text = height
            ET.SubElement(row, 'Cell', Name="THICKNESS", DataType="170").text = thickness
            
            ET.SubElement(row, 'Cell', Name="COMMENT", DataType="162").text = ""
            ET.SubElement(row, 'Cell', Name="UNIT", DataType="163").text = "1"
            ET.SubElement(row, 'Cell', Name="HOOK", DataType="282").text = "0"
            ET.SubElement(row, 'Cell', Name="TIME", DataType="223").text = "00:00:00"
            ET.SubElement(row, 'Cell', Name="OFFSET X", DataType="277").text = "0"
            ET.SubElement(row, 'Cell', Name="OFFSET Y", DataType="278").text = "0"
            ET.SubElement(row, 'Cell', Name="OFFSET Z", DataType="279").text = "0"

    ET.SubElement(root, 'Bench', Row="0")
    add_footer(root)

     # Convert the ElementTree to a string and pretty-print it
    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

    # Write the pretty XML to a file in the selected directory
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)

    print(f"Generated file: {output_filename}")

    

def select_directory():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Directory")
    return directory

def main():
    directory_path = select_directory()
    if not directory_path:
        print("No directory selected.")
        return
    
    print(f"Selected Directory")

    generate_xlmst_file(directory_path)

if __name__ == "__main__":
    main()