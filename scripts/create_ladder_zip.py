import zipfile
import os

def create_zip(zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            for file in files:
                zipf.write(os.path.join(root, file))

if __name__ == "__main__":
    zip_filename = "my_project.zip"
    create_zip(zip_filename)
