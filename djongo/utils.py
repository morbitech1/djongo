import re
import functools


encode_dict = {
    ".": "\\u002e",
    "\$": "\\u0024",
    "\\": "\\\\",
}
encode_regex = re.compile("|".join(map(re.escape, encode_dict.keys())))


@functools.lru_cache(maxsize=1024)
def encode_key(s: str):
    if isinstance(s, int):
        return str(s)
    elif isinstance(s, str):
        return encode_regex.sub(lambda match: encode_dict[match.group()], s)
    else:
        return s


def encode_keys(obj, is_key=False):
    if is_key:
        if isinstance(obj, (int, str)):
            return encode_key(obj)
        return obj
    if isinstance(obj, dict):
        return {encode_keys(k, True): encode_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [encode_keys(v) for v in obj]
    return obj


decode_dict = {
    "\\u002e": ".",
    "\\u0024": "\$",
    "\\\\": "\\",
}
decode_regex = re.compile("|".join(map(re.escape, decode_dict.keys())))


@functools.lru_cache(maxsize=1024)
def decode_key(s: str):
    if s.isdigit() or (s.startswith('-') and s[1:].isdigit()):
        return int(s)
    else:
        return decode_regex.sub(lambda match: decode_dict[match.group()], s)


def decode_keys(obj, is_key=False):
    if isinstance(obj, str):
        if is_key:
            return decode_key(obj)
        return obj
    if isinstance(obj, dict):
        return {decode_keys(k, True): decode_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode_keys(v) for v in obj]
    return obj
