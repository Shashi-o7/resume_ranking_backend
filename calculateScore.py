from collections import UserDict
from pymongo import MongoClient
import json





def calcScore(email:str):
    client = MongoClient(
        "mongodb+srv://resumeParserAdmin:vijay789@resumeparser.g0dcg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.jobSeekers

    usersDocument = db.users

    myquery = {"_id": email}
    doc = usersDocument.find_one(myquery)
    schoolMarks = float(doc['school_marks'])
    collegeMarks = float(doc['college_marks'])
    progLanguages = doc['progLanguages']
    techSkills = doc['techSkills']
    prevExpStop = (doc['previousExperiences_Stop'])
    prevExpStart = (doc['previousExperiences_Start'])
    totalYears = 0
    for i in range(len(prevExpStart)):
        totalYears+=(int(prevExpStop[i])-int(prevExpStart[i]))

    client = MongoClient(
        "mongodb+srv://resumeParserAdmin:vijay789@resumeparser.g0dcg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.recruiters

    usersDocument = db.allJobs
    jobSeekerArray=[]

    for docs in usersDocument.find():
       
        data = (docs['requirements'])
        requiredExperience = int(data['totalYears'])
        requiredSchoolMarks =  float(data['schoolMarks'])
        requiredCollegeMarks =  float(data['collegeMarks'])
        requiredLanguages = data['progLanguages']
        requiredSkills= data['techSkills']

        totalScore=0

        if totalYears >=requiredExperience:
            totalYears = requiredExperience
        totalScore += 30*(totalYears/requiredExperience)

        if schoolMarks >= requiredSchoolMarks:
            schoolMarks = requiredSchoolMarks
        totalScore += 10*(schoolMarks/requiredSchoolMarks)

        if collegeMarks >= requiredCollegeMarks:
            collegeMarks = requiredCollegeMarks
        totalScore += 10*(collegeMarks/requiredCollegeMarks)

        langCount, skillCount=0,0

        for lang in requiredLanguages:
            if lang in progLanguages:
                langCount+=1

        totalScore+= 25*(langCount/len(requiredLanguages))

        for skill in requiredSkills:
            if skill in techSkills:
                skillCount+=1
        
        totalScore += 25*(skillCount/len(requiredSkills))

        jobSeekerArray.append(totalScore)
    
    return jobSeekerArray

        


print(calcScore('refined@gmail.com'))