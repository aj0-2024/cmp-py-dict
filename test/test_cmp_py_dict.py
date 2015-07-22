import unittest
from app import cmp_py_dict


class TestCmpDict(unittest.TestCase):

    def test_case_1(self):
        old_dict = {1:100, 2:200}
        new_dict = {1:50, 3:200}

        cmpobj = cmp_py_dict.CmpDict(old_dict, new_dict)

        self.assertEqual(cmpobj.new, {'.3'})
        self.assertEqual(cmpobj.modified, {'.1 - [100 -> 50]'})
        self.assertEqual(cmpobj.deleted, {'.2'})

    def test_case_2(self):
        old_dict = {1:{1:50}, 2:{1:50}}
        new_dict = {1:{1:50}, 2:{1:40}}

        cmpobj = cmp_py_dict.CmpDict(old_dict, new_dict)

        self.assertEqual(cmpobj.new, set())
        self.assertEqual(cmpobj.modified, {'.1.2.1 - [50 -> 40]'})
        self.assertEqual(cmpobj.deleted, set())


    def test_case_3(self):
        old_dict = {}
        new_dict = {}

        cmpobj = cmp_py_dict.CmpDict(old_dict, new_dict)

        self.assertEqual(cmpobj.new, set())
        self.assertEqual(cmpobj.modified, set())
        self.assertEqual(cmpobj.deleted, set())

    def test_case_4(self):
        old_dict = {1:[1,2,3]}
        new_dict = {1:[1,2]}

        cmpobj = cmp_py_dict.CmpDict(old_dict, new_dict)

        self.assertEqual(cmpobj.new, set())
        self.assertEqual(cmpobj.modified, {'.1 - [[1, 2, 3] -> [1, 2]]'})
        self.assertEqual(cmpobj.deleted, set())

    def test_case_5(self):
        old_dict = {1:2}
        invalid_input = 'invalid'

        with self.assertRaises(TypeError):
            cmpobj = cmp_py_dict.CmpDict(old_dict, invalid_input)



