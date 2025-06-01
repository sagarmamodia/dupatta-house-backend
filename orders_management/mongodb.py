from django.conf import settings 
from pymongo import MongoClient 
import gridfs

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
fs = gridfs.GridFS(db)

