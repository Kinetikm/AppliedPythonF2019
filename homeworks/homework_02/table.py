import sys

from .loader import Loader
from .parser import Parser
from .builder import Table

if __name__ == '__main__':
    filename = sys.argv[1]

    l = Loader(filename)
    p = Parser(filename, l.fencoding, l.fformat)
    t = Table()
    t.draw(p.parse_data())
