import unittest
from unittest.mock import patch, call
from decorators.lru_cache import lru_cache
from collections import namedtuple

class TestLRUCacheHelper3:

    def _get_from_diccionario_expensive_function(self, key):
        raise Exception("This should not happen")

    @lru_cache(used_memory_max_size=30000)
    def get_from_diccionario_cached(self, key):
        return self._get_from_diccionario_expensive_function(key)

class TestLRUCacheHelper7:

    def _get_from_diccionario_expensive_function(self, key):
        raise Exception("This should not happen")

    @lru_cache(used_memory_max_size=70000)
    def get_from_diccionario_cached(self, key):
        return self._get_from_diccionario_expensive_function(key)

_TestFixture = namedtuple("TestFixture", ["obj", "keyset", "expected_calls", "expected_hits", "expected_misses"])

def create_fixtures_for_test_7():
    obj1 = TestLRUCacheHelper7()
    keySet1 = ['1', '2', '3', '4', '1', '2', '3', '4', '5']
    expected_calls1 = [call('1'), call('2'), call('3'), call('4'), call('5')]
    expected_hits1 = 4
    expected_misses1 = 5
    first = _TestFixture(obj1, keySet1, expected_calls1, expected_hits1, expected_misses1)
    #
    #
    fixtures = [first]
    return fixtures

def create_fixtures_for_test_3():
    obj1 = TestLRUCacheHelper3()
    keySet1 = ['1', '2', '3', '4', '1', '2', '3', '4', '5']
    expected_calls1 = [call('1'), call('2'), call('3'), call('4'), call('1'), call('2'), call('3'), call('4'), call('5')]
    expected_hits1 = 0
    expected_misses1 = 9
    first =  _TestFixture(obj1, keySet1, expected_calls1, expected_hits1, expected_misses1)
    #
    obj2 = TestLRUCacheHelper3()
    keySet2 = ['1', '2', '3', '4', '3']
    expected_calls2 = [call('1'), call('2'), call('3'), call('4')]
    expected_hits2 = 1
    expected_misses2 = 4
    second = _TestFixture(obj2, keySet2, expected_calls2, expected_hits2, expected_misses2)
    #
    fixtures = [first, second]
    return fixtures

class TestLRUCache(unittest.TestCase):
    _STRING_LENGTH = 10000

    @patch.object(TestLRUCacheHelper7, '_get_from_diccionario_expensive_function', return_value = 'x' * _STRING_LENGTH)
    def test_lru_cache_7(self, moc_get_from_diccionario_expensive_function):
        """ FIXTURE(s) """
        set_of_fixtures = create_fixtures_for_test_7()
        self.main_test_body(moc_get_from_diccionario_expensive_function, set_of_fixtures)

    @patch.object(TestLRUCacheHelper3, '_get_from_diccionario_expensive_function', return_value = 'x' * _STRING_LENGTH)
    def test_lru_cache_3(self, moc_get_from_diccionario_expensive_function):
        """ FIXTURE(s) """
        set_of_fixtures = create_fixtures_for_test_3()
        self.main_test_body(moc_get_from_diccionario_expensive_function, set_of_fixtures)

    def main_test_body(self, moc_get_from_diccionario_expensive_function, set_of_fixtures):
        for fixture in set_of_fixtures:
            moc_get_from_diccionario_expensive_function.reset_mock()
            key_set = fixture.keyset
            expected_calls = fixture.expected_calls
            expected_hits = fixture.expected_hits
            expected_misses = fixture.expected_misses
            """ SUT """
            obj = fixture.obj
            obj.get_from_diccionario_cached.cache_clear()
            sut = obj.get_from_diccionario_cached
            """ test """
            for key in key_set:
                sut(key)
            """ assertions """
            actual_calls = moc_get_from_diccionario_expensive_function.call_args_list
            assert (len(actual_calls) == len(expected_calls))
            assert actual_calls == expected_calls
            cache_info = obj.get_from_diccionario_cached.cache_info()
            assert expected_hits == cache_info.hits
            assert expected_misses == cache_info.misses
            assert cache_info.maxsize is None


if __name__ == '__main__':
    unittest.main()