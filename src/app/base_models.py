from typing import Optional
from pydantic import BaseModel

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
