import json
import os
import re

# Path to the notebook
notebook_path = "Harware_and_Software_Mod_B_Final_Project.ipynb"

try:
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_json = f.read()
        
    # Fix potential JSON issues
    # Sometimes VSCode's notebook format causes issues with GitHub rendering
    # Replace the VSCode Cell tags with standard Jupyter notebook format
    notebook_json = re.sub(r'<VSCode.Cell id="([^"]*)" language="markdown">', 
                          r'{"cell_type": "markdown", "metadata": {}, "source": [', 
                          notebook_json)
    
    notebook_json = re.sub(r'<VSCode.Cell id="([^"]*)" language="python">', 
                          r'{"cell_type": "code", "metadata": {}, "source": [', 
                          notebook_json)
    
    notebook_json = re.sub(r'</VSCode.Cell>', r']},', notebook_json)
    
    # Add proper notebook JSON structure
    notebook_json = '{"cells": [' + notebook_json + '], "metadata": {}, "nbformat": 4, "nbformat_minor": 2}'
    
    # Remove trailing comma before closing bracket
    notebook_json = notebook_json.replace(',]}', ']}')
    
    # Fix image paths for GitHub
    notebook_json = notebook_json.replace('images/', 'notebooks/images/')
    
    # Try to parse the JSON to validate it
    notebook_data = json.loads(notebook_json)
    
    # Write the fixed notebook
    with open("Harware_and_Software_Mod_B_Final_Project.github.ipynb", 'w', encoding='utf-8') as f:
        json.dump(notebook_data, f, indent=2)
        
    print("Successfully converted notebook to GitHub-compatible format")
    
except Exception as e:
    print(f"Error: {str(e)}")
    print("Creating a GitHub-compatible markdown version instead...")
    
    try:
        # If JSON conversion fails, create a markdown file instead
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = f.read()
        
        # Extract markdown content
        markdown_cells = re.findall(r'<VSCode.Cell id="[^"]*" language="markdown">(.*?)</VSCode.Cell>', 
                                   notebook_content, re.DOTALL)
        
        # Extract code cells
        code_cells = re.findall(r'<VSCode.Cell id="[^"]*" language="python">(.*?)</VSCode.Cell>', 
                               notebook_content, re.DOTALL)
        
        # Combine into a single markdown file
        md_content = ""
        
        # Add header
        md_content += "# Hardware and Software for Big Data Mod B Final Project Report\n\n"
        md_content += "## Time Series Analysis on OULAD Dataset\n\n"
        
        # Add markdown cells
        for cell in markdown_cells:
            md_content += cell.strip() + "\n\n"
            
        # Add code cells with proper formatting
        for i, cell in enumerate(code_cells):
            md_content += f"### Code Cell {i+1}\n```python\n{cell.strip()}\n```\n\n"
        
        # Fix image paths
        md_content = md_content.replace('images/', 'notebooks/images/')
        
        # Write the markdown file
        with open("Harware_and_Software_Mod_B_Final_Project.md", 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print("Created GitHub-compatible markdown file")
        
    except Exception as e2:
        print(f"Failed to create markdown file: {str(e2)}")
