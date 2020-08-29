import unittest
import courseSelector

class TestOverlappingTimes(unittest.TestCase):
    def testTimeConversation(self):
        self.assertEqual(courseSelector.convertHhMmToMinutes('8:00'), 480)
        self.assertEqual(courseSelector.convertHhMmToMinutes('12:30'), 750)
        self.assertEqual(courseSelector.convertHhMmToMinutes('15:23'), 923)
        self.assertEqual(courseSelector.convertHhMmToMinutes('18:49'), 1129)
        self.assertEqual(courseSelector.convertHhMmToMinutes('0:50'), 50)

if __name__ == '__main__':
    unittest.main()