#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Open Communications Security
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import unittest
import cpfcnpj
import re

CNPJ_SAMPLES = []
CPF_SAMPLES = []
def setUpModule():
	with open('cpfcnpj-test-cnpj.txt', 'r') as inp:
		for l in inp:
			l = l.strip()
			if re.match('[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}\\/[0-9]{4}\\-[0-9]{2}', l):
				CNPJ_SAMPLES.append(l)
	with open('cpfcnpj-test-cpf.txt', 'r') as inp:
		for l in inp:
			l = l.strip()
			if re.match('[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}\\-[0-9]{2}', l):
				CPF_SAMPLES.append(l)

class TestCpfCN(unittest.TestCase):
	def test_remove_non_digits(self):
		self.assertEqual('', cpfcnpj.remove_non_digits(''))
		self.assertEqual('1234567890', cpfcnpj.remove_non_digits('1234567890'))
		self.assertEqual('1234567890', cpfcnpj.remove_non_digits('1a2d3 f4 g5 h6t7r 8y9h0'))

	def test_gen_random_string(self):
		for i in range(128):
			s = cpfcnpj.gen_random_string(i)
			self.assertEqual(i, len(s))
			self.assertIsNotNone(re.match('[0-9]*', s))

	def test_compute_cpf_validation(self):
		for c in CPF_SAMPLES:
			c = cpfcnpj.remove_non_digits(c)
			v = cpfcnpj.compute_cpf_validation(c)
			self.assertEqual(c[9:12], v)

	def test_compute_cnpj_validation(self):
		for c in CNPJ_SAMPLES:
			c = cpfcnpj.remove_non_digits(c)
			v = cpfcnpj.compute_cnpj_validation(c)
			self.assertEqual(c[12:14], v)

	def test_gen_random_cpf(self):
		for i in range(128):
			c = cpfcnpj.gen_random_cpf()
			self.assertEquals(11, len(c))
			self.assertEquals(cpfcnpj.compute_cpf_validation(c), c[9:11])

	def test_gen_random_cnpj(self):
		for i in range(128):
			c = cpfcnpj.gen_random_cnpj()
			self.assertEquals(14, len(c))
			self.assertEquals(cpfcnpj.compute_cnpj_validation(c), c[12:14])

	def test_gen_random_cnpj_unit(self):
		for i in range(128):
			c = cpfcnpj.gen_random_cnpj(i)
			unit = '{0:04d}'.format(i)
			self.assertEquals(14, len(c))
			self.assertEquals(unit, c[8:12])
			self.assertEquals(cpfcnpj.compute_cnpj_validation(c), c[12:14])

	def test_format_cpf(self):
		for c in CPF_SAMPLES:
			v = cpfcnpj.format_cpf(cpfcnpj.remove_non_digits(c))
			self.assertEqual(c, v)

	def test_format_cnpj(self):
		for c in CNPJ_SAMPLES:
			v = cpfcnpj.format_cnpj(cpfcnpj.remove_non_digits(c))
			self.assertEqual(c, v)

	def test_is_cpf_valid(self):
		for c in CPF_SAMPLES:
			# Formatted
			self.assertTrue(cpfcnpj.is_cpf_valid(c))
			c = cpfcnpj.remove_non_digits(c)
			# Make the validation incorrect
			c = c[0:9] + '{0:02d}'.format((int(c[9:11]) + 1) % 100)
			self.assertFalse(cpfcnpj.is_cpf_valid(c))
			self.assertFalse(cpfcnpj.is_cpf_valid(cpfcnpj.format_cpf(c)))
		# Wrong values
		self.assertFalse(cpfcnpj.is_cpf_valid('37.7984.551-24'))
		self.assertFalse(cpfcnpj.is_cpf_valid('377984.551-24'))
		self.assertFalse(cpfcnpj.is_cpf_valid('377.A84.551-24'))
		self.assertFalse(cpfcnpj.is_cpf_valid('3779845512'))
		self.assertFalse(cpfcnpj.is_cpf_valid('377984551A4'))
		self.assertFalse(cpfcnpj.is_cpf_valid('377984551241'))

	def test_is_cnpj_valid(self):
		for c in CNPJ_SAMPLES:
			# Formatted
			self.assertTrue(cpfcnpj.is_cnpj_valid(c))
			c = cpfcnpj.remove_non_digits(c)
			# Make the validation incorrect
			c = c[0:12] + '{0:02d}'.format((int(c[12:14]) + 1) % 100)
			self.assertFalse(cpfcnpj.is_cnpj_valid(c))
			self.assertFalse(cpfcnpj.is_cnpj_valid(cpfcnpj.format_cnpj(c)))
		# Wrong values
		self.assertFalse(cpfcnpj.is_cnpj_valid('431.35.870/0001-80'))
		self.assertFalse(cpfcnpj.is_cnpj_valid('43.135.8700001-80'))
		self.assertFalse(cpfcnpj.is_cnpj_valid('43.135.870/000180'))
		self.assertFalse(cpfcnpj.is_cnpj_valid('43.135.A70/0001-80'))
		self.assertFalse(cpfcnpj.is_cnpj_valid('4313587000018'))
		self.assertFalse(cpfcnpj.is_cnpj_valid('431358700001a0'))
		self.assertFalse(cpfcnpj.is_cnpj_valid('431358700001801'))

if __name__ == '__main__':
    unittest.main()

