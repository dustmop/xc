import sys


def collect_values(args):
  oper = None
  vals = []
  for a in args:
    if oper:
      if oper == '+':
        left = vals.pop()
        right = parse_value(a)
        vals.append(left + right)
      elif oper == '*':
        left = vals.pop()
        right = parse_value(a)
        vals.append(left * right)
      elif oper == '-':
        left = vals.pop()
        right = parse_value(a)
        vals.append(left - right)
      elif oper == '/':
        left = vals.pop()
        right = parse_value(a)
        vals.append(left / right)
      oper = None
      continue
    if a in ['+', '*', '-', '/']:
      oper = a
    elif a == ',':
      pass
    else:
      vals.append(parse_value(a))
  return vals


def parse_value(arg):
  if arg[0] == 'x':
    return int(arg[1:], 16)
  elif arg[0:2] == '0x':
    return int(arg[2:], 16)
  else:
    return int(arg, 10)


def get_max_width(vals):
  max_width = 0
  for n in vals:
    text = '%d' % n
    if len(text) > max_width:
      max_width = len(text)
  return max_width


def run():
  if len(sys.argv) < 2:
    print('Usage: xc <num>')
    sys.exit(1)
  vals = collect_values(sys.argv[1:])
  max_width = get_max_width(vals)
  print_template = '0x%0' + str(max_width) + 'x   %' + str(max_width) + 'd'
  for n in vals:
    print(print_template % (n, n))


if __name__ == '__main__':
  run()
