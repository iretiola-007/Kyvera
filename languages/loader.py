from . import japanese, german, italian

LANGUAGES = {
    "japanese": japanese,
    "german": german,
    "italian": italian,
}

def load_language(name):
    if name not in LANGUAGES:
        raise Exception(f"Unsupported language: {name}")
    return LANGUAGES[name]
