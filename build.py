import os
import shutil

def main():
    # Ask user for input
    extension_name = input("Extension name: ")
    extension_author = input("Extension Author: ")
    extension_version = input("Extension Version: ")
    extension_description = input("Extension Description: ")
    extension_dependencies = input("Extension Dependencies (separate with commas): ")
    path = input("Path To Create extensions in (leave blank for current directory): ")

    # Set up the directory
    directory = f"com.psc.{extension_name}"
    if path:
        directory = os.path.join(path, directory)
        os.makedirs(directory, exist_ok=True)
    else:
        directory = os.path.join("src", directory)
        os.makedirs(directory, exist_ok=True)
    
    if extension_dependencies:
        extension_dependencies = ", ".join([f'"{dependency}"' for dependency in extension_dependencies.split(",")])
    else:
        extension_dependencies = "numpy", "opencv-python"
    # Create and write to manifest.py
    manifest_content = f"""from PyShiftCore import *   

def main():
    manifest = Manifest()
    manifest.name = "{extension_name}"
    manifest.version = "{extension_version}"
    manifest.description = "{extension_description}"
    manifest.author = "{extension_author}"
    manifest.dependencies = [{extension_dependencies}]
    return manifest

if __name__ == "__main__":
    manifest = main()
"""
    with open(os.path.join(directory, "manifest.py"), "w") as file:
        file.write(manifest_content)

    # Create and write to entry.py
    entry_content = """from PyShiftCore import *
    
def display_alert(message: str) -> None:
    app = App() # Get the current After Effects application
    app.reportInfo(message) # Send a message to the user
    return None  # Not necessary. If calling from JS, can return anything(?).

def search_project_folder_by_name(name: str) -> Item:
    app = App()  # Get the current After Effects application
    project = app.project  # Get the current After Effects project
    for item in project.items:  # Loop through the items in the current After Effects project
        if item.name == name:  # If the item's name matches the name we're looking for
            return item  # Return the item
        if isinstance(item, FolderItem):  # If the item is a folder
            for child in item.children:  # Loop through the children of the folder
                if child.name == name:  # If the child's name matches the name we're looking for
                    return child  # Return the child
    return None   
"""
    with open(os.path.join(directory, "entry.py"), "w") as file:
        file.write(entry_content)
        
    shutil.copy("PyShiftCore.pyi", directory)      # Copy PyShiftCore.pyi file
    
    print(f"Setup completed. Extension '{extension_name}' created in '{directory}'.")

if __name__ == "__main__":
    main()
