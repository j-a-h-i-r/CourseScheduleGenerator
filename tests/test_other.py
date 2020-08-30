import unittest
import scheduleGenerator

class TestOverlappingTimes(unittest.TestCase):
    def testTimeConversation(self):
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('8:00'), 480)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('12:30'), 750)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('15:23'), 923)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('18:49'), 1129)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('0:50'), 50)

courseList = [
    {
        'courseCode': 'CSE360',
        'sections': [{
            'section': '1',
            'sectionSchedule': [
                {'start': '10:10', 'end': '11:40', 'day': 'Monday'}, 
                {'start': '10:10', 'end': '11:40', 'day': 'Wednesday'}
            ],
            'labSchedule': [
                {'start': '13:30', 'end': '15:30', 'day': 'Sunday'}
            ]}
        ]
    }, {
        'courseCode': 'CSE365',
        'sections': [{
            'section': '1',
            'sectionSchedule': [
                {'start': '10:10','end': '11:40','day': 'Monday'}, 
                {'start': '10:10','end': '11:40','day': 'Wednesday'}
            ],
            'labSchedule': [
                {'start': '1:30','end': '3:30','day': 'Sunday'}
            ]}, {
                'section': '2',
                'sectionSchedule': [
                    {'start': '10:10','end': '11:40','day': 'Tuesday'}, 
                    {'start': '10:10','end': '11:40','day': 'Thursday'}
                ],
                'labSchedule': [
                    {'start': '13:30','end': '15:30','day': 'Thursday'}
                ]
            }
        ]
    }
]

class TestCombinations(unittest.TestCase):
    def testCombnation(self):
        combs = scheduleGenerator.getAllSectionCombinations(courseList)
        self.assertEqual(len(combs), 2)
        self.assertEqual(combs[0][0]['courseCode'], 'CSE360')
        self.assertEqual(combs[1][1]['section'], '2')

if __name__ == '__main__':
    unittest.main()