import re


def remove_all_brackets(text: str) -> str:
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\{[^}]*\}', '', text)
    text = re.sub(r'\<[^>]*\>', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def normalize_word(word: str) -> str:
    return word.lower().strip(".,:;!?()[]{}«»\"'")


def word_in_translation(search_word: str, translation: str) -> tuple[bool, int]:
    clean_translation = remove_all_brackets(translation)
    search_word = normalize_word(search_word)

    if clean_translation.strip().lower() == search_word:
        return True, 10

    pattern = r'\b' + re.escape(search_word) + r'\b'
    if re.search(pattern, clean_translation):
        return True, 5

    return False, 0
