from flask import Flask, render_template
import Mangopy
import base64

app = Flask(__name__)

my_database = Mangopy.MongoDb()
for db in my_database.get_dbs():
    print(db)


@app.route("/")
def get_movie():
    return render_template("home.html")


@app.route("/search/<movie_name>", methods=["GET"])
def read(movie_name):
    return my_database.read_image(movie_name)


@app.route("/search/<movie_name>", methods=["Delete"])
def mongo_delete(movie_name):
    my_database.delete_image(movie_name)


@app.route("/home/<movie_name>")
def show_image(movie_name):
    binary_image = base64.b64encode(my_database.read_image(movie_name))
    return render_template("image.html", file_type="jpeg", data=binary_image.decode('utf-8'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)
    # r = requests.get(url=f"http://127.0.0.1:5000/search/{movie_name}")
