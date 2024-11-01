# Updates - L/H/Thickness from each file, indicies need to increment, error if not all the same

# 3rd line has l/w/thickness

import os

import xml.etree.ElementTree as ET
from xml.dom import minidom
from tkinter import Tk, filedialog


def add_footer(root):
    devices = ET.SubElement(root, 'Devices')
    for dev_id in [88, 75, 114, 116, 101, 104, 102, 103, 99, 100, 76, 77]:
        ET.SubElement(devices, 'Dev', id=str(dev_id), value="0")
    
    devices.find('.//Dev[@id="99"]').set('value', '1')

def generate_xlmst_file(directory):
    filename_input = input("Enter a filename for the output (without extension): ")
    output_filename = os.path.normpath(os.path.join(directory, f"{filename_input}.xmlst"))

    print(f"Output File: {output_filename}")
    
    root = ET.Element('List')

        # Create the Rows element with the specified attributes
    rows = ET.SubElement(root, 'Rows', Name=filename_input, Repetitions="1", TL="0", TH="0", TS="0", Criterion="", ThicknessSpoilBoardLeft="15.5", ThicknessSpoilBoardRight="19", ThicknessPodsOnSpoilBoard="54", EnabledSpoilBoardLeft="1", EnabledSpoilBoardRight="1")
    index = 1

    # Iterate over files in the specified directory
    for filename in os.listdir(directory):
        print(f"Processing: {filename}")
        if filename.lower().endswith(".tcn"):
            # // update the index
            normalized_filename = os.path.normpath(os.path.join(directory, filename))
            # print the original and normalized filename
            print(f"Original: {filename}")
            print(f"Normalized: {normalized_filename}")

            row = ET.SubElement(rows, 'Row', Index=str(index), SavedID="13", FileName=normalized_filename)
            index += 1

            # Add cells
            ET.SubElement(row, 'Cell', Name="DRAW", DataType="281").text = "1"
            ET.SubElement(row, 'Cell', Name="ESEC", DataType="165").text = "1"
            ET.SubElement(row, 'Cell', Name="NAME", DataType="161").text = normalized_filename
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
            ET.SubElement(row, 'Cell', Name="LENGTH", DataType="168").text = "2451.1"
            ET.SubElement(row, 'Cell', Name="HEIGHT", DataType="169").text = "1231.9"
            ET.SubElement(row, 'Cell', Name="THICKNESS", DataType="170").text = "18.5"
            
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