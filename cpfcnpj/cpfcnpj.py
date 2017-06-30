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
import re
import random

def remove_non_digits(v):
	""" Remove all non digit characters from a given string.
	Parameter:
		v -- The source string.
	Return:
		The value of v without the non-digit characters.
	"""
	return re.sub('[^0-9]', '', v)

def gen_random_string(length):
	""" Generates a random digit string.
	Parameter:
		length -- The lenght of the strings.
	Return:
		The random string.
	"""
	s = ''
	for i in range(length):
		s = s + str(random.randrange(0,10))
	return s

def compute_cpf_validation(cpf):
	""" Generates the check digits for a given CPF.
	Parameter:
		cpf -- A string with 9 to 11 digits. Only the first 9 will be used.
	Return:
		The checkdigits for the given CPF.
	"""
	if not re.match('[0-9]{9,11}', cpf):
		raise ValueError('The CPF must have at least 9 digits.')
	v1 = 0
	v2 = 0
	for i in range(9):
		c = int(cpf[i:i+1])
		v1 = v1 + (c * (10 - i))
		v2 = v2 + (c * (11 - i))
	v1 = 11 - (v1 % 11)
	if v1 > 9:
		v1 = 0
	v2 = 11 - ((v2 + v1 * 2) % 11)
	if v2 > 9:
		v2 = 0
	return str(v1) + str(v2)

def compute_cnpj_validation(cnpj):
	""" Generates the check digits for a given CNPJ.
	Parameter:
		cnpj -- A string with 12 to 14 digits. Only the first 12 will be used.
	Return:
		The checkdigits for the given CPF.
	"""
	if not re.match('[0-9]{12,14}', cnpj):
		raise ValueError('The CNPJ must have at least 12 digits.')
	v1 = 0
	v2 = 0
	for i in range(12):
		c = int(cnpj[i:i+1])
		m1 = 9 - ((i + 4) % 8)
		m2 = 9 - ((i + 3) % 8)
		v1 = v1 + (c * m1)
		v2 = v2 + (c * m2)
	v1 = 11 - (v1 % 11)
	if v1 > 9:
		v1 = 0
	v2 = 11 - ((v2 + v1 * 2) % 11)
	if v2 > 9:
		v2 = 0
	return str(v1) + str(v2)

def gen_random_cpf():
	""" Generates a random CPF.
	Return:
		The generated CPF.
	"""
	cpf = gen_random_string(9)
	return cpf + compute_cpf_validation(cpf)

def gen_random_cnpj(unit = None):
	""" Generates a random CNPJ.
	Parameter:
		unit -- The number of the unit. It will be random if not set.
	Return:
		The generated CNPJ.
	"""
	cnpj = ''
	if unit == None:
		cnpj = gen_random_string(12)
	else:
		cnpj = gen_random_string(8) + '{0:04d}'.format(unit % 1000)
	return cnpj + compute_cnpj_validation(cnpj)

def format_cpf(cpf):
	""" Formats the CPF as 'xxx.xxx.xxx-xx'.
	Parameter:
		cpf -- The cpf value. It must contain 9 digits.
	Return:
		The formatted CPF.
	"""
	return cpf[0:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:12]

def format_cnpj(cnpj):
	""" Formats the CNPJ as 'xx.xxx.xxx/xxxx-xx'.
	Parameter:
		cnpj -- The cpf value. It must contain 14 digits.
	Return:
		The formatted CNPJ.
	"""
	return cnpj[0:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:14]

def is_cpf_valid(cpf):
	""" Verifies if the given CPF is valid.
	Parameter:
		cpf -- The CPF value. It must be in the format 'xxx.xxx.xxx-xx' or 'xxxxxxxxxxx'.
	Return:
		True if the CPF is valid or false otherwise.
	"""
	if not re.match('^[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}\\-[0-9]{2}$', cpf):
		if not re.match('^[0-9]{11}$', cpf):
			return False
	cpf = remove_non_digits(cpf)
	return cpf[9:12] == compute_cpf_validation(cpf)

def is_cnpj_valid(cnpj):
	""" Verifies if the given CNPJ is valid.
	Parameter:
		cnpj -- The CNPJ value. It must be in the format 'xx.xxx.xxx/xxxx-xx' or 'xxxxxxxxxxxxxx'.
	Return:
		True if the CNPJ is valid or false otherwise.
	"""
	if not re.match('^[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}\\/[0-9]{4}\\-[0-9]{2}$', cnpj):
		if not re.match('^[0-9]{14}$', cnpj):
			return False
	cnpj = remove_non_digits(cnpj)
	return cnpj[12:14] == compute_cnpj_validation(cnpj)

