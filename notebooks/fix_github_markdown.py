import json
import os
import re

# Path to the notebook
notebook_path = "Harware_and_Software_Mod_B_Final_Project.ipynb"

try:
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)
    
    # Check if the notebook follows the expected structure
    if 'cells' in notebook_content:
        print(f"Notebook loaded: {len(notebook_content['cells'])} cells found")
        
        # Look for markdown cells and improve their formatting for GitHub
        modified = False
        for i, cell in enumerate(notebook_content['cells']):
            if cell['cell_type'] == 'markdown':
                for j, source in enumerate(cell['source']):
                    # Fix any image references to use relative paths correctly
                    if "images/" in source:
                        new_source = source.replace(
                            "images/", 
                            "notebooks/images/"
                        )
                        cell['source'][j] = new_source
                        modified = True
                        print(f"Updated image path in cell {i+1}")
                    
                    # Ensure proper line breaks between headers and content
                    if re.match(r'^#+\s+', source) and j < len(cell['source']) - 1:
                        if not cell['source'][j+1].strip() == '':
                            cell['source'].insert(j+1, '\n')
                            modified = True
                            print(f"Added line break after header in cell {i+1}")
                    
                    # Fix double asterisks formatting (bold text)
                    if '****' in source:  # Check for potentially malformed bold text
                        new_source = source.replace('****', '**')
                        if new_source != source:
                            cell['source'][j] = new_source
                            modified = True
                            print(f"Fixed bold formatting in cell {i+1}")
                    
                    # Ensure code blocks have proper syntax
                    if '```' in source and not ('```python' in source or '```bash' in source or '```r' in source):
                        # Check if it could be a python code block without language specification
                        if re.search(r'```\s*\n\s*[a-z0-9_.]+=|import\s|def\s|class\s|print\(', source, re.IGNORECASE):
                            new_source = source.replace('```', '```python', 1)
                            cell['source'][j] = new_source
                            modified = True
                            print(f"Added language specification to code block in cell {i+1}")
        
        # Save the modified notebook if changes were made
        if modified:
            with open(notebook_path + '.github', 'w', encoding='utf-8') as f:
                json.dump(notebook_content, f, indent=2)
            print(f"Modified notebook saved as {notebook_path}.github")
            
            # Rename files
            os.rename(notebook_path, notebook_path + '.prebak')
            os.rename(notebook_path + '.github', notebook_path)
            print(f"Original notebook renamed to {notebook_path}.prebak")
            print(f"GitHub-optimized notebook is now the main file: {notebook_path}")
        else:
            print("No markdown formatting issues were found")
    else:
        print("Notebook doesn't have the expected structure (no 'cells' key found)")
        
except json.JSONDecodeError as e:
    print(f"Error: The notebook file isn't a valid JSON file: {str(e)}")
except Exception as e:
    print(f"Error: {str(e)}")
