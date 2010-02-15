import unittest
import datagen
from datagen import *

class AlgorithmTest(unittest.TestCase):

    def assert_output(self, condition, output):
        """Given a condition and an expected output, asserts the
            datagen module returns that output"""
        data = datagen.get_data(condition)
        for o in output:
            self.assertEqual(data[o], output[o])
        



        
    
    def test_identity(self):
        cond = "x is 7"
        self.assert_output(cond, {"x": 7})
        
    def test_random_identity(self):
        from random import randint
        n = randint(1,100)
        cond = "x is " + str(n)
        self.assert_output(cond, {"x": n})

    def test_not_identity(self):
        cond = "x is not 7"
        x = datagen.get_data(cond).get("x")
        self.assertTrue(x is not 7)

    def test_identity_str(self):
        cond = "sex is 'M'"
        sex = datagen.get_data(cond).get("sex")
        self.assertTrue(sex is 'M')

    def test_not_identity_str(self):
        cond = "sex is not 'M'"
        sex = datagen.get_data(cond).get("sex")
        self.assertTrue(sex is not 'M')




    def test_lt(self):
        cond = "x < 11"
        x = datagen.get_data(cond).get("x")
        self.assertTrue(x < 11)

    def test_gte(self):
        cond = "x >= 104"
        x = datagen.get_data(cond).get("x")
        self.assertTrue(x >= 104)

    def test_inequality_chain(self):
        cond = "18 < age < 70"
        age = datagen.get_data(cond).get("age")
        self.assertTrue(18 < age < 70)
        


        
    def test_meta_boolean_true(self):
        cond = "(age < 100) is True"
        age = datagen.get_data(cond).get("age")
        self.assertTrue((age < 100) is True)
        
    def test_meta_boolean_false(self):
        cond = "(8 < age) is False"
        data = datagen.get_data(cond)
        age = data.get("age")
        self.assertTrue((8 < age) is False)





    def test_inclusion(self):
        cond = "sex in ['M', 'F']"
        sex = datagen.get_data(cond).get("sex")
        self.assertTrue(sex in ['M', 'F'])

    def test_not_inclusion(self):
        cond = "sex not in ['M', 'F']"
        sex = datagen.get_data(cond).get("sex")
        self.assertTrue(sex not in ['M', 'F'])





    def test_length(self):
        cond = "8 <= length(password) <= 20"
        pwd = datagen.get_data(cond).get("password")
        self.assertTrue(8 <= length(pwd) <= 20)

    def test_range(self):
        cond = "length(password) not in range(20,100)"
        pwd = datagen.get_data(cond).get("password")
        self.assertTrue(length(pwd) not in range(20,100))




    def test_and(self):
        cond = "x < 100 and x*x is 36"
        x = datagen.get_data(cond).get("x")
        self.assertTrue(x < 100 and x*x is 36)

    def test_or(self):
        cond = "x is 9 or x is 11"
        x = datagen.get_data(cond).get("x")
        self.assertTrue(x is 9 or x is 11)

    



    def test_relational(self):
        cond = "x > y"
        data = datagen.get_data(cond)
        x = data.get('x')
        y = data.get('y')
        self.assertTrue(x > y)

    def test_relational_chained(self):
        cond = "5 < x < y"
        data = datagen.get_data(cond)
        x = data.get('x')
        y = data.get('y')
        self.assertTrue(5 < x < y)

    def test_relational_and(self):
        cond = "x < 8 and y > x"
        data = datagen.get_data(cond)
        x = data.get('x')
        y = data.get('y')
        self.assertTrue(x < 8 and y > x)

    def test_relational_or(self):
        cond = "x < y or y is 0"
        data = datagen.get_data(cond)
        x = data.get('x')
        y = data.get('y')
        self.assertTrue(x < y or y is 0)

    def test_relational_anjy(self):
        cond = [
            "x > 0",
            "y > 0",
            "x > y"
            ]
        data = datagen.get_data(cond)
        x = data.get('x')
        y = data.get('y')
        self.assertTrue(x > 0)
        self.assertTrue(y > 0)
        self.assertTrue(x > y)




    def test_pick(self):
        cond = [
            "password[0] in letters",
            "length(password) < 10"
            ]
        password = datagen.get_data(cond).get("password")
        self.assertTrue(password[0] in letters)
        self.assertTrue(length(password) < 10)

    def test_pick2(self):
        cond = [
            "password[0] not in symbols",
            ]
        password = datagen.get_data(cond).get("password")
        self.assertTrue(password[0] not in symbols)






    def test_language_addon_contains_letters(self):
        cond = "password contains 4 letters"
        password = datagen.get_data(cond).get("password")
        self.assertTrue(datagen.contains(
                    container = password,
                    lower = 4,
                    upper = None,
                    containee = letters
                ))

    def test_language_addon_contains_symbols(self):
        cond = "password contains 2 symbols"
        password = datagen.get_data(cond).get("password")
        self.assertTrue(datagen.contains(
                    container = password,
                    lower = 2,
                    upper = None,
                    containee = symbols
                ))

    def test_language_addon_contains_digits(self):
        cond = [
            "password contains 5 digits",
            "password contains 10 characters"
            ]
        password = datagen.get_data(cond).get("password")
        self.assertTrue(datagen.contains(
                    container = password,
                    lower = 5,
                    upper = None,
                    containee = digits
                ))

    def test_language_addon_contains_chars(self):
        cond = "password contains 10 characters"
        password = datagen.get_data(cond).get("password")
        self.assertTrue(datagen.contains(
                    container = password,
                    lower = 10,
                    upper = None,
                    containee = characters
                ))

    def test_language_addon_contains_numbers(self):
        cond = "password contains 3 numbers"
        password = datagen.get_data(cond).get("password")
        self.assertTrue(datagen.contains(
                    container = password,
                    lower = 3,
                    upper = None,
                    containee = numbers
                ))
        
    def test_language_addon_contains_special(self):
        cond = "password contains 5 ['a','b','c','d','e','f','g','G']"
        password = datagen.get_data(cond).get("password")
        self.assertTrue(datagen.contains(
                    container = password,
                    lower = 5,
                    upper = None,
                    containee = ['a','b','c','d','e','f','g','G']
                ))

    def test_language_addon_contains_range(self):
        cond = "password contains 5 to 8 letters"
        password = datagen.get_data(cond).get("password")
        self.assertTrue(datagen.contains(
                    container = password,
                    lower = 5,
                    upper = 8,
                    containee = letters
                ))





  



    def test_does_not_repeat(self):
        cond = "password does not repeat"
        p = datagen.get_data(cond).get("password")
        self.assertTrue(
            not any(p[i] == p[i+1] for i in xrange(len(p)-1))
        )
        
        




    def test_complex(self):
        cond = "0 < x < y < 100 or (x is 50 and y is 50)"
        data = datagen.get_data(cond)
        x = data.get('x')
        y = data.get('y')
        self.assertTrue(0 < x < y < 100 or (x is 50 and y is 50))

    def test_flattness_of_input(self):
        flat_cond = "x > 10"
        nonflat_cond = ["x > 10"]

        self.assertEquals(
                datagen.get_data(flat_cond).get('x') > 10,
                datagen.get_data(nonflat_cond).get('x') > 10
            )




    def test_real_password_case(self):
        conds = [
            "6 <= length(password) <= 12",
            "password contains 1 letter",
            "password contains 1 number+symbol",
            "password does not repeat"
            ]

        p = datagen.get_data(conds).get("password")

        self.assertTrue(6 <= length(p) <= 12)
        self.assertTrue(datagen.contains(
                    container = p,
                    lower = 1,
                    upper = None,
                    containee = letters
                ))
        self.assertTrue(
            datagen.contains(
                    container = p,
                    lower = 1,
                    upper = number,
                    containee = letters
                )

            or
            datagen.contains(
                    container = p,
                    lower = 1,
                    upper = number,
                    containee = letters
                )

            )

        flag = False
        for i in xrange(len(p)-1):
            if p[i] == p[i+1]:
                flag = True
        self.assertTrue(flag is False)
        




