import unittest

import scheduleGenerator

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

nonOverlappingSchedule1 = {
    'Monday': [
        {'start': '8:10', 'end': '10:50'},
        {'start': '12:10', 'end': '3:50'},
    ],
    'Tuesday': [
        {'start': '4:50', 'end': '5:50'}
    ],
    'Wednesday': [
        {'start': '1:15', 'end': '1:20'}
    ]
}
nonOverlappingSchedule2 = {
    'Monday': [
        {'start': '10:10', 'end': '12:50'},
        {'start': '15:10', 'end': '17:50'},
    ],
    'Tuesday': [
        {'start': '9:50', 'end': '10:50'}
    ],
    'Wednesday': [
        {'start': '13:15', 'end': '20:20'}
    ]
}
overlappingSchedule1 = {
    'Monday': [
        {'start': '8:10', 'end': '10:50'},
        {'start': '10:10', 'end': '13:50'},
    ],
    'Tuesday': [
        {'start': '4:50', 'end': '5:50'}
    ],
    'Wednesday': [
        {'start': '1:15', 'end': '1:20'}
    ]
}

class TestOverlappingTimes(unittest.TestCase):
    def testNonOverlapping(self):
        self.assertFalse(scheduleGenerator.isOverlappingTimesForSingleDay(nonOverLappingTimes))
    
    def testOverlapping(self):
        self.assertTrue(scheduleGenerator.isOverlappingTimesForSingleDay(overlappingTimes))
    
    def testisOverlappingSchedule(self):
        self.assertFalse(scheduleGenerator.isOverlappingSchedule(nonOverlappingSchedule1))
        self.assertFalse(scheduleGenerator.isOverlappingSchedule(nonOverlappingSchedule2))
        self.assertTrue(scheduleGenerator.isOverlappingSchedule(overlappingSchedule1))

if __name__ == '__main__':
    unittest.main()