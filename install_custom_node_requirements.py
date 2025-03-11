#!/usr/bin/env python3
import os
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def install_requirements(custom_nodes_dir):
    """
    Search through top-level folders in the custom_nodes directory,
    check for requirements.txt files, and install requirements if found.
    """
    custom_nodes_path = Path(custom_nodes_dir)
    
    if not custom_nodes_path.exists() or not custom_nodes_path.is_dir():
        logging.error(f"Custom nodes directory not found: {custom_nodes_dir}")
        return
    
    logging.info(f"Scanning {custom_nodes_dir} for requirements.txt files...")
    
    # Get all top-level items in the custom_nodes directory
    for item in custom_nodes_path.iterdir():
        if item.is_dir() and not item.name.startswith('__'):  # Skip __pycache__ and similar directories
            req_file = item / "requirements.txt"
            
            if req_file.exists():
                folder_name = item.name
                logging.info(f"Found requirements.txt in {folder_name}")
                
                try:
                    logging.info(f"Installing requirements for {folder_name}...")
                    result = subprocess.run(
                        ["uv", "add", "-r", req_file],
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    
                    if result.returncode == 0:
                        logging.info(f"Successfully installed requirements for {folder_name}")
                    else:
                        logging.error(f"Failed to install requirements for {folder_name}")
                        logging.error(f"Error: {result.stderr}")
                        
                except Exception as e:
                    logging.error(f"Error installing requirements for {folder_name}: {e}")
            else:
                logging.info(f"No requirements.txt found in {folder_name}")

if __name__ == "__main__":
    custom_nodes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_nodes")
    install_requirements(custom_nodes_dir)
    logging.info("Finished processing all custom node directories")