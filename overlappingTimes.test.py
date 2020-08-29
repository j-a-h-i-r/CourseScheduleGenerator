import unittest

import courseSelector

nonOverLappingTimes = [
    {'start': '10:10', 'end': '11:40'},
    {'start': '1:30', 'end': '3:00'},
    {'start': '4:50', 'end': '6:50'},
    {'start': '8:30', 'end': '10:00'},
]

overlappingTimes = [
    {'start': '10:10', 'end': '11:40'},
    {'start': '1:30', 'end': '3:00'},
    {'start': '1:30', 'end': '3:30'},
]

class TestOverlappingTimes(unittest.TestCase):
    def testNonOverlapping(self):
        self.assertFalse(courseSelector.isOverlappingTimes(nonOverLappingTimes))
    
    def testOverlapping(self):
        self.assertTrue(courseSelector.isOverlappingTimes(overlappingTimes))


if __name__ == '__main__':
    unittest.main()