from fastapi import FastAPI, Request
import spacy
import pickle
from downloadPDF import savePDF
from dbConnection import *
import fitz
from calculateScore import calcScore
from fastapi.middleware.cors import CORSMiddleware


nlp = spacy.blank('en')
train_data = pickle.load(open('train_data.pkl', 'rb'))
nlp_model = spacy.load('nlp_model')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parsePDF/")
async def root(request: Request):
    requestJSON = await request.json()
    pdfURL = requestJSON['pdfURL']
    email = requestJSON['email']
    savePDF(pdfURL)
    fname = 'resume.pdf'
    doc = fitz.open(fname)
    text = ""
    for page in doc:
        text = text + str(page.getText())

    tx = " ".join(text.split('\n'))
    doc = nlp_model(tx)
    r = {}
    r['url'] = pdfURL
    for ent in doc.ents:
        rKey = ent.label_.upper()
        rValue = ent.text
        r[rKey] = rValue

    updateUser(email, r)

    return r


@app.post("/checkUser/")
async def root(request: Request):
    emailJSON = await request.json()
    email = emailJSON['email']
    res = firstTimeUser(email)
    r = {}
    if res:
        r['status'] = 'true'
    else:
        r['status'] = 'false'
    return r


@app.post("/fetchUser/")
async def root(request: Request):
    emailJSON = await request.json()
    email = emailJSON['email']
    res = getUser(email)
    if res:
        return res
    else:
        return {'status': 'userNotAvailable'}


@app.post("/submitUser/")
async def root(request: Request):
    emailJSON = await request.json()
    email = emailJSON['email']
    data = emailJSON['formValue']

    res = submitForm(email, data)
    if res:
        return res
    else:
        return {'status': 'userNotAvailable1'}


@app.post("/getJobInfo/")
async def root(request: Request):
    emailJSON = await request.json()
    email = emailJSON['email']
    res = queryAllJobs()
    r = {}

    r['data'] = res
    r['score'] = calcScore(email)

    if res:
        return r
    else:
        return {'status': 'userNotAvailable1'}
