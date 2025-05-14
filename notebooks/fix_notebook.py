import json
import os

# Path to the notebook
notebook_path = "Harware_and_Software_Mod_B_Final_Project.ipynb"

try:
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)
    
    # Check if the notebook follows the expected structure
    if 'cells' in notebook_content:
        print(f"Notebook loaded: {len(notebook_content['cells'])} cells found")
        
        # Look for the cells with references to the missing image
        modified = False
        for i, cell in enumerate(notebook_content['cells']):
            if cell['cell_type'] == 'markdown':
                for j, source in enumerate(cell['source']):
                    if 'Plotting Anomalies.png' in source:
                        # Replace the attachment reference with a note
                        old_line = cell['source'][j]
                        cell['source'][j] = "(Note: Image 'Plotting Anomalies.png' was removed due to missing file)\n"
                        print(f"Replaced reference to missing image in cell {i+1}")
                        modified = True
        
        # Remove the attachment metadata if present
        if 'metadata' in notebook_content and 'attachments' in notebook_content['metadata']:
            if 'Plotting Anomalies.png' in notebook_content['metadata']['attachments']:
                del notebook_content['metadata']['attachments']['Plotting Anomalies.png']
                modified = True
                print("Removed attachment metadata for missing image")
        
        # Save the modified notebook if changes were made
        if modified:
            with open(notebook_path + '.fixed', 'w', encoding='utf-8') as f:
                json.dump(notebook_content, f, indent=2)
            print(f"Modified notebook saved as {notebook_path}.fixed")
            
            # Rename files
            os.rename(notebook_path, notebook_path + '.original')
            os.rename(notebook_path + '.fixed', notebook_path)
            print(f"Original notebook renamed to {notebook_path}.original")
            print(f"Fixed notebook is now the main file: {notebook_path}")
        else:
            print("No references to the missing image found")
    else:
        print("Notebook doesn't have the expected structure (no 'cells' key found)")
        
except json.JSONDecodeError:
    print("Error: The notebook file isn't a valid JSON file.")
except Exception as e:
    print(f"Error: {str(e)}")
