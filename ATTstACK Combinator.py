import json
import glob
import os
import re

def select_input_folder():
    folder_list = next(os.walk('.'))[1]
    print(f'Select folder containing your input layers:')
    print(f'0. ..')
    for i in range(len(folder_list)):
        print(f'{i+1}. {folder_list[i]}')

    folder_index = int(input('Folder:'))
    if folder_index > 0:
        folder_path = folder_list[folder_index-1] + "\\"
    else:
        folder_path = ""
    
    # Clear output
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
        
    print(f"Selected folder: \"{folder_path}\"")
    return folder_path

def get_all_input_files(folder_path):
    file_list = glob.glob(folder_path + '*.json')
    return file_list

def select_input_file(folder_path):
    file_list = glob.glob(folder_path + '*.json')
    print(f'Select the file containing your overlay layer:')
    for i in range(len(file_list)):
        print(f'{i+1}. {file_list[i]}')

    file_index = int(input('File:'))
    file_path = file_list[file_index-1]
    return file_path

# Get input files
input_files = get_all_input_files(select_input_folder())

# Read input files into dictionary
input_dict = {}
for input_file in input_files:
    with open(input_file, encoding="utf8") as json_file:
        input_dict[input_file] = json.load(json_file)

# Define output dictionary
output_dict = {}

# Build combined metadata - source file names
metadata_list = []
metadata_dict = {}
metadata_dict['name'] = "Input files:"
metadata_dict['value'] = ""
for input_file_name in input_dict.keys():
    metadata_dict['value'] = metadata_dict['value'] + input_file_name.split("\\")[1] + "; "
metadata_list.append(metadata_dict)

# Build combined metadata - source layer names
metadata_dict = {}
metadata_dict['name'] = "Layers:"
metadata_dict['value'] = ""
for input_layer_item in input_dict.values():
    metadata_dict['value'] = metadata_dict['value'] + input_layer_item['name'] + "; "
metadata_list.append(metadata_dict)
output_dict['metadata'] = metadata_list

# Build versions (get the latest across all layers)
versions_dict = {}
versions_dict['attack'] = "9"
versions_dict['navigator'] = "4.3"
versions_dict['layer'] = "4.2"
for input_layer_item in input_dict.values():
    if int(input_layer_item['versions']['attack']) > int(versions_dict['attack']):
        versions_dict['attack'] = input_layer_item['versions']['attack']
    if float(input_layer_item['versions']['navigator']) > float(versions_dict['navigator']):
        versions_dict['navigator'] = input_layer_item['versions']['navigator']
output_dict['versions'] = versions_dict

# Build other properties
output_dict['selectTechniquesAcrossTactics']: True
output_dict['selectSubtechniquesWithParent']: False
output_dict['domain'] = 'enterprise-attack'
filters_dict = {}
filters_dict['platforms'] = ['Linux', "macOS", "Windows", "Office 365", "Azure AD", "Iaas", "SaaS", "PRE", "Network"]
output_dict['filters'] = filters_dict
output_dict['sorting'] = 3
layout_dict = {}
layout_dict['layout'] = 'side'
layout_dict['showID'] = False
layout_dict['showName'] = True
output_dict['layout'] = layout_dict
output_dict['hideDisabled'] = False

# Build combined layers
combined_techniques = {}
for input_layer_item in input_dict.values():    
    for technique in input_layer_item['techniques']:        
        # Build metadata to append if a technique has a comment
        metadata_to_append = {}
        metadata_list = []
        if "comment" in technique:
            metadata_to_append = {
                'name': input_layer_item['name'].split("(", 1)[0][:-1],
                #'value': technique['comment'].split(")", 1)[1][1:].rsplit(".", 1)[0]
                'value': re.sub(r"\(.*?\)|\[|\]", "", technique['comment'])
                #'value': technique['comment']
            }
            metadata_list.append(metadata_to_append.copy())
        
        # If the technique is seen for the first time
        if (technique['techniqueID']) not in combined_techniques.keys():
            combined_techniques[technique['techniqueID']] = {
                "techniqueID": technique['techniqueID'],
                "score": 1,
                "color": "",
                "comment": "Used by: " + input_layer_item['name'],
                "enabled": True,
                "metadata": metadata_list,
                #"showSubtechniques": technique['showSubtechniques']
                "showSubtechniques": False
            }
        # If the technique is already in a combined layer, and needs to be appended
        else:
            # if existing technique has metadata
            original_metadata = (combined_techniques[technique['techniqueID']]['metadata']).copy()
            if 'value' in metadata_to_append and metadata_to_append['value']:
                original_metadata.extend(metadata_list)            
            combined_techniques[technique['techniqueID']] = {
                "techniqueID": technique['techniqueID'],
                "score": combined_techniques[technique['techniqueID']]['score'] + 1,
                "color": "",
                "comment": combined_techniques[technique['techniqueID']]['comment'] + "; " + input_layer_item['name'],
                "enabled": True,
                "metadata": original_metadata,
                #"showSubtechniques": technique['showSubtechniques']
                "showSubtechniques": False
            }
output_techniques = []

# Get the maximum score for the correct color gradient
max_score = 1
for value in combined_techniques.values():        
    output_techniques.append(value)
    if value['score'] > max_score:
        max_score = value['score']

output_dict['techniques'] = output_techniques

# Build colors
color_dict = {}
color_dict['colors'] = ['#8ec843', '#ffe766', '#ff6666']
color_dict['minValue'] = 1
color_dict['maxValue'] = max_score
output_dict['gradient'] = color_dict

# Name the output

output_dict['name'] = str(input("Name for the resulting layer: "))
output_dict['description'] = str(input("Description for the resulting layer: "))
            
#print(json.dumps(output_dict, indent=3, sort_keys=False))
with open(output_dict['name'] + '.json', 'w') as outfile:
    json.dump(output_dict, outfile, indent=4)

print(f"Combined layer output into \"{output_dict['name'] + '.json'}\"")