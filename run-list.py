import os

import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog

def add_footer(root):
    # Add footer devices
    devices = ET.SubElement(root, 'Devices')
    for dev_id in [88, 75, 114, 116, 101, 104, 102, 103, 99, 100, 76, 77]:
        ET.SubElement(devices, 'Dev', id=str(dev_id), value="0")
    # Set specific device to 1 as per example
    devices.find('.//Dev[@id="99"]').set('value', '1')

def get_run_number(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".tcn"):
            run_number = int(filename[1:3])
            return run_number
        
    if not run_number:
        print("No .tcn files found in the specified directory.")
        # throw an error
        return

def generate_xlmst_file(directory):
    run_number = get_run_number(directory)
    if not run_number:
        return
    
    output_filename = f"RUN_{run_number:02}.xmlst"
    
    root = ET.Element('List')

        # Create the Rows element with the specified attributes
    rows = ET.SubElement(root, 'Rows', Name=output_filename, Repetitions="1", TL="0", TH="0", TS="0", Criterion="", ThicknessSpoilBoardLeft="15.5", ThicknessSpoilBoardRight="19", ThicknessPodsOnSpoilBoard="150", EnabledSpoilBoardLeft="1", EnabledSpoilBoardRight="1")
    
    # Iterate over files in the specified directory
    for filename in os.listdir(directory):
        print(f"Processing: {filename}")
        if filename.endswith(".tcn"):  # Adjust the condition if you need a different file type
            row = ET.SubElement(rows, 'Row', Index="1", SavedID="3", FileName=filename)

            # Add cells
            ET.SubElement(row, 'Cell', Name="DRAW", DataType="281").text = "0"
            ET.SubElement(row, 'Cell', Name="ESEC", DataType="165").text = "1"
            ET.SubElement(row, 'Cell', Name="NAME", DataType="161").text = os.path.join(directory, filename)
            ET.SubElement(row, 'Cell', Name="REPETITIONS", DataType="164").text = "1"
            ET.SubElement(row, 'Cell', Name="EXECUTED", DataType="288").text = "0"

            # Check if filename ends with 'Z' to change the FIELD value
            if filename.endswith('Z.tcn'):
                field_value = '0'
            else:
                field_value = '6'

            ET.SubElement(row, 'Cell', Name="FIELD", DataType="171").text = field_value
            ET.SubElement(row, 'Cell', Name="ROTATION", DataType="286").text = "1"
            ET.SubElement(row, 'Cell', Name="MIRROR", DataType="284").text = "0"
            ET.SubElement(row, 'Cell', Name="HOOKOPTI", DataType="600").text = "0"
            ET.SubElement(row, 'Cell', Name="LENGTH", DataType="168").text = "520"
            ET.SubElement(row, 'Cell', Name="HEIGHT", DataType="169").text = "166"
            ET.SubElement(row, 'Cell', Name="THICKNESS", DataType="170").text = "43.517"
            ET.SubElement(row, 'Cell', Name="COMMENT", DataType="162").text = ""
            ET.SubElement(row, 'Cell', Name="UNIT", DataType="163").text = "1"
            ET.SubElement(row, 'Cell', Name="HOOK", DataType="282").text = "1"
            ET.SubElement(row, 'Cell', Name="TIME", DataType="223").text = "00:09:08"
            ET.SubElement(row, 'Cell', Name="OFFSET X", DataType="277").text = "6"
            ET.SubElement(row, 'Cell', Name="OFFSET Y", DataType="278").text = "330"
            ET.SubElement(row, 'Cell', Name="OFFSET Z", DataType="279").text = "0"

    add_footer(root)

    # Write to a file
    tree = ET.ElementTree(root)
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)
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

    generate_xlmst_file(directory_path)

if __name__ == "__main__":
    main()