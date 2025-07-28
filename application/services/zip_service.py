import os
import zipfile
import shutil

class ZipService:
    def __init__(self, export_dir: str = "./exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def compress_folder(self, folder_path: str) -> str:
        base_name = os.path.basename(folder_path)
        zip_name = base_name + ".zip"
        temp_zip_path = folder_path + ".zip"
        
        with zipfile.ZipFile(temp_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=os.path.dirname(folder_path))
                    zipf.write(full_path, arcname)

        # Remove folder after compression
        shutil.rmtree(folder_path)

        # Move to exports/
        final_path = os.path.join(self.export_dir, zip_name)
        shutil.move(temp_zip_path, final_path)
        print(f"📦 ZIP moved to: {final_path}")
        return final_path