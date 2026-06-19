import os
def should_index(file_path: str,file_type:str) -> bool:

    if file_type !='blob':
        return False

    ignored_patterns= {'node_modules','.git','.env','dist','build','.next','__pycache__'}

    path_components = file_path.split('/')
    if any(part in ignored_patterns for part in path_components):
        return False
    
    valid_extensions = {
        '.py', '.js', '.ts', '.java', '.c', '.cpp', 
        '.h', '.cs', '.go', '.rs', '.rb', '.php','.tsx','.jsx'
    }

    _, ext = os.path.splitext(file_path)
    return ext.lower() in valid_extensions