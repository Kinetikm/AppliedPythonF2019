def open_file(f):
    try:
        open(f)
        return True
    except:
        raise
