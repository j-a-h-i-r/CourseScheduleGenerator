import logging
import itertools
import pprint
from functools import cmp_to_key

pp = pprint.PrettyPrinter(indent=4, compact=False)

SHOW = logging.DEBUG
HIDE = logging.CRITICAL
logging.basicConfig(format="%(levelname)s: %(message)s", level=HIDE)

courseDict = {
    'CSE360': {
        'sections': [
            {
                'section': '1',
                'sectionSchedule': [
                    {
                        'start': '10:10',
                        'end': '11:40',
                        'day': 'Monday'
                    }, {
                        'start': '10:10',
                        'end': '11:40',
                        'day': 'Wednesday'
                    }
                ],
                'labSchedule': [
                    {
                        'start': '13:30',
                        'end': '15:30',
                        'day': 'Sunday'
                    }
                ]
            }
        ]
    },
    'CSE365': {
        'sections': [
            {
                'section': '1',
                'sectionSchedule': [
                    {
                        'start': '10:10',
                        'end': '11:40',
                        'day': 'Monday'
                    }, {
                        'start': '10:10',
                        'end': '11:40',
                        'day': 'Wednesday'
                    }
                ],
                'labSchedule': [
                    {
                        'start': '1:30',
                        'end': '3:30',
                        'day': 'Sunday'
                    }
                ]
            }, {
                'section': '2',
                'sectionSchedule': [
                    {
                        'start': '10:10',
                        'end': '11:40',
                        'day': 'Tuesday'
                    }, {
                        'start': '10:10',
                        'end': '11:40',
                        'day': 'Thursday'
                    }
                ],
                'labSchedule': [
                    {
                        'start': '13:30',
                        'end': '15:30',
                        'day': 'Thursday'
                    }
                ]
            }
        ]
    },
    'CSE375': {
        'sections': [
            {
                'section': '1',
                'sectionSchedule': [
                    {
                        'start': '10:10',
                        'end': '11:40',
                        'day': 'Sunday'
                    }, {
                        'start': '8:30',
                        'end': '10:00',
                        'day': 'Wednesday'
                    }
                ],
                'labSchedule': [
                    {
                        'start': '8:00',
                        'end': '10:00',
                        'day': 'Sunday'
                    }
                ]
            }
        ]
    }
}


def getAllCourseCombinations(courseDict):
    sections = []
    for course in courseDict:
        courseSections = []
        for section in courseDict[course]['sections']:
            section['courseCode'] = course
            courseSections.append(section)
        sections.append(courseSections)
    sectionCombinations = list(itertools.product(*sections))
    return sectionCombinations

def convertHhMmToMinutes(hhMMStr: str) -> int:
    hh, mm = hhMMStr.split(':')
    hhInt = int(hh)
    mmInt = int(mm)
    minutes = hhInt*24 + mmInt
    return minutes

def cmpByStartTime(time1: str, time2: str):
    '''
    time1: time in HH:MM format
    '''
    time1Start = time1['start']
    time2Start = time2['start']
    time1StartInMinutes = convertHhMmToMinutes(time1Start)
    time2StartInMinutes = convertHhMmToMinutes(time2Start)
    return time1StartInMinutes - time2StartInMinutes

def isOverlappingTimes(times: list):
    '''
    Check if the times are overlapping.
    times - [{start: '10:10', end: '11:40'}]
    '''

    # Convert HH:MM times to minute only. This will make the comparision easier
    sortedTimes = sorted(times, key=cmp_to_key(cmpByStartTime))
    for i in range(1, len(sortedTimes)):
        if sortedTimes[i-1]['end'] > sortedTimes[i]['start']:
            return True 
    return False

def isOverlappingSchedule(schedulesByDay: dict):
    '''
    Get a schedules by day and check if it has any overlapping schedule
    Schedule Format: {start: '10:10', end: '11:40'}
    '''
    for day in schedulesByDay:
        isOverlapping = isOverlappingTimes(schedulesByDay[day])
        if isOverlapping:
            return True
    return False

def isCombinationValid(sectionCombination):
    '''
    Validate a section combination. A combination is valid if it does not 
    have any overlapping time.
    '''
    timesByDay = {}
    for section in sectionCombination:
        sectionSchedules = section['sectionSchedule']
        for schedule in sectionSchedules:
            day = schedule.get('day')
            startTime = schedule.get('start')
            endTime = schedule.get('end')
            if day in timesByDay:
                timesByDay[day].append({
                    'start': startTime,
                    'end': endTime
                })
            else:
                timesByDay[day] = [{
                    'start': startTime,
                    'end': endTime
                }]
        labSchedules = section.get('labSchedule', [])
        for labSchedule in labSchedules:
            day = labSchedule.get('day')
            startTime = labSchedule.get('start')
            endTime = labSchedule.get('end')
            scheduleDict = {
                'start': startTime,
                'end': endTime
            }
            if day in timesByDay:
                timesByDay[day].append(scheduleDict)
            else:
                timesByDay[day] = [scheduleDict]
    isOverlapping = isOverlappingSchedule(timesByDay)
    return not isOverlapping

def getCourseCombinations(courseDict):
    sectionCombinations = getAllCourseCombinations(courseDict)
    validCombinations = []
    for sectionCombination in sectionCombinations:
        combinationValid = isCombinationValid(sectionCombination)
        if combinationValid:
            validCombinations.append(sectionCombination)
    return validCombinations

def printSchedule(sections):
    # print(sections)
    scheduleByDay = dict()
    for section in sections:
        sectionNumber = section['section']
        courseCode = section['courseCode']
        sectionSchedules = section['sectionSchedule']
        labSchedules = section.get('labSchedule', [])

        for sectionSchedule in sectionSchedules:
            startTime = sectionSchedule['start']
            endTime = sectionSchedule['end']
            day = sectionSchedule['day']
            scheduleDict = {
                'start': startTime,
                'end': endTime,
                'section': sectionNumber,
                'courseCode': courseCode
            }
            if day in scheduleByDay:
                scheduleByDay[day].append(scheduleDict)
            else:
                scheduleByDay[day] = [scheduleDict]
        for labSchedule in labSchedules:
            startTime = labSchedule['start']
            endTime = labSchedule['end']
            day = labSchedule['day']
            scheduleDict = {
                'start': startTime,
                'end': endTime,
                'section': sectionNumber,
                'courseCode': courseCode,
                'isLab': True
            }
            if day in scheduleByDay:
                scheduleByDay[day].append(scheduleDict)
            else:
                scheduleByDay[day] = [scheduleDict]

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    for day in days:
        scheduleInDay = scheduleByDay.get(day, [])
        scheduleInDaySorted = sorted(scheduleInDay, key=cmp_to_key(cmpByStartTime))
        print(day)
        print('-' * len(day))
        for schedule in scheduleInDaySorted:
            start = schedule['start']
            end = schedule['end']
            isLab = schedule.get('isLab')
            courseCode = schedule['courseCode']
            section = schedule['section']
            print(courseCode, section, start, end)

if __name__ == '__main__':
    validSectionCombinations = getCourseCombinations(courseDict)
    for i, sectionCombination in enumerate(validSectionCombinations, 1):
        header = f'Schedule {i}'
        print(header)
        print('-' * len(header))
        printSchedule(sectionCombination)
        print()
