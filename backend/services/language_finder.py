import os
EXTENSION_TO_LANGUAGE = {
    '.py':   'py',
    '.js':   'js',
    '.ts':   'ts',
    '.tsx':  'ts',
    '.jsx':  'js',
    '.go':   'go',
    '.rb':   'rb',
    '.java': 'java',
    '.cpp': 'c++'
}

def language_find(name:str) -> str:
    _, ext = os.path.splitext(name)   # "Form.tsx" → ('.tsx')
    return EXTENSION_TO_LANGUAGE.get(ext,'generic')
