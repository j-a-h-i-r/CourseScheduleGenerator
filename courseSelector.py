import copy
import logging

SHOW = logging.DEBUG
HIDE = logging.CRITICAL
logging.basicConfig(format="%(levelname)s: %(message)s", level=HIDE)

courseDict = {
    'cse360': {
        'courseTime': ['5t5r', '6t6r'],
        'hasLab': False  # add lab info here instead of separate dict
    },
    'cse365': {
        'courseTime': ['5m5w', '5s5r'],
        'hasLab': True
    },
    'cse375': {
        'courseTime': ['2m2w', '2s2t', '4s4r'],
        'hasLab': False
    }
}
labDict = {
    'cse360': [],
    'cse365': ['6m', '6s'],
    'cse375': []
}
courseName = sorted(list(courseDict.keys()))
logging.info(courseName)

allCourse = []
allLab = []


def allComb(crsData, labData, courseSoFar, labSoFar, li):
    if li == 3:  # li = list size
        allCourse.append(copy.deepcopy(courseSoFar))
        allLab.append(copy.deepcopy(labSoFar))
        # also works if I write alll.append(combSoFar[:])
        logging.debug(courseSoFar)
        logging.debug(labSoFar)
        return
    name = courseName[li]
    crsInfo = crsData[name]
    for i in range(len(crsInfo['courseTime'])):
        courseSoFar[name] = crsInfo['courseTime'][i]

        if crsInfo['hasLab'] is True:
            labSoFar[name] = labData[name][i]
        else:
            labSoFar[name] = ""
        allComb(crsData, labData, courseSoFar, labSoFar, li + 1)
        courseSoFar.pop(name)
        labSoFar.pop(name)


allComb(courseDict, labDict, {}, {}, 0)
logging.debug(allCourse)
logging.debug(allLab)


def validator(prevTime, crsTimeList):
    """takes a list of course time and check if it is valid"""
    for slot in crsTimeList:
        if slot == "":
            """Empty lab slot. Ignore this"""
            logging.debug(prevTime + "     no lab")
            continue
        elif len(slot) == 2:
            """
            Time slot for a lab class:
                time slot 1 covers time slot 1
                time slot 2 covers both time slot 2 and 3
                time slot 4 covers both time slot 4 and 5
                time slot 6 covers time slot 6
            """
            if slot[0] == '1' or slot[0] == '6':
                """time slot 1. add this again. so 1w becomes 1w1w"""
                slot += slot
            elif slot[0] == '2' or slot[0] == '4':
                """time slot 2/4 will cover 3/5 too. so 2w becomes 2w3w"""
                anotherSlot = str(int(slot[0]) + 1) + slot[1]
                slot += anotherSlot
        if slot[:2] in prevTime or slot[2:] in prevTime:
            return "", False
        else:
            prevTime += slot
    return prevTime, True


def getValidCourse(crsList, labList):
    """
    argument is a list of list of course and lab time
    algo:
    - check if a time is in time slot of previous courses
    - Not in - add it
    - In - this time slot is not valid
    """
    validCourses = []
    validLabs = []
    for crs, lab in zip(crsList, labList):
        tm, isCourseValid = validator("", list(crs.values()))
        if isCourseValid is True:
            """course is valid, check if it still remain if lab is added"""
            tm, isLabValid = validator(tm, list(lab.values()))
            if isLabValid is True:
                validCourses.append(crs)
                validLabs.append(lab)
    return validCourses, validLabs


def printSchedule(courseList, labList):
    days = ['s', 'm', 't', 'w', 'r']
    dayName = {'s': 'Sunday', 'm': 'Monday',
               't': 'Tuesday', 'w': 'Wednesday', 'r': 'Thursday'}
    clsTime = {'1': '08:30 - 10:00', '2': '10:10 - 11:40',
               '3': '11:50 - 01:20', '4': '01:30 - 03:00',
               '5': '03:10 - 04:40', '6': '04:50 - 06:20'}
    labTime = {'1': '8:00 - 10:00', '2': '10:10 - 12:10',
               '4': '1:30 - 3:30', '6': '4:50 - 6:50'}
    classes = {
        's': [], 'm': [], 't': [], 'w': [], 'r': []
    }
    """
    fill up the classes dict with information of class time and course name
    """
    for name, slot in courseList.items():
        if len(slot) == 0:
            """empty class. skip"""
            continue
        elif len(slot) == 2:
            """lab class"""
            classes[slot[1]].append([name + "Lab", slot[0]])
        else:
            """regular class"""
            classes[slot[1]].append([name, slot[0]])
            classes[slot[3]].append([name, slot[2]])
    for name, slot in labList.items():
        if len(slot) == 0:
            """empty class. skip"""
            continue
        elif len(slot) == 2:
            """lab class"""
            classes[slot[1]].append([name + 'Lab', slot[0]])
        else:
            """regular class"""
            classes[slot[1]].append([name, slot[0]])
            classes[slot[3]].append([name, slot[0]])

    for day in days:
        if len(classes[day]) == 0:
            """no class in this day"""
            continue
        print(dayName[day])
        print('-' * len(dayName[day]))
        for crsName, crsTime in sorted(classes[day], key=lambda x: x[1]):
            if crsName.lower().endswith('lab'):
                """This is a lab class. Use labTime to show labs time"""
                print(labTime[crsTime] + " - " + crsName)
            else:
                print(clsTime[crsTime] + " - " + crsName)


validCourse, validLab = getValidCourse(allCourse, allLab)
logging.debug(validCourse)
logging.debug(validLab)

cnt = 0

for cls, lab in zip(validCourse, validLab):
    print("Schedule ", cnt + 1)
    print("========================")
    printSchedule(cls, lab)
    print()
    cnt += 1
