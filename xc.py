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
  if arg[-1] == ',':
    arg = arg[:-1]
  if arg[0] == 'x':
    return int(arg[1:], 16)
  elif arg[0:2] == '0x':
    return int(arg[2:], 16)
  else:
    return int(arg, 10)


def get_max_widths(vals):
  max_dec = max_hex = 0
  for n in vals:
    text = '%d' % n
    if len(text) > max_dec:
      max_dec = len(text)
    text = '%x' % n
    if len(text) > max_hex:
      max_hex = len(text)
  return max_dec, max_hex


def run():
  if len(sys.argv) < 2:
    print('Usage: xc <num>')
    sys.exit(1)
  vals = collect_values(sys.argv[1:])
  max_dec, max_hex = get_max_widths(vals)
  print_template = '0x%0' + str(max_hex) + 'x   %' + str(max_dec) + 'd'
  for n in vals:
    print(print_template % (n, n))


if __name__ == '__main__':
  run()
