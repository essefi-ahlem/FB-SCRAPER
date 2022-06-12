from facebook_scraper import get_posts
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


def connect_db(connection_string,verbose=False):
    '''Connect to Database. 
    Args: 
        connection_string: str
    Return:
        db: Pymongo session to the db
    '''
    try:
        clt = MongoClient(connection_string)
        db = clt["fb_scraper"]
        if verbose:
            print("The database was loaded. list of collections:\n",db.list_collection_names())
        return db
    except Exception as err:
        print(err)
        
class ScrapePostSchema(BaseModel):
    '''
    Request Model for scraping posts from nintendo facebook page.
    args:   pages: nbr of pages to scrape
            extra_info: bool, get the post reactions if true
            options: a dict of options. Exemple: Set options={"comments": True} to extract comments
    '''
    pages: int = 1
    extra_info: Optional[bool] = False
    options: Optional[dict]

class FindPostSchema(BaseModel):
    '''
    Request Model for scraping.
    Refer to pymongo and mongodb documentation for further details.

    Fileds:
        fields: fieldnames to be retrieved for each document
        query: find the post by post_id
    '''
    fields: dict = { "post_id": 1, "text": 1,"likes":1, "comments":1} #return these fields
    query: dict = {"post_id":"5366122223472187"}


class DeletePost(BaseModel):
    delete_one: bool = False
    query: dict = {"post_id":"5366122223472187"}

app = FastAPI()
load_dotenv(".env")
connection_string = os.environ.get("DB_CONNECTION")
db = connect_db(connection_string=connection_string ,verbose=True)

@app.get("/")
async def root():
    ''' A route for a simple test'''
    return {"message": "Hello World"}


@app.post("/extract_posts") 
async def extract_posts(request: ScrapePostSchema):
    ''' 
    Scrape posts according to the ScrapePostSchema and insert them to database.
    '''
    request = json.loads(request.json())
    for post in get_posts('nintendo',**request):
        db.posts.insert_one(post)
    return {"req": request}
           
@app.post("/find_posts")
async def find_posts(request: FindPostSchema):

    ''' Find posts required fields specified in FindPostSchema using the id  '''
    try:
        request = json.loads(request.json())

        query = request['query']
        fields = request['fields']
        fields['_id'] = fields.get('_id',0)

        ls_posts = db.posts.find(query,fields)
        ls_posts= list(ls_posts)
        return {"posts":ls_posts}

    except Exception as e:
        return {"Exception":str(e)}

@app.post("/delete_posts")
async def delete_posts(request: DeletePost):

    ''' Delete a post using its ID'''
    try:
        request = json.loads(request.json())

        query = request['query'] 

        res = db.posts.delete_one(query)

        return {"result":res.raw_result}
    except Exception as e:
        return {"Exception":str(e)}

@app.get("/count_posts")
async def stats_count_posts():
    ''' Get the posts count in db'''
    return {"count_posts":db.posts.count_documents({})}


#if __name__ == '__main__':
 #   uvicorn.run(app, port=8002, host="0.0.0.0")