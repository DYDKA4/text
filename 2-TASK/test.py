import unittest
import re
import solution
class MyTestCase(unittest.TestCase):

    @staticmethod
    def test_html():
        entities = set()
        # regexp = re.compile(solution.SERIES_REGEXP)
        # with open('series/77164.html', 'r') as file:
        #     print(file)
        #     # for match in regexp.finditer(file):
        #     #     for key, value in match.groupdict().items():
        #     #         if value is not None:
        #     #             start, end = match.span(key)
        #     # entities.add((start, end, key))

    def test_PERSONS_REGEXP(self):
        entities = set()
        regexp = re.compile(solution.PERSONS_REGEXP)
        file = str(open('sentences/1.txt', 'r'))
        print(file)
        for match in regexp.finditer(file):
            for key, value in match.groupdict().items():
                if value is not None:
                    start, end = match.span(key)
                    entities.add((start, end, key))
        print(entities)
if __name__ == '__main__':
    unittest.main()
