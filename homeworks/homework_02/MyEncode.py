def give_encode(filename):
    import chardet
    encod = {"utf-8", "utf-16", "windows-1251"}
    with open(filename, "rb") as file:
        data = file.read()
        code = chardet.detect(data)["encoding"]
    if code not in encod:
        return False
    return code
