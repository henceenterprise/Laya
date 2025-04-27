import os
import zipfile
from datetime import datetime
import gitignore_parser

class ProjectExporter:
    @staticmethod
    def export_project(folder_path: str) -> str:
        """
        Export the selected folder into a .zip file, respecting .gitignore rules.
        Returns the created .zip file path.
        """
        if not os.path.isdir(folder_path):
            raise ValueError("The selected path is not a valid folder.")

        gitignore_path = os.path.join(folder_path, '.gitignore')
        if not os.path.isfile(gitignore_path):
            raise FileNotFoundError("No .gitignore file found in the selected folder.")

        # Parse the .gitignore
        matches = gitignore_parser.parse_gitignore(gitignore_path)

        # Create the .zip file name
        folder_name = os.path.basename(folder_path.rstrip('/\\'))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        zip_filename = f"{folder_name}_export_{timestamp}.zip"

        # ZIP will be created outside the project folder
        parent_folder = os.path.dirname(folder_path)
        zip_path = os.path.join(parent_folder, zip_filename)

        # Create the .zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                # Filter directories to exclude ignored ones
                dirs[:] = [d for d in dirs if not matches(os.path.relpath(os.path.join(root, d), folder_path).replace("\\", "/"))]

                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path).replace("\\", "/")

                    if not matches(relative_path) and relative_path != zip_filename:
                        zipf.write(file_path, arcname=relative_path)

        return zip_path
