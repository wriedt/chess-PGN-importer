import os
import sys
import shutil
import urllib.request
import zipfile

def setup_addon():
    # Define paths
    addon_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(addon_dir, 'temp')
    lib_dir = os.path.join(addon_dir, 'lib')

    # Create necessary directories
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(lib_dir, exist_ok=True)

    # Download python-chess
    chess_url = "https://github.com/niklasf/python-chess/archive/master.zip"
    chess_zip = os.path.join(temp_dir, "python-chess.zip")
    urllib.request.urlretrieve(chess_url, chess_zip)

    # Extract python-chess
    with zipfile.ZipFile(chess_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Move necessary files to lib directory
    chess_dir = os.path.join(temp_dir, "python-chess-master", "chess")
    shutil.move(chess_dir, lib_dir)

    # Clean up temporary files
    shutil.rmtree(temp_dir)

    # Create manifest.json
    manifest = {
        "package": "chess_moves_from_pgn",
        "name": "Chess Moves from PGN Files",
        "mod": 0
    }
    
    import json
    with open(os.path.join(addon_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f)

    print("Setup completed successfully!")

if __name__ == "__main__":
    setup_addon()
