import sys


def show(text):
  if text[:2] == '0x':
    return int(text[2:], 16)
  else:
    return int(text)


def run():
  if len(sys.argv) < 2:
    print('Usage: xc <num>')
    sys.exit(1)
  max_width = 0
  for n in xrange(1, len(sys.argv)):
    arg = sys.argv[n]
    text = '%x' % show(arg)
    if len(text) > max_width:
      max_width = len(text)
  print_template = '0x%0' + str(max_width) + 'x   %d'
  for n in xrange(1, len(sys.argv)):
    arg = sys.argv[n]
    num = show(arg)
    print(print_template % (num, num))


if __name__ == '__main__':
  run()
