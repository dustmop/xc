import math
import os
import sys


class Elem(object):
  """Elem represents some kind of element: a value, or an operator"""

  def __init__(self, val, name, func, prec):
    self.val = val
    self.name = name
    self.func = func
    self.prec = prec

  def is_value(self):
    return self.val is not None

  def calculate(self, left, right):
    return Elem(self.func(left.num(), right.num()), None, None, None)

  def num(self):
    return self.val

  def str(self):
    if self.is_value():
      return self.val
    return self.name

  def higher_precedence(self, other):
    return self.prec > other.prec

  def __repr__(self):
    return '#<Elem val=%s name=%s func=%s prec=%s>'.format(
      self.val, self.name, '#func' if self.func else None, self.prec)


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
    return Elem(None, arg, f, p)
  if arg == ',':
    return None
  v = parse_value(arg)
  return Elem(v, None, None, 0)


def collect_values(args):
  # Expand any arguments with spaces (quoted on command-line).
  args = [each for a in args for each in a.split(' ') if each]
  # Stack and other things for expression handling.
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
  # Retrieve flags
  flags = {}
  if len(args) > 0 and args[0] == '-d':
    flags['dec'] = True
    args = args[1:]
  if len(args) > 0 and args[0] == '-x':
    flags['hex'] = True
    args = args[1:]
  # Iterate over the arguments
  for a in args:
    try:
      e = arg_to_elem(a)
    except ValueError:
      errs.append({'kind': 'parse',
                   'message': 'Failed to parse "{}"'.format(a), 'detail': a})
      toper = None
      stack = []
      continue
    if e is None:
      continue
    if e.is_value():
      # If top of stack is not an operator, two values in a row.
      if toper != len(stack) - 1:
        flush_stack()
        toper = None
      stack.append(e)
      continue
    if toper is None:
      # No operator in the stack
      if not stack:
        msg = 'Operator missing left hand size "{}"'.format(a)
        errs.append({'kind': 'no-op', 'message': msg, 'detail': a})
        continue
      stack.append(e)
      toper = len(stack) - 1
      continue
    if toper == len(stack) - 1:
      # Top of stack is an operator, error
      msg = 'Syntax error: "{} {}"'.format(stack[-1].str(), e.str())
      errs.append({'kind': 'syntax', 'message': msg, 'detail': e.str()})
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
  return vals, flags, errs


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
    text = '{}'.format(n)
    if len(text) > max_dec:
      max_dec = len(text)
    text = '{:x}'.format(hex_unsigned(n))
    if len(text) > max_hex:
      max_hex = len(text)
  return max_dec, max_hex


def hex_unsigned(n):
  if n >= 0:
    return int(n)
  ab = -n
  if ab <= 0x10:
    return int(0x100 - ab)
  else:
    return int(0x10**(2 + len('{:x}'.format(ab - 1))) - ab)


def files_in_dir(path):
  return os.listdir(path)


def is_filefound_error(e, files):
  return e['kind'] == 'parse' and e['detail'] in files


def display_errors(errs):
  files = files_in_dir('.')
  for e in errs:
    sys.stderr.write(e['message'] + '\n')
    if is_filefound_error(e, files):
      sys.stderr.write('Escape * using a backslash, like \\*\n')
      return


def run():
  if len(sys.argv) < 2:
    print("""Usage: xc <inputs>

  inputs: Any series of numbers (decimal or hex) with arithemetic operators.
          Numbers will be displayed in both decimal and hex, and arithmetic
          operators will be applied according to standard precendence.

  Flags:     -x     output hexadecimal only (with no prefix)
             -d     output decimal only

  Operators: +, -   addition, subtraction
             *, /   multiply, divide (you may need to escape multiply like \*)
             **     exponentiation

  Numbers:   123         decimal
             -456        negative
             0xa4, xa4   hexadecimal

  Examples:
  > xc 0x40 + 20
  0x54 84

  > xc 10 0x10 100 0x100
  0x00a    10
  0x010    16
  0x064   100
  0x100   256

  > xc -0x21 \* 5
  0xff56   -165

  > xc '123 + 345'
  0x1d4   468""")
    sys.exit(1)
  (vals, flags, errs) = collect_values(sys.argv[1:])
  if errs:
    display_errors(errs)
    sys.exit(1)
  max_dec, max_hex = get_max_widths(vals)
  show_template = '0x{hex:' + str(max_hex) + 'x}   {dec:' + str(max_dec) + 'd}'
  if flags.get('dec'):
    show_template = '{dec:' + str(max_dec) + 'd}'
  if flags.get('hex'):
    show_template = '{hex:' + str(max_hex) + 'x}'
  for n in vals:
    if isinstance(n, float):
      if math.fabs(n - math.floor(n)) < 0.0001:
        n = int(n)
      else:
        print('{}'.format(n))
        continue
    print(show_template.format(hex=hex_unsigned(n), dec=n))


if __name__ == '__main__':
  run()
