import zipfile
import os

def create_zip():
    zip_path = os.path.join(os.path.dirname(__file__), 'Q1_Submission.zip')
    base_dir = os.path.dirname(__file__)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add main.tex
        tex_path = os.path.join(base_dir, 'main.tex')
        if os.path.exists(tex_path):
            zipf.write(tex_path, arcname='main.tex')
            print("Added main.tex to zip")
            
        # Add plots
        plots_dir = os.path.join(base_dir, 'plots')
        if os.path.exists(plots_dir):
            for filename in os.listdir(plots_dir):
                if filename.endswith('.png'):
                    file_path = os.path.join(plots_dir, filename)
                    arcname = f"plots/{filename}"
                    zipf.write(file_path, arcname=arcname)
                    print(f"Added {arcname} to zip")
                    
    print(f"Successfully created {zip_path}")

if __name__ == '__main__':
    create_zip()
