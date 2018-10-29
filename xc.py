import sys


def run():
  if len(sys.argv) < 2:
    print('Usage: xc <num>')
    sys.exit(1)
  arg = sys.argv[1]
  if arg[:2] == '0x':
    num = int(arg[2:], 16)
  else:
    num = int(arg)
  print('0x%x   %d' % (num, num))


if __name__ == '__main__':
  run()
