import unittest

import xc


class XCTests(unittest.TestCase):
  def test_basic(self):
    (vals, errs) = xc.collect_values(['123'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [123])

  def test_multiple_values(self):
    (vals, errs) = xc.collect_values(['34', '56', '78'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [34, 56, 78])

  def test_ignore_comma(self):
    (vals, errs) = xc.collect_values(['34', ',', '56,', '78'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [34, 56, 78])

  def test_addition(self):
    (vals, errs) = xc.collect_values(['203', '+', '142'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [345])

  def test_subtraction(self):
    (vals, errs) = xc.collect_values(['203', '-', '142'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [61])

  def test_multiply(self):
    (vals, errs) = xc.collect_values(['203', '*', '142'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [28826])

  def test_divide(self):
    (vals, errs) = xc.collect_values(['564', '/', '2'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [282.0])

  def test_exponent(self):
    (vals, errs) = xc.collect_values(['24', '**', '5'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [7962624])

  def test_hex(self):
    (vals, errs) = xc.collect_values(['0xabc', 'x124', '0x10', 'xc84'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [2748, 292, 16, 3204])

  def test_negative(self):
    (vals, errs) = xc.collect_values(['-564'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [-564])

  def test_negative_hex(self):
    (vals, errs) = xc.collect_values(['-0x34', '-x1234'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [-52, -4660])

  def test_floating(self):
    (vals, errs) = xc.collect_values(['35.7'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [35.7])

  def test_same_precedence(self):
    (vals, errs) = xc.collect_values(['203', '+', '142', '+', '7'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [352])

  def test_higher_precedence(self):
    (vals, errs) = xc.collect_values(['203', '+', '142', '*', '7'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [1197])

  def test_lower_precedence(self):
    (vals, errs) = xc.collect_values(['203', '*', '142', '+', '7'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [28833])

  def test_syntax_error(self):
    (vals, errs) = xc.collect_values(['203', '+', '+', '142'])
    self.assertEqual(errs, [{'message': 'Syntax error: "+ +"', 'detail': '+'}])
    self.assertEqual(vals, [142])

  def test_empty_stack_error(self):
    (vals, errs) = xc.collect_values(['+', '142'])
    self.assertEqual(errs, [{'message': 'Operator missing left hand size "+"',
                             'detail': '+'}])
    self.assertEqual(vals, [142])

  def test_spaces_in_args(self):
    (vals, errs) = xc.collect_values(['203 + 142'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [345])

  def test_mixed_spaces(self):
    (vals, errs) = xc.collect_values(['123', '+', '203 + 142', ' + 348'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [816])

  def test_multiple_operators(self):
    (vals, errs) = xc.collect_values(['3', '+', '4', '5', '+', '6'])
    self.assertEqual(errs, [])
    self.assertEqual(vals, [7, 11])


# TODO:
# padding
# display hex and dec, correct width
# test errors


if __name__ == '__main__':
  unittest.main()
