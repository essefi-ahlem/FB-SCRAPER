from facebook_scraper import get_posts
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
from fastapi import FastAPI
from uvicorn import Server, Config 
from base_models import ScrapePostSchema,FindPostSchema,DeletePost
from connection import connect_db


 
app = FastAPI()
load_dotenv(".env")
connection_string = os.environ.get("DB_CONNECTION")
db = connect_db(verbose=True)
#db=connection()

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


if __name__ == '__main__':
    server = Server(Config(app=app, host='0.0.0.0', port=8003))
    server.run()