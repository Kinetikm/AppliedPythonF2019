from chardet.universaldetector import UniversalDetector


def define_encoding(filename):
    detector = UniversalDetector()
    try:
        with open(filename, 'rb') as file_:
            for line in file_:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
    except:
        print("Файл не валиден")
        raise SystemExit
    return detector.result['encoding']
