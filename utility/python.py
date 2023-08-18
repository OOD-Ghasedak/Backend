import random
import string
from typing import Sequence


def common_prefix(s1: str, s2: str):
    len_s2 = len(s2)
    for i, c in enumerate(s1):
        if i >= len_s2 or s2[i] != c:
            return s1[:i]
    return s1


def generate_random_string(options: Sequence, length: int) -> str:
    return ''.join(random.choices(options, k=length))


def rand_slug():
    return generate_random_string(string.ascii_letters + string.digits, length=8)
