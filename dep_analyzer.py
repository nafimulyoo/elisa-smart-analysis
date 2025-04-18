import os
import sys
import ast

def find_dependencies(filename, project_root, visited=None):
    """
    Recursively find all dependencies of a Python file, excluding venv.

    Args:
        filename: The path to the Python file.
        project_root: The root directory of the project.
        visited: A set to keep track of visited files.

    Returns:
        A set of all dependent module filepaths.
    """
    if visited is None:
        visited = set()

    filename = os.path.abspath(filename)
    if filename in visited:
        return set()

    visited.add(filename)
    dependencies = {filename}

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        return set()
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        return set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            else:  # ast.ImportFrom
                modules = [node.module] if node.module else []

            for module_name in modules:
                if module_name is None:
                    continue

                module_file = find_module_file(module_name, project_root)

                if module_file and not is_venv_file(module_file, project_root):
                    dependencies.update(
                        find_dependencies(module_file, project_root, visited)
                    )
                elif module_file:
                    print(
                        f"Skipping venv module {module_name} imported in "
                        f"{filename}"
                    )
                else:
                    print(
                        f"Warning: Could not find module {module_name} imported"
                        f" in {filename}"
                    )

    return dependencies


def find_module_file(module_name, project_root):
    """
    Find the file path of a module given its name, considering sys.path.

    Args:
        module_name: The name of the module.
        project_root: The root directory of the project.

    Returns:
        The absolute path to the module's file, or None if not found.
    """
    for path in sys.path:
        if path == "":
            search_path = project_root
        else:
            search_path = path

        module_path = os.path.join(
            search_path, module_name.replace('.', '/') + '.py'
        )
        init_path = os.path.join(
            search_path, module_name.replace('.', '/'), '__init__.py'
        )

        if os.path.isfile(module_path):
            return os.path.abspath(module_path)
        elif os.path.isfile(init_path):
            return os.path.abspath(init_path)

    return None


def list_all_python_files(directory):
    """
    List all Python files in a directory recursively.

    Args:
        directory: The directory to search.

    Returns:
        A set of absolute paths to all Python files.
    """
    python_files = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.add(os.path.abspath(os.path.join(root, file)))
    return python_files


def is_venv_file(filepath, project_root):
    """
    Check if a file is located within a virtual environment directory.

    Args:
        filepath: The absolute path to the file.
        project_root: The root directory of the project.

    Returns:
        True if the file is in a venv, False otherwise.
    """
    venv_names = ['venv', '.venv', 'env']  # Common venv names

    filepath = os.path.abspath(filepath)
    project_root = os.path.abspath(project_root)

    parts = filepath.replace(project_root, '').split(os.sep)
    for part in parts:
        if part in venv_names:
            return True
    return False


if __name__ == '__main__':
    project_root = '.'  # Replace with the actual root directory
    entry_points = ['index.py']

    all_dependencies = set()
    for entry_point in entry_points:
        entry_point_path = os.path.join(project_root, entry_point)
        if os.path.isfile(entry_point_path):
            all_dependencies.update(
                find_dependencies(entry_point_path, project_root)
            )
        else:
            print(f"Error: Entry point not found: {entry_point_path}")

    all_python_files = list_all_python_files(project_root)

    # Exclude venv files from all_python_files
    all_python_files = {
        f for f in all_python_files if not is_venv_file(f, project_root)
    }

    unused_files = all_python_files - all_dependencies

    print("Potentially unused Python files:")
    for file in sorted(unused_files):
        print(file)

    # Output to file
    with open('not_used.txt', 'w') as f:
        for file in sorted(unused_files):
            f.write(file + '\n')

    print("Unused files written to not_used.txt")
