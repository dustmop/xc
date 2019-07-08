import math
import os
import sys


class Elem(object):
  def __init__(self, val, func, prec):
    self.val = val
    self.func = func
    self.prec = prec

  def is_value(self):
    return self.val is not None

  def calculate(self, left, right):
    return Elem(self.func(left.num(), right.num()), None, None)

  def num(self):
    return self.val

  def higher_precedence(self, other):
    return self.prec > other.prec


def arg_to_elem(arg):
  if arg in ['+', '*', '-', '/', '**']:
    if arg == '+':
      f = lambda x,y: x + y
      p = 1
    elif arg == '*':
      f = lambda x,y: x * y
      p = 2
    elif arg == '-':
      f = lambda x,y: x - y
      p = 1
    elif arg == '/':
      f = lambda x,y: (1.0 * x) / y
      p = 2
    elif arg == '**':
      f = lambda x,y: x ** y
      p = 3
    return Elem(None, f, p)
  if arg == ',':
    return None
  v = parse_value(arg)
  return Elem(v, None, 0)


def collect_values(args):
  toper = None
  vals = []
  errs = []
  stack = []
  def flush_stack():
    # If empty
    if not stack:
      return
    result = stack.pop()
    while stack:
      # Reduce
      op = stack.pop()
      left = stack.pop()
      result = op.calculate(left, result)
    vals.append(result.num())
  # Iterate over the arguments
  for a in args:
    try:
      e = arg_to_elem(a)
    except ValueError:
      errs.append({'message': 'Failed to parse "%s"' % a, 'detail': a})
      stack = []
      continue
    if e is None:
      continue
    if e.is_value():
      # If top of stack is not an operator, two values in a row.
      if toper != len(stack) - 1:
        flush_stack()
      stack.append(e)
      continue
    if toper is None:
      # No operator in the stack
      stack.append(e)
      toper = len(stack) - 1
      continue
    if toper == len(stack) - 1:
      # Top of stack is an operator, error
      errs.append({'message': 'Syntax error %s %s' % (stack[-1].str(), e.str()),
                   'detail': e.str()})
      stack = []
      continue
    # Operator already in stack, check precedence
    if e.higher_precedence(stack[toper]):
      stack.append(e)
      toper = len(stack) - 1
      continue
    # Reduce
    right = stack.pop()
    op = stack.pop()
    left = stack.pop()
    result = op.calculate(left, right)
    stack.append(result)
    stack.append(e)
    toper = len(stack) - 1
    continue
  flush_stack()
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
  elif '.' in arg:
    return float(arg)
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
    if isinstance(n, float):
      if math.fabs(n - math.floor(n)) < 0.0001:
        n = int(n)
      else:
        print('%s' % n)
        continue
    print(print_template % (hex_unsigned(n), n))


if __name__ == '__main__':
  run()
