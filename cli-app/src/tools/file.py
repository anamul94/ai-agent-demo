import json
import os
from pathlib import Path
from typing import Any, List, Optional

from agno.tools import Toolkit
from agno.utils.log import log_debug, log_error, log_info


class FileTools(Toolkit):
    def __init__(
        self,
        base_dir: Optional[Path] = None,
        save_files: bool = True,
        read_files: bool = True,
        list_files: bool = True,
        search_files: bool = True,
        dir_operations: bool = True,
        **kwargs,
    ):
        self.base_dir: Path = base_dir or Path.cwd()

        tools: List[Any] = []
        if save_files:
            tools.append(self.save_file)
        if read_files:
            tools.append(self.read_file)
        if list_files:
            tools.append(self.list_files)
        if search_files:
            tools.append(self.search_files)
        if dir_operations:
            tools.extend([
                self.list_directory,
                self.list_directory_tree,
                self.create_directory,
                self.change_directory,
                self.get_current_directory,
                self.get_file_info,
                self.get_directory_size,
                self.walk_directory,
                self.find_files_by_extension,
                self.find_files_by_name,
                self.copy_file,
                self.move_file,
                self.delete_file,
                self.delete_directory,
                self.check_path_exists,
            ])

        super().__init__(name="file_tools", tools=tools, **kwargs)

    def save_file(self, contents: str, file_name: str, overwrite: bool = True) -> str:
        """Saves the contents to a file called `file_name` and returns the file name if successful.

        :param contents: The contents to save.
        :param file_name: The name of the file to save to.
        :param overwrite: Overwrite the file if it already exists.
        :return: The file name if successful, otherwise returns an error message.
        """
        try:
            file_path = self.base_dir.joinpath(file_name)
            log_debug(f"Saving contents to {file_path}")
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
            if file_path.exists() and not overwrite:
                return f"File {file_name} already exists"
            file_path.write_text(contents)
            log_info(f"Saved: {file_path}")
            return str(file_name)
        except Exception as e:
            log_error(f"Error saving to file: {e}")
            return f"Error saving to file: {e}"

    def read_file(self, file_name: str) -> str:
        """Reads the contents of the file `file_name` and returns the contents if successful.

        :param file_name: The name of the file to read.
        :return: The contents of the file if successful, otherwise returns an error message.
        """
        try:
            log_info(f"Reading file: {file_name}")
            file_path = self.base_dir.joinpath(file_name)
            contents = file_path.read_text(encoding="utf-8")
            return str(contents)
        except Exception as e:
            log_error(f"Error reading file: {e}")
            return f"Error reading file: {e}"

    def list_files(self) -> str:
        """Returns a list of files in the base directory

        :return: The contents of the file if successful, otherwise returns an error message.
        """
        try:
            log_info(f"Reading files in : {self.base_dir}")
            return json.dumps([str(file_path) for file_path in self.base_dir.iterdir()], indent=4)
        except Exception as e:
            log_error(f"Error reading files: {e}")
            return f"Error reading files: {e}"

    def search_files(self, pattern: str) -> str:
        """Searches for files in the base directory that match the pattern

        :param pattern: The pattern to search for, e.g. "*.txt", "file*.csv", "**/*.py".
        :return: JSON formatted list of matching file paths, or error message.
        """
        try:
            if not pattern or not pattern.strip():
                return "Error: Pattern cannot be empty"

            log_debug(f"Searching files in {self.base_dir} with pattern {pattern}")
            matching_files = list(self.base_dir.glob(pattern))

            file_paths = [str(file_path) for file_path in matching_files]

            result = {
                "pattern": pattern,
                "base_directory": str(self.base_dir),
                "matches_found": len(file_paths),
                "files": file_paths,
            }
            log_debug(f"Found {len(file_paths)} files matching pattern {pattern}")
            return json.dumps(result, indent=2)

        except Exception as e:
            error_msg = f"Error searching files with pattern '{pattern}': {e}"
            log_error(error_msg)
            return error_msg

    def list_directory(self, path: Optional[str] = None, show_hidden: bool = False) -> str:
        """Lists all files and directories in the specified path with detailed information.

        :param path: The directory path to list. If None, uses base_dir.
        :param show_hidden: Whether to show hidden files and directories.
        :return: JSON formatted directory listing with file details.
        """
        try:
            target_path = Path(path) if path else self.base_dir
            if not target_path.exists():
                return f"Error: Directory '{target_path}' does not exist"
            
            if not target_path.is_dir():
                return f"Error: '{target_path}' is not a directory"

            log_info(f"Listing directory: {target_path}")
            
            items = []
            for item in target_path.iterdir():
                if not show_hidden and item.name.startswith('.'):
                    continue
                
                stat = item.stat()
                items.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else None,
                    "modified": stat.st_mtime,
                    "permissions": oct(stat.st_mode)[-3:],
                })
            
            result = {
                "directory": str(target_path),
                "total_items": len(items),
                "items": sorted(items, key=lambda x: (x["type"], x["name"]))
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            log_error(f"Error listing directory: {e}")
            return f"Error listing directory: {e}"

    def list_directory_tree(self, path: Optional[str] = None, max_depth: int = 3) -> str:
        """Lists directory structure in a tree format up to specified depth.

        :param path: The directory path to explore. If None, uses base_dir.
        :param max_depth: Maximum depth to traverse (default: 3).
        :return: JSON formatted directory tree structure.
        """
        try:
            target_path = Path(path) if path else self.base_dir
            if not target_path.exists():
                return f"Error: Directory '{target_path}' does not exist"
            
            if not target_path.is_dir():
                return f"Error: '{target_path}' is not a directory"

            log_info(f"Creating directory tree for: {target_path}")
            
            def build_tree(current_path: Path, current_depth: int) -> dict:
                if current_depth > max_depth:
                    return {"name": current_path.name, "type": "directory", "truncated": True}
                
                item_info = {
                    "name": current_path.name,
                    "path": str(current_path),
                    "type": "directory" if current_path.is_dir() else "file"
                }
                
                if current_path.is_dir():
                    children = []
                    try:
                        for child in sorted(current_path.iterdir()):
                            if not child.name.startswith('.'):  # Skip hidden files
                                children.append(build_tree(child, current_depth + 1))
                        item_info["children"] = children
                    except PermissionError:
                        item_info["error"] = "Permission denied"
                else:
                    item_info["size"] = current_path.stat().st_size
                
                return item_info
            
            tree = build_tree(target_path, 0)
            return json.dumps(tree, indent=2)
            
        except Exception as e:
            log_error(f"Error creating directory tree: {e}")
            return f"Error creating directory tree: {e}"

    def create_directory(self, dir_name: str, parents: bool = True) -> str:
        """Creates a new directory.

        :param dir_name: The name/path of the directory to create.
        :param parents: Whether to create parent directories if they don't exist.
        :return: Success message or error message.
        """
        try:
            dir_path = self.base_dir.joinpath(dir_name)
            log_info(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=parents, exist_ok=True)
            return f"Directory '{dir_name}' created successfully"
        except Exception as e:
            log_error(f"Error creating directory: {e}")
            return f"Error creating directory: {e}"

    def change_directory(self, path: str) -> str:
        """Changes the base directory for file operations.

        :param path: The new base directory path.
        :return: Success message or error message.
        """
        try:
            new_path = Path(path).resolve()
            if not new_path.exists():
                return f"Error: Directory '{path}' does not exist"
            if not new_path.is_dir():
                return f"Error: '{path}' is not a directory"
            
            old_base = self.base_dir
            self.base_dir = new_path
            log_info(f"Changed base directory from {old_base} to {new_path}")
            return f"Changed base directory to: {new_path}"
        except Exception as e:
            log_error(f"Error changing directory: {e}")
            return f"Error changing directory: {e}"

    def get_current_directory(self) -> str:
        """Returns the current base directory.

        :return: Current base directory path.
        """
        return str(self.base_dir)

    def get_file_info(self, file_name: str) -> str:
        """Gets detailed information about a file or directory.

        :param file_name: The name of the file or directory.
        :return: JSON formatted file information.
        """
        try:
            file_path = self.base_dir.joinpath(file_name)
            if not file_path.exists():
                return f"Error: '{file_name}' does not exist"
            
            stat = file_path.stat()
            info = {
                "name": file_path.name,
                "path": str(file_path),
                "type": "directory" if file_path.is_dir() else "file",
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "accessed": stat.st_atime,
                "permissions": oct(stat.st_mode)[-3:],
                "owner": stat.st_uid,
                "group": stat.st_gid,
            }
            
            if file_path.is_file():
                info["extension"] = file_path.suffix
                info["stem"] = file_path.stem
            
            return json.dumps(info, indent=2)
            
        except Exception as e:
            log_error(f"Error getting file info: {e}")
            return f"Error getting file info: {e}"

    def get_directory_size(self, dir_name: Optional[str] = None) -> str:
        """Calculates the total size of a directory and its contents.

        :param dir_name: The directory name. If None, uses base_dir.
        :return: Directory size information in JSON format.
        """
        try:
            target_path = Path(dir_name) if dir_name else self.base_dir
            if not target_path.exists():
                return f"Error: Directory '{target_path}' does not exist"
            if not target_path.is_dir():
                return f"Error: '{target_path}' is not a directory"
            
            total_size = 0
            file_count = 0
            dir_count = 0
            
            for item in target_path.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
                    file_count += 1
                elif item.is_dir():
                    dir_count += 1
            
            result = {
                "directory": str(target_path),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "file_count": file_count,
                "directory_count": dir_count
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            log_error(f"Error calculating directory size: {e}")
            return f"Error calculating directory size: {e}"

    def walk_directory(self, path: Optional[str] = None, max_files: int = 100) -> str:
        """Walks through directory structure and returns all files and subdirectories.

        :param path: The directory path to walk. If None, uses base_dir.
        :param max_files: Maximum number of files to return (prevents overwhelming output).
        :return: JSON formatted list of all files and directories.
        """
        try:
            target_path = Path(path) if path else self.base_dir
            if not target_path.exists():
                return f"Error: Directory '{target_path}' does not exist"
            if not target_path.is_dir():
                return f"Error: '{target_path}' is not a directory"
            
            all_items = []
            file_count = 0
            
            for root, dirs, files in os.walk(target_path):
                root_path = Path(root)
                
                # Add directories
                for dir_name in dirs:
                    all_items.append({
                        "name": dir_name,
                        "path": str(root_path / dir_name),
                        "type": "directory",
                        "parent": str(root_path)
                    })
                
                # Add files
                for file_name in files:
                    if file_count >= max_files:
                        break
                    file_path = root_path / file_name
                    all_items.append({
                        "name": file_name,
                        "path": str(file_path),
                        "type": "file",
                        "parent": str(root_path),
                        "size": file_path.stat().st_size,
                        "extension": file_path.suffix
                    })
                    file_count += 1
                
                if file_count >= max_files:
                    break
            
            result = {
                "directory": str(target_path),
                "total_items": len(all_items),
                "truncated": file_count >= max_files,
                "items": all_items
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            log_error(f"Error walking directory: {e}")
            return f"Error walking directory: {e}"

    def find_files_by_extension(self, extension: str, path: Optional[str] = None) -> str:
        """Finds all files with a specific extension.

        :param extension: The file extension to search for (e.g., '.txt', '.py').
        :param path: The directory path to search. If None, uses base_dir.
        :return: JSON formatted list of matching files.
        """
        try:
            target_path = Path(path) if path else self.base_dir
            if not extension.startswith('.'):
                extension = '.' + extension
            
            pattern = f"**/*{extension}"
            return self.search_files(pattern)
            
        except Exception as e:
            log_error(f"Error finding files by extension: {e}")
            return f"Error finding files by extension: {e}"

    def find_files_by_name(self, name_pattern: str, path: Optional[str] = None) -> str:
        """Finds all files matching a name pattern.

        :param name_pattern: The name pattern to search for (supports wildcards).
        :param path: The directory path to search. If None, uses base_dir.
        :return: JSON formatted list of matching files.
        """
        try:
            pattern = f"**/{name_pattern}"
            return self.search_files(pattern)
            
        except Exception as e:
            log_error(f"Error finding files by name: {e}")
            return f"Error finding files by name: {e}"

    def copy_file(self, src: str, dst: str) -> str:
        """Copies a file from source to destination.

        :param src: Source file path.
        :param dst: Destination file path.
        :return: Success message or error message.
        """
        try:
            import shutil
            src_path = self.base_dir.joinpath(src)
            dst_path = self.base_dir.joinpath(dst)
            
            if not src_path.exists():
                return f"Error: Source file '{src}' does not exist"
            
            # Create destination directory if it doesn't exist
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(src_path, dst_path)
            log_info(f"Copied {src_path} to {dst_path}")
            return f"File copied successfully from '{src}' to '{dst}'"
            
        except Exception as e:
            log_error(f"Error copying file: {e}")
            return f"Error copying file: {e}"

    def move_file(self, src: str, dst: str) -> str:
        """Moves a file from source to destination.

        :param src: Source file path.
        :param dst: Destination file path.
        :return: Success message or error message.
        """
        try:
            import shutil
            src_path = self.base_dir.joinpath(src)
            dst_path = self.base_dir.joinpath(dst)
            
            if not src_path.exists():
                return f"Error: Source file '{src}' does not exist"
            
            # Create destination directory if it doesn't exist
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(src_path), str(dst_path))
            log_info(f"Moved {src_path} to {dst_path}")
            return f"File moved successfully from '{src}' to '{dst}'"
            
        except Exception as e:
            log_error(f"Error moving file: {e}")
            return f"Error moving file: {e}"

    def delete_file(self, file_name: str) -> str:
        """Deletes a file.

        :param file_name: The name of the file to delete.
        :return: Success message or error message.
        """
        try:
            file_path = self.base_dir.joinpath(file_name)
            if not file_path.exists():
                return f"Error: File '{file_name}' does not exist"
            
            if file_path.is_dir():
                return f"Error: '{file_name}' is a directory, use delete_directory instead"
            
            file_path.unlink()
            log_info(f"Deleted file: {file_path}")
            return f"File '{file_name}' deleted successfully"
            
        except Exception as e:
            log_error(f"Error deleting file: {e}")
            return f"Error deleting file: {e}"

    def delete_directory(self, dir_name: str, recursive: bool = False) -> str:
        """Deletes a directory.

        :param dir_name: The name of the directory to delete.
        :param recursive: Whether to delete directory and all its contents.
        :return: Success message or error message.
        """
        try:
            import shutil
            dir_path = self.base_dir.joinpath(dir_name)
            if not dir_path.exists():
                return f"Error: Directory '{dir_name}' does not exist"
            
            if not dir_path.is_dir():
                return f"Error: '{dir_name}' is not a directory"
            
            if recursive:
                shutil.rmtree(dir_path)
                log_info(f"Deleted directory recursively: {dir_path}")
                return f"Directory '{dir_name}' and all contents deleted successfully"
            else:
                dir_path.rmdir()  # Only works if directory is empty
                log_info(f"Deleted empty directory: {dir_path}")
                return f"Directory '{dir_name}' deleted successfully"
            
        except Exception as e:
            log_error(f"Error deleting directory: {e}")
            return f"Error deleting directory: {e}"

    def check_path_exists(self, path: str) -> str:
        """Checks if a path exists and returns its type.

        :param path: The path to check.
        :return: JSON formatted path information.
        """
        try:
            target_path = self.base_dir.joinpath(path)
            
            result = {
                "path": str(target_path),
                "exists": target_path.exists(),
                "type": None,
                "readable": False,
                "writable": False
            }
            
            if target_path.exists():
                if target_path.is_file():
                    result["type"] = "file"
                elif target_path.is_dir():
                    result["type"] = "directory"
                elif target_path.is_symlink():
                    result["type"] = "symlink"
                else:
                    result["type"] = "other"
                
                result["readable"] = os.access(target_path, os.R_OK)
                result["writable"] = os.access(target_path, os.W_OK)
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            log_error(f"Error checking path: {e}")
            return f"Error checking path: {e}"