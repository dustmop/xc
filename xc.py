import sys


def run():
  if len(sys.argv) < 2:
    print('Usage: xc <num>')
    sys.exit(1)
  arg = sys.argv[1]
  num = int(arg)
  print('0x%x   %d' % (num, num))


if __name__ == '__main__':
  run()
