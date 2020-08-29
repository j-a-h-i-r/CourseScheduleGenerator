import logging
import itertools
import pprint
from functools import cmp_to_key

import data

pp = pprint.PrettyPrinter(indent=4, compact=False)

SHOW = logging.DEBUG
HIDE = logging.CRITICAL
logging.basicConfig(format="%(levelname)s: %(message)s", level=HIDE)

def getAllSectionCombinations(courses: list) -> list:
    '''
    Return all possible combinations of the sections of different courses
    '''
    sections = []
    for course in courses:
        courseSections = []
        courseCode = course['courseCode']
        for section in course['sections']:
            section['courseCode'] = courseCode
            courseSections.append(section)
        sections.append(courseSections)
    sectionCombinations = list(itertools.product(*sections))
    return sectionCombinations

def convertHhMmToMinutes(hhMMStr: str) -> int:
    '''
    Take a time in string in HH:MM format and convert it to minutes
    '''
    hh, mm = hhMMStr.split(':')
    hhInt, mmInt = map(int, [hh, mm])
    minutes = hhInt*60 + mmInt
    return minutes

def cmpByStartTime(time1: dict, time2: dict) -> int:
    '''
    A custom comparator function for sorting schedules based on start time
    time1: A schedule containing `start` and `end` time in `HH:MM` format
    '''
    time1Start = time1['start']
    time2Start = time2['start']
    time1StartInMinutes = convertHhMmToMinutes(time1Start)
    time2StartInMinutes = convertHhMmToMinutes(time2Start)
    return time1StartInMinutes - time2StartInMinutes

def isOverlappingTimesForSingleDay(times: list) -> bool:
    '''
    Check if the times are overlapping. `times` contain the schedule of sections
    for a single day.
    times: 
        - [{start: '10:10', end: '11:40'}]
    '''
    sortedTimes = sorted(times, key=cmp_to_key(cmpByStartTime))
    for i in range(1, len(sortedTimes)):
        if sortedTimes[i-1]['end'] > sortedTimes[i]['start']:
            return True 
    return False

def isOverlappingSchedule(schedulesPerDay: dict) -> bool:
    '''
    Get schedules per day and check if it has any overlapping schedule.
    schedulesPerDay: 
        - {'Monday: [{start: '10:10', end: '11:40'}]}
    '''
    for day in schedulesPerDay:
        isOverlapping = isOverlappingTimesForSingleDay(schedulesPerDay[day])
        if isOverlapping:
            return True
    return False

def isCombinationOfSectionsValid(sectionCombination: list) -> bool:
    '''
    Validate a section combination. A combination is valid if it does not 
    have any overlapping time.
    '''
    schedulePerDay = {}
    for section in sectionCombination:
        sectionSchedules = section['sectionSchedule']
        labSchedules = section.get('labSchedule', [])
        allSchedules = sectionSchedules + labSchedules
        
        for schedule in allSchedules:
            day = schedule.get('day')
            startTime = schedule.get('start')
            endTime = schedule.get('end')
            scheduleDict = {
                'start': startTime,
                'end': endTime
            }
            if day in schedulePerDay:
                schedulePerDay[day].append(scheduleDict)
            else:
                schedulePerDay[day] = [scheduleDict]

    scheduleIsOverlapping = isOverlappingSchedule(schedulePerDay)
    return not scheduleIsOverlapping

def getCourseCombinations(courseList: list) -> list:
    '''
    Get valid section combinations from course list
    '''
    sectionCombinations = getAllSectionCombinations(courseList)
    validCombinations = []
    for sectionCombination in sectionCombinations:
        combinationValid = isCombinationOfSectionsValid(sectionCombination)
        if combinationValid:
            validCombinations.append(sectionCombination)
    return validCombinations

def printSchedule(sections: list):
    '''
    Print a basic schedule
    '''
    schedulePerDay = dict()
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
            if day in schedulePerDay:
                schedulePerDay[day].append(scheduleDict)
            else:
                schedulePerDay[day] = [scheduleDict]
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
            if day in schedulePerDay:
                schedulePerDay[day].append(scheduleDict)
            else:
                schedulePerDay[day] = [scheduleDict]

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    for day in days:
        scheduleInDay = schedulePerDay.get(day, [])
        scheduleInDaySorted = sorted(scheduleInDay, key=cmp_to_key(cmpByStartTime))
        print(day)
        print('-' * len(day))
        for schedule in scheduleInDaySorted:
            start = schedule['start']
            end = schedule['end']
            isLab = schedule.get('isLab')
            courseCode = schedule['courseCode']
            section = schedule['section']
            if isLab:
                print(courseCode, section, start, end, '(Lab)')
            else:
                print(courseCode, section, start, end)

if __name__ == '__main__':
    courseDict = data.getTestData()
    validSectionCombinations = getCourseCombinations(courseDict)
    for i, sectionCombination in enumerate(validSectionCombinations, 1):
        header = f'Schedule {i}'
        print(header)
        print('-' * len(header))
        printSchedule(sectionCombination)
        print()
