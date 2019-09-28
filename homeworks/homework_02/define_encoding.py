from chardet.universaldetector import UniversalDetector as d


def detect_encoding(filename):
    detector = d()
    try:
        with open(filename, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
    except:
        print("Файл не валиден")
        raise SystemExit
    return detector.result['encoding']
