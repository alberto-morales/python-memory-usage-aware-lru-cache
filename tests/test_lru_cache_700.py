import unittest
from unittest.mock import patch, call
from decorators.lru_cache import lru_cache
from collections import namedtuple

class TestLRUCacheHelper700:

    def _get_from_diccionario_expensive_function(self, key):
        raise Exception("This should not happen")

    @lru_cache(used_memory_max_size=700)
    def get_from_diccionario_cached(self, key):
        return self._get_from_diccionario_expensive_function(key)

_TestFixture = namedtuple("TestFixture", ["keyset", "expected_calls", "expected_hits", "expected_misses"])

class TestLRUCache700(unittest.TestCase):
    _STRING_LENGTH = 10000

    def create_fixtures_for_test(self):
        keySet = ['1', '2', '3', '4', '1', '2', '3', '4', '5']
        expected_calls = [call('1'), call('2'), call('3'), call('4'), call('5')]
        expected_hits = 4
        expected_misses = 5
        first =  _TestFixture(keySet, expected_calls, expected_hits, expected_misses)
        fixtures = [first]
        return fixtures

    @patch.object(TestLRUCacheHelper700, '_get_from_diccionario_expensive_function', return_value = 'x' * _STRING_LENGTH)
    def test_lru_cache(self, moc_get_from_diccionario_expensive_function):
        """ FIXTURE(s) """
        set_of_fixtures = self.create_fixtures_for_test()
        for fixture in set_of_fixtures:
            key_set = fixture.keyset
            expected_calls = fixture.expected_calls
            expected_hits = fixture.expected_hits
            expected_misses = fixture.expected_misses
            """ SUT """
            obj = TestLRUCacheHelper700()
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