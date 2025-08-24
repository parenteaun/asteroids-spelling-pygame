import random
from collections import Counter

LETTER_SCORES = {
    7: list('AEIOULNSTR'),
    6: list('DG'),
    5: list('BCMP'),
    4: list('FHVWY'),
    3: list('K'),
    2: list('JX'),
    1: list('QZ')
}

def build_frequency_list():
    """Return a list with each letter repeated its value‑score times."""
    freq_list = []
    for score, letters in LETTER_SCORES.items():
        freq_list.extend(letters * score)
    random.shuffle(freq_list)
    return freq_list

def frequency_counter():
    """Convenience Counter for debug / UI."""
    return Counter(build_frequency_list())
