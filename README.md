[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/j-a-h-i-r/CourseScheduleGenerator) 

# Course-Schedule-Generator
Hobby project to generate course all possible schedule from course and lab time

Data Format:
```
[
    {
        'courseCode': '<Code of the Course>',
        'sections': [
            {
                'section': '<Section Number>',
                'sectionSchedule': [
                    {
                        'start': '10:10',  // Start Time in 24hr HH:MM format
                        'end': '11:40',    // End Time of the Course
                        'day': 'Monday' 
                    }, {
                        'start': '10:10',  
                        'end': '11:40',
                        'day': 'Wednesday' // Sections are usually held twice a week
                    }
                ],
                'labSchedule': [          // Add a `labSchedule` key if the course has Lab
                    {
                        'start': '13:30',
                        'end': '15:30',
                        'day': 'Sunday'
                    }
                ]
            }
        ]
    }, {
         // More courses and sections ...
    }
]
```

TODO:
1. Add a converter function to convert course schedule format of different universities to this common format
2. Add a web interface