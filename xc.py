import os
import sys


def collect_values(args):
  oper = None
  vals = []
  errs = []
  for a in args:
    if oper:
      if oper == '+':
        f = lambda x,y: x + y
      elif oper == '*':
        f = lambda x,y: x * y
      elif oper == '-':
        f = lambda x,y: x - y
      elif oper == '/':
        f = lambda x,y: x / y
      elif oper == '**':
        f = lambda x,y: x ** y
      left = vals.pop()
      try:
        right = parse_value(a)
      except ValueError:
        errs.append({'message': 'Failed to parse "%s"' % a, 'detail': a})
        vals.append(0)
        continue
      vals.append(f(left, right))
      oper = None
      continue
    if a in ['+', '*', '-', '/', '**']:
      oper = a
    elif a == ',':
      pass
    else:
      try:
        vals.append(parse_value(a))
      except ValueError:
        errs.append({'message': 'Failed to parse "%s"' % a, 'detail': a})
        vals.append(0)
  return vals, errs


def parse_value(arg):
  if arg[-1] == ',':
    arg = arg[:-1]
  if arg[0] == 'x':
    return int(arg[1:], 16)
  elif arg[0:2] == '0x':
    return int(arg[2:], 16)
  elif arg[0:2] == '-x':
    return -int(arg[2:], 16)
  elif arg[0:3] == '-0x':
    return -int(arg[3:], 16)
  else:
    return int(arg, 10)


def get_max_widths(vals):
  max_dec = max_hex = 0
  for n in vals:
    text = '%d' % n
    if len(text) > max_dec:
      max_dec = len(text)
    text = '%x' % hex_unsigned(n)
    if len(text) > max_hex:
      max_hex = len(text)
  return max_dec, max_hex


def hex_unsigned(n):
  if n >= 0:
    return n
  ab = -n
  if ab <= 0x10:
    return 0x100 - ab
  else:
    return 0x10**(2 + len('%x' % (ab - 1))) - ab


def files_in_dir(path):
  return os.listdir(path)


def run():
  if len(sys.argv) < 2:
    print('Usage: xc <num>')
    sys.exit(1)
  (vals, errs) = collect_values(sys.argv[1:])
  if errs:
    files = files_in_dir('.')
    skip_found_files = False
    for e in errs:
      if skip_found_files and e['detail'] in files:
        continue
      sys.stderr.write(e['message'] + '\n')
      if e['detail'] in files:
        sys.stderr.write('Escape * using a backslash, like \\*\n')
        skip_found_files = True
    sys.exit(1)
  max_dec, max_hex = get_max_widths(vals)
  print_template = '0x%0' + str(max_hex) + 'x   %' + str(max_dec) + 'd'
  for n in vals:
    print(print_template % (hex_unsigned(n), n))


if __name__ == '__main__':
  run()
