from collections import UserDict
from pymongo import MongoClient


def firstTimeUser(email: str):
    client = MongoClient(
        "mongodb+srv://resumeParserAdmin:vijay789@resumeparser.g0dcg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.jobSeekers

    usersDocument = db.users

    if usersDocument.count_documents({'_id': email}, limit=1):
        return False
    else:
        d = {
            "_id": email,

            "firstName": "Vijay",
            "lastName": "Kumar",
            "date_of_birth": "22/12/1999",
            "email_address": "goodemail@gmail.com",
            "phone_number": "8884696920",
            "address_1": "323, BSK 3rd Stage",
            "address_2": "Near Katriguppe Signal",
            "city_name": "Bengaluru",
            "state_name": "Karnataka",
            "pincode": "560085",


            "school_name": "KV Gola Road",
            "school_passing_year": "2017",
            "school_marks": "92.41",


            "college_name": "DSCE",
            "college_marks": "8.78",
            "college_passing_year": "2021",

            "progLanguages":  ["C++", "Python", "JAVA"],
            "techSkills":  ["Clean Coding", "Copy Code From Stack", "Nice Syntax!"],



            "previousExperiences":  ["Blah Blah Experience", "Not Such Good Experience"],
            "previousExperiences_Employer":  ["Google", "Yahoo"],
            "previousExperiences_Start":  ["2000", "2001"],
            "previousExperiences_Stop":  ["2010", "2020"],
            "previousProjects_Summary":  ["Neat Summary1", "Neat Summary2"],
            "previousProjects_Title":  ["Good Project", "A really good project!"],


            "achievements": ["Best Chess Player", "Best Dancer"],
            "certificates":  ["Coursera", "NPTEL", "University Of Duke"],
            "hobbiesAndInterests": ["Snooker", "Cricket", "Chess"],
            "spokenLanguages":  ["English", "Hindi"],


        }
        x = usersDocument.insert_one(d)

        return True


def getUser(email: str):
    client = MongoClient(
        "mongodb+srv://resumeParserAdmin:vijay789@resumeparser.g0dcg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.jobSeekers

    usersDocument = db.users

    myquery = {"_id": email}
    doc = usersDocument.find_one(myquery)
    if doc:
        return doc
    else:
        return False


def updateUser(email: str, d):
    original_data = {"COMPANIES WORKED AT": "Could Not Parse", "SKILLS": "Could Not Parse", "GRADUATION YEAR": "Could Not Parse", "COLLEGE NAME": "Could Not Parse", "DEGREE": "Could Not Parse",
                     "DESIGNATION": "Could Not Parse", "EMAIL ADDRESS": "Could Not Parse", "LOCATION": "Could Not Parse", "NAME": "Could Not Parse", "YEARS OF EXPERIENCE": "Could Not Parse", "UNKNOWN": "Could Not Parse"}
    for item in d:
        original_data[item] = d[item]

    client = MongoClient(
        "mongodb+srv://resumeParserAdmin:vijay789@resumeparser.g0dcg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.jobSeekers

    usersDocument = db.users

    myquery = {"_id": email}
    doc = usersDocument.find_one(myquery)

    allNames = original_data['NAME'].strip().split(" ")

    doc['firstName'] = allNames[0]
    doc['lastName'] = allNames[1]
    allCompanies = original_data['COMPANIES WORKED AT'].strip().split(",")
    doc['previousExperiences_Employer'] = allCompanies
    allSkills = original_data['SKILLS'].strip().split(",")
    doc['techSkills'] = allSkills
    doc['college_passing_year'] = original_data['GRADUATION YEAR']
    doc['address_1'] = original_data['LOCATION']
    doc['college_name'] = original_data['COLLEGE NAME'] + original_data['DEGREE']
    doc['email_address'] = original_data['EMAIL ADDRESS']

    usersDocument.save(doc)

    if doc:
        return doc
    else:
        return False


def submitForm(email: str, data):

    client = MongoClient(
        "mongodb+srv://resumeParserAdmin:vijay789@resumeparser.g0dcg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.jobSeekers

    usersDocument = db.users

    myquery = {"_id": email}

    usersDocument.save(data)
    doc = usersDocument.find_one(myquery)

    if doc:
        return doc
    else:
        return False


def queryAllJobs():
    client = MongoClient(
        "mongodb+srv://resumeParserAdmin:vijay789@resumeparser.g0dcg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.recruiters

    usersDocument = db.allJobs
    res = []

    for docs in usersDocument.find():
        res.append(docs)
    return res


print(queryAllJobs())