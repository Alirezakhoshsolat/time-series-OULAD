import re
import os

# Path to the notebook
notebook_path = "Harware_and_Software_Mod_B_Final_Project.ipynb"
backup_path = "Harware_and_Software_Mod_B_Final_Project.ipynb.img_backup"

# Create a backup of the original file
os.system(f'copy "{notebook_path}" "{backup_path}"')

# Read the notebook content
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook_content = f.read()

# Function to remove image references from markdown cell content
def remove_image_references(markdown_content):
    # Remove markdown image syntax: ![alt text](image_path)
    cleaned_content = re.sub(r'!\[.*?\]\(.*?\)', '', markdown_content)
    
    # Remove HTML image tags: <img src="..." />
    cleaned_content = re.sub(r'<img\s+[^>]*?src\s*=\s*["\'].*?["\'][^>]*?>', '', cleaned_content)
    
    # Remove references to "Plotting Anomalies.png" or other specific image references
    cleaned_content = re.sub(r'Plotting Anomalies\.png', 'output plots', cleaned_content)
    cleaned_content = re.sub(r'image-\d+\.png', 'output plots', cleaned_content)
    
    return cleaned_content

# Find all markdown cells and clean their content
# Pattern matches <VSCode.Cell id="XXXX" language="markdown">content</VSCode.Cell>
pattern = r'(<VSCode\.Cell id="[^"]*" language="markdown">)(.*?)(<\/VSCode\.Cell>)'

def replace_match(match):
    cell_start = match.group(1)
    content = match.group(2)
    cell_end = match.group(3)
    
    # Clean the content while keeping plot references
    cleaned_content = remove_image_references(content)
    
    return cell_start + cleaned_content + cell_end

# Replace image references in markdown cells
modified_content = re.sub(pattern, replace_match, notebook_content, flags=re.DOTALL)

# Write the modified notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print(f"Image references removed from {notebook_path}")
print(f"Original notebook backed up as {backup_path}")