# -*- coding: utf-8 -*-
'''
CMP, Compare with Accumulator Test
'''

import unittest

from pynes.compiler import lexical, syntax, semantic

class CpmTest(unittest.TestCase):

    def test_cmp_imm(self):
        tokens = lexical('CMP #$10')
        self.assertEquals(2 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_HEX_NUMBER', tokens[1]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_IMMEDIATE', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xc9, 0x10])

    def test_cmp_imm_with_decimal(self):
        tokens = lexical('CMP #10')
        self.assertEquals(2 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_DECIMAL_NUMBER', tokens[1]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_IMMEDIATE', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xc9, 0x0a])

    def test_cmp_imm_with_binary(self):
        tokens = lexical('CMP #%00000100')
        self.assertEquals(2 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_BINARY_NUMBER', tokens[1]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_IMMEDIATE', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xc9, 0x04])

    def test_cmp_zp(self):
        tokens = lexical('CMP $00')
        self.assertEquals(2 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_ADDRESS', tokens[1]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_ZEROPAGE', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xc5, 0x00])

    def test_cmp_zpx(self):
        tokens = lexical('CMP $10,X')
        self.assertEquals(4 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_ADDRESS', tokens[1]['type'])
        self.assertEquals('T_SEPARATOR', tokens[2]['type'])
        self.assertEquals('T_REGISTER', tokens[3]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_ZEROPAGE_X', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xd5, 0x10])

    def test_cmp_abs(self):
        tokens = lexical('CMP $1234')
        self.assertEquals(2 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_ADDRESS', tokens[1]['type'])
        self.assertEquals('$1234', tokens[1]['value'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_ABSOLUTE', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xcd, 0x34, 0x12])

    def test_cmp_absx(self):
        tokens = lexical('CMP $1234,X')
        self.assertEquals(4 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_ADDRESS', tokens[1]['type'])
        self.assertEquals('$1234', tokens[1]['value'])
        self.assertEquals('T_SEPARATOR', tokens[2]['type'])
        self.assertEquals('T_REGISTER', tokens[3]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_ABSOLUTE_X', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xdd, 0x34, 0x12])

    def test_cmp_absy(self):
        tokens = lexical('CMP $1234,Y')
        self.assertEquals(4 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_ADDRESS', tokens[1]['type'])
        self.assertEquals('T_SEPARATOR', tokens[2]['type'])
        self.assertEquals('T_REGISTER', tokens[3]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_ABSOLUTE_Y', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xd9, 0x34, 0x12])

    def test_cmp_indx(self):
        tokens = lexical('CMP ($20,X)')
        self.assertEquals(6 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_OPEN', tokens[1]['type'])
        self.assertEquals('T_ADDRESS', tokens[2]['type'])
        self.assertEquals('$20', tokens[2]['value'])
        self.assertEquals('T_SEPARATOR', tokens[3]['type'])
        self.assertEquals('T_REGISTER', tokens[4]['type'])
        self.assertEquals('T_CLOSE', tokens[5]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_INDIRECT_X', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xc1, 0x20])

    def test_cmp_indy(self):
        tokens = lexical('CMP ($20),Y')
        self.assertEquals(6 , len(tokens))
        self.assertEquals('T_INSTRUCTION', tokens[0]['type'])
        self.assertEquals('T_OPEN', tokens[1]['type'])
        self.assertEquals('T_ADDRESS', tokens[2]['type'])
        self.assertEquals('T_CLOSE', tokens[3]['type'])
        self.assertEquals('T_SEPARATOR', tokens[4]['type'])
        self.assertEquals('T_REGISTER', tokens[5]['type'])
        ast = syntax(tokens)
        self.assertEquals(1 , len(ast))
        self.assertEquals('S_INDIRECT_Y', ast[0]['type'])
        code = semantic(ast)
        self.assertEquals(code, [0xd1, 0x20])
