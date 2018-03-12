'''
Helpers for dynamically generated tests.

'''
# allow mixed snake/camel case in this file
# pylint: disable=invalid-name

def create_assertRaises(expect, constructor, *args, **kwargs):
    '''generate a :meth:`unittest.TestCase.assertRaises`
    ready to be "inserted" to a TestCase class
    '''
    def do_test(self):
        '''automatically generated method
        '''
        with self.assertRaises(expect):
            constructor(*args, **kwargs)
    return do_test


def create_assertEqual(expect, constructor, *args, **kwargs):
    '''generate a :meth:`unittest.TestCase.assertEqual`
    ready to be "inserted" to a TestCase class
    '''
    def do_test(self):
        '''automatically generated method
        '''
        result = constructor(*args, **kwargs)
        self.assertEqual(
            expect,
            result,
            'expected: {!r}, got: {!r}'.format(expect, result)
        )
    return do_test
