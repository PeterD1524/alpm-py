def parse_extended_data(string: bytes):
    name, value = string.split(b"=", 1)
    return name, value
