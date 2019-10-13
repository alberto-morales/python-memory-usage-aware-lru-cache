import unittest
from parameterized import parameterized
from unittest.mock import patch, call
from decorators.lru_cache import lru_cache
import sys

class TestLRUCacheHelper700:

    def _get_from_diccionario_expensive_function(self, key):
        raise Exception("This should not happen")

    @lru_cache(used_memory_max_size=700)
    def get_from_diccionario_cached(self, key):
        return self._get_from_diccionario_expensive_function(key)

class TestLRUCache(unittest.TestCase):
    _STRING_LENGTH = 10000

    @patch.object(TestLRUCacheHelper700, '_get_from_diccionario_expensive_function', return_value = 'x' * _STRING_LENGTH)
    def test_lru_cache_1(self, moc_get_from_diccionario_expensive_function):
        """ FIXTURE """
        keySet =  ['1','2','3','4','1','2','3','4','5']
        """ SUT """
        obj = TestLRUCacheHelper700()
        sut = obj.get_from_diccionario_cached
        """ test """
        for key in keySet:
            sut(key)
        """ assertions """
        expected_calls = [call('1'), call('2'), call('3'), call('4'), call('5')]
        actual_calls = moc_get_from_diccionario_expensive_function.call_args_list
        assert (len(actual_calls) == len(expected_calls))
        assert actual_calls == expected_calls
        cache_info = obj.get_from_diccionario_cached.cache_info()
        assert 4 == cache_info.hits
        assert 5 == cache_info.misses
        assert cache_info.maxsize is None

if __name__ == '__main__':
    unittest.main()