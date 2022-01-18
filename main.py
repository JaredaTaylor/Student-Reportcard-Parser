import sys
import json
import os
'''
AUTHOR: Jared Taylor
Github: jaredataylor

1. reads these .csv files
2. parses them
3. calculates the students final grades and generates the report as a structured JSON file

take csv, convert to json format
'''

# Class for student object
class Student:
    def __init__(self, id, name):
        self.id = int(id)
        self.name = name
        self.marks = {}

    # prints student info, mainly used during testing
    def printStudent(self):
        print('Student ID:', self.id)
        print('Student name:', self.name)
        print('Student Marks:', self.marks)

    # add mark to student's marks
    def addMark(self, testID, mark):
        self.marks[testID] = int(mark)


# Class for course object
class Course:
    def __init__(self, id, subject, teacher):
        self.id = int(id)
        self.name = subject
        self.teacher = teacher
        self.tests = {}

    # prints course info, mainly used during testing
    def printCourse(self):
        print('Course ID:', self.id)
        print('Course Subject:', self.name)
        print('Teacher:', self.teacher)
        print('Tests:', self.tests)

    # add test to course tests
    def addTest(self, testID, weight):
        self.tests[testID] = int(weight)


# Function takes base path and file path and reads the csv in
# Returns list where each index is a line from the file
def cleanLines(basePath):
    path = os.path.join(basePath)
    lineList = []
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            lines = lines[1:]
        file.close
        for line in lines:
            tmp = line.replace('\n', '')
            tmp = tmp.split(',')
            lineList.append(tmp)
    except:
        sys.stderr.write('Invalid file type/no such file or directory\n')
        sys.exit(1)
    
    return lineList


# creates a list of students and creates a student instance for each line in the csv and adds student to list
# returns list of student instances
def readStudents(basePath):
    lines = cleanLines(basePath)
    studentList = []

    # each entry is a student, clean info and create student for studentList
    for line in lines:
        student = Student(line[0], line[1])
        studentList.append(student)

    return studentList

# creates a list of courses and creates a course instance for each line in the csv and adds course to list
# returns list of course instances
def readCourses(basePath):
    lines = cleanLines(basePath)
    courseList = []

    for line in lines:
        course = Course(line[0], line[1], line[2])
        courseList.append(course)

    return courseList

# for each test, add it to the corresponding course
# return altered course list
def readTests(basePath, courseList):
    lines = cleanLines(basePath)
    testList = []

    for line in lines:
        #tmp = line.replace('\n', '')
        #tmp = tmp.split(',')
        for course in courseList:
            #if tmp[1] == course.id:
            if int(line[1]) == course.id:
                course.addTest(line[0], line[2])

    return courseList

# read mark, add to student's marks
# return altered student list
def readMarks(basePath, studentList, classList):
    lines = cleanLines(basePath)
    for line in lines:
        #tmp = line.replace('\n', '')
        #tmp = tmp.split(',')
        for student in studentList:
            #if tmp[1] == student.id:
            if int(line[1]) == student.id:
                student.addMark(line[0], line[2])

    return studentList

# build dict, then write to json file
def writeJson(outputPath, studentList, courseList):
    # build dict
    d = {"students": []}
    for student in studentList:
        stuDict = {}
        stuDict["id"] = student.id
        stuDict["name"] = student.name
        courses = getCourseAverage(student, courseList)
        stuDict["totalAverage"] = round(getTotalAverage(courses), 2)
        stuDict["courses"] = []

        # iterate through all courses
        for course in courseList:
            temp = {}
            found = False

            # if student in course
            if course.id in courses:
                found = True
                temp["id"] = course.id
                temp["name"] = course.name
                temp["teacher"] = course.teacher
                temp["courseAverage"] = round(courses[course.id], 2)

            # course was found, add course info to student dict entry
            if found == True:
                stuDict["courses"].append(temp)
        d["students"].append(stuDict)

    # write to json
    jsonString = json.dumps(d)
    jsonFile = open(outputPath, 'w')
    jsonFile.write(jsonString)
    jsonFile.close()
            

# calculate average for each course a student took
# return dictionary of format {"ID", int(grade)}
def getCourseAverage(student, courseList):
    courseAvgs = {}
    for course in courseList:
        courseMark = 0
        for testID in course.tests:
            cnt = 0
            if testID in student.marks:

                # increment number of tests taken
                cnt += 1
                courseMark += (course.tests.get(testID) / 100) * student.marks.get(testID)

        # if student took tests in course, add grade
        if cnt > 0:
            courseAvgs[course.id] = courseMark
    return courseAvgs


# calculate student's total average over classes they took
# return float of their average mark
def getTotalAverage(marks):
    sum = 0
    for i in marks:
        sum += marks[i]
    return (sum / len(marks))


def main(coursepath, studentpath, testpath, markpath, outputpath):
    studentList = readStudents(studentpath)
    courseList = readCourses(coursepath)
    courseList = readTests(testpath, courseList)
    studentList = readMarks(markpath, studentList, courseList)
    writeJson(outputpath, studentList, courseList)

# validate length
if len(sys.argv) < 6:
    sys.stderr.write('Usage: main.py {course-path} {student-path} {test-path} {mark-path} {output-path}\n')
    sys.exit(1)

elif len(sys.argv) > 6:
    sys.stderr.write('Usage: main.py {course-path} {student-path} {test-path} {mark-path} {output-path}\n')
    sys.exit(1)

else:

    # Get course input path
    coursePath = sys.argv[1]

    # Get student input path
    studentPath = sys.argv[2]

    # Get tests input path
    testPath = sys.argv[3]

    # get marks input path
    markPath = sys.argv[4]
        
    # get output path
    outputPath = sys.argv[5]

    if __name__ == '__main__':
        main(coursePath, studentPath, testPath, markPath, outputPath)


    