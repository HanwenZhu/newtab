import sys

from newtab import app


if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = sys.argv[1]
    else:
        port = 5050
    app.run(host='localhost', port=port)
