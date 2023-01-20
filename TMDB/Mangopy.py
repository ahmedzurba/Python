import pymongo
import gridfs
import Tmdb


class MongoDb:

    def __init__(self):
        # self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.client = pymongo.MongoClient("mongodb://tmdb-db_host-1:27017/")
        self.mydb = self.client["mydatabase"]
        self.myfs = gridfs.GridFS(self.mydb)
        self.mycol = self.mydb["fs.files"]
        self.tmbd_downloader=Tmdb.TmdbDownloader()

    def get_dbs(self):
        return self.client.list_databases()

    def write_image(self, contents, movie_name, movie_id, file_type):
        image_document = self.mycol.find_one({"moviename": movie_name})
        if image_document is None:
            self.myfs.put(contents, moviename=movie_name, movieid=movie_id, filetype=file_type)

    def update_image(self, movie_name, key_to_update, val_to_update):
        self.mycol.update_many({"moviename": movie_name}, {"$set": {key_to_update: val_to_update}})

    def delete_image(self, movie_name):
        image_document = self.mycol.find_one({"moviename": movie_name})
        if image_document is not None:
            image_id = image_document["_id"]
            self.myfs.delete(image_id)

    def read_image(self, movie_name):
        image_document= self.mycol.find_one({"moviename": movie_name})
        if image_document is not None:
            image_id = image_document["_id"]
            image_file = self.myfs.get(image_id).read()
        else:
            image_file, filename, movie_id, filetype = self.tmbd_downloader.get_image(movie_name)
            self.write_image(image_file, filename, movie_id, filetype)
        return image_file

    def meta_data(self, movie_name):
        return self.mycol.find_one({"moviename": movie_name})



