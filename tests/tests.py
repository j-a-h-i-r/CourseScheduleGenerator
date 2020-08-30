import unittest
import scheduleGenerator

class TestOverlappingTimes(unittest.TestCase):
    def testTimeConversation(self):
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('8:00'), 480)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('12:30'), 750)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('15:23'), 923)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('18:49'), 1129)
        self.assertEqual(scheduleGenerator.convertHhMmToMinutes('0:50'), 50)

if __name__ == '__main__':
    unittest.main()