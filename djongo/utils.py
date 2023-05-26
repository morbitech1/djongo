def encode_key(s: str):
    return s.replace("\\", "\\\\").replace("\$", "\\u0024").replace(".", "\\u002e")


encode_keys_cache = {}
def encode_keys(obj, is_key=False):
    if is_key:
        if obj in encode_keys_cache:
            return encode_keys_cache[obj]
        if isinstance(obj, int):
            encode_keys_cache[obj] = str(obj)
        elif isinstance(obj, str):
            encode_keys_cache[obj] = encode_key(obj)
        else:
            return obj
        return encode_keys_cache[obj]
    if isinstance(obj, dict):
        return {encode_keys(k, True): encode_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [encode_keys(v) for v in obj]
    return obj


def decode_key(s: str):
    return s.replace("\\u002e", ".").replace("\\u0024", "\$").replace("\\\\", "\\")


decode_keys_cache = {}
def decode_keys(obj, is_key=False):
    if isinstance(obj, str):
        if is_key:
            if obj in decode_keys_cache:
                return decode_keys_cache[obj]
            if obj.isdigit() or (obj.startswith('-') and obj[1:].isdigit()):
                decode_keys_cache[obj] = int(obj)
            else:
                decode_keys_cache[obj] = decode_key(obj)
            return decode_keys_cache[obj]
        return obj
    if isinstance(obj, dict):
        return {decode_keys(k, True): decode_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode_keys(v) for v in obj]
    return obj
