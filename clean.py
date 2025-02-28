import os
import shutil
import logging

# 🔹 Set up logging to track moved files
# This log file helps users keep track of all file movements, making it easier to reverse changes.
logging.basicConfig(filename="file_cleaner.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def create_subfolder_if_needed(folder_path, subfolder_name):
    """
    Creates a subfolder in the specified path if it doesn't already exist.
    
    Why? Ensures that files are sorted into organized categories, reducing clutter.
    """
    subfolder_path = os.path.join(folder_path, subfolder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)  # Efficiently creates the folder if missing.
    return subfolder_path

def move_file_to_subfolder(file_path, subfolder_path):
    """
    Moves a file to the specified subfolder and logs the movement.

    Why? Logging enhances traceability, allowing users to track which files were moved and their original locations.
    """
    file_size = os.path.getsize(file_path)  # Get file size in bytes
    shutil.move(file_path, subfolder_path)  # Moves the file efficiently
    logging.info(f"Moved: {os.path.basename(file_path)} → {subfolder_path}/ (Size: {file_size} bytes)")
    print(f"✅ Moved: {os.path.basename(file_path)} → {subfolder_path}/ (Size: {file_size} bytes)")

def clean_folder(folder_path):
    """
    Organizes files in the specified folder into subfolders based on file type.

    Why? This improves accessibility, making it easier to find files by grouping them into relevant categories.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):  # Ensure it's a file and not a folder
            file_extension = filename.split('.')[-1].lower()  # Extract file extension
            if file_extension:  # Only process files that have an extension
                subfolder_name = f"{file_extension.upper()} Files"
                subfolder_path = create_subfolder_if_needed(folder_path, subfolder_name)
                move_file_to_subfolder(file_path, subfolder_path)

def undo_last_clean():
    """
    Moves files back to their original folder using the log file.

    Why? The undo feature ensures that users can recover their files if needed, enhancing the script's usability.
    """
    if not os.path.exists("file_cleaner.log"):  # Ensure the log file exists before attempting undo
        print("❌ No log file found. Cannot undo.")
        return

    with open("file_cleaner.log", "r") as log_file:
        lines = log_file.readlines()

    # Undo operations in reverse order to maintain original file structure
    for line in reversed(lines):
        if "Moved:" in line:
            parts = line.strip().split(" → ")
            filename = parts[0].split(": ")[1]  # Extract file name
            subfolder = parts[1].split("/")[0]  # Extract destination folder name

            original_path = os.path.join(folder_path, filename)
            subfolder_path = os.path.join(folder_path, subfolder)

            # Ensure the file exists before attempting to move it back
            if os.path.exists(os.path.join(subfolder_path, filename)):
                shutil.move(os.path.join(subfolder_path, filename), original_path)
                print(f"🔄 Restored: {filename} → {folder_path}")
            else:
                print(f"⚠️ File {filename} not found in {subfolder_path}. Skipping...")

    print("🔄 Undo complete.")

if __name__ == "__main__":
    print("📂 Desktop Cleaner Script")

    # 🔹 Allow user to enter a folder path instead of hardcoding it
    # Why? This makes the script reusable for any directory, enhancing flexibility.
    folder_path = input("Enter the folder path to clean: ").strip()

    # Validate folder path before proceeding
    if os.path.isdir(folder_path):
        print("\nWhat would you like to do?")
        print("1. Clean Folder")  # Sort files into categorized subfolders
        print("2. Undo Last Clean")  # Restore files to their original locations
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            clean_folder(folder_path)
            print("✅ Cleaning complete. Check 'file_cleaner.log' for details.")
        elif choice == "2":
            undo_last_clean()
        else:
            print("❌ Invalid choice.")
    else:
        print("❌ Invalid folder path. Please check and try again.")
