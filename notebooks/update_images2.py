import json
import os
import re
from pathlib import Path

# Path to the notebook
notebook_path = "Harware_and_Software_Mod_B_Final_Project.ipynb"
images_dir = "images"

try:
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)
    
    # Check if the notebook follows the expected structure
    if 'cells' in notebook_content:
        print(f"Notebook loaded: {len(notebook_content['cells'])} cells found")
        
        # Look for the cells with image attachments and update them
        modified = False
        for i, cell in enumerate(notebook_content['cells']):
            if cell['cell_type'] == 'markdown':
                for j, source in enumerate(cell['source']):
                    # Check for markdown image references
                    pattern = r'!\[(.*?)\]\((attachment:(.*?))\)'
                    if re.search(pattern, source):
                        # Replace attachment references with file references
                        new_source = re.sub(
                            pattern,
                            r'![\1](images/\3)',
                            source
                        )
                        cell['source'][j] = new_source
                        modified = True
                        print(f"Updated image reference in cell {i+1}")
                        
                    # Special handling for the 'Plotting Anomalies.png' case
                    if 'Plotting Anomalies.png' in source:
                        # Change to reference an actual image file
                        cell['source'][j] = source.replace(
                            'Plotting Anomalies.png', 
                            'image-placeholder.png'
                        )
                        modified = True
                        print(f"Updated missing 'Plotting Anomalies.png' reference to use placeholder in cell {i+1}")
        
        # Save the modified notebook if changes were made
        if modified:
            with open(notebook_path + '.fixed', 'w', encoding='utf-8') as f:
                json.dump(notebook_content, f, indent=2)
            print(f"Modified notebook saved as {notebook_path}.fixed")
            
            # Rename files
            os.rename(notebook_path, notebook_path + '.bak3')
            os.rename(notebook_path + '.fixed', notebook_path)
            print(f"Original notebook renamed to {notebook_path}.bak3")
            print(f"Fixed notebook is now the main file: {notebook_path}")
        else:
            print("No image references to update were found")
    else:
        print("Notebook doesn't have the expected structure (no 'cells' key found)")
        
except json.JSONDecodeError as e:
    print(f"Error: The notebook file isn't a valid JSON file: {str(e)}")
except Exception as e:
    print(f"Error: {str(e)}")
