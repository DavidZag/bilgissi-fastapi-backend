from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import datetime
from fastapi.encoders import jsonable_encoder
from bson.json_util import dumps



#Database Stuff
client = pymongo.MongoClient("mongodb+srv://admin:bilgissi@bilgissi.hlcbf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.assistant
chats_collection = db.chats

#Schemas for API

class Message(BaseModel):
    user_id:int
    conversation_id:int
    message_id:int
    timestamp:str
    question:str


class retrieveConversationsReq(BaseModel):
    user_id:int


class retrieveMessagesReq(BaseModel):
    user_id:int
    conversation_id:int


app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "FastAPI"}

@app.post('/retrieveConversations')
async def retrieve_Conversations_By_User(request: retrieveConversationsReq):
    user_id = request.user_id
    res = list(chats_collection.find({"user_id":user_id}))
    res = [i["conversation_id"] for i in res]
    return res

@app.post('/getMessages')
async def get_Messages_By_Convo(request: retrieveMessagesReq):
    user_id = request.user_id
    conv_id = request.conversation_id
    res = list(chats_collection.find({"conversation_id":conv_id, "user_id":user_id}))
    json_res = dump(res)
    return json_res

@app.post('/writeMessage')
async def answer_question(message: Message):
    message_json = jsonable_encoder(message)
    chats_collection.insert_one(message_json)
    return 2