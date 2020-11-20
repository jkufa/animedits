from collections import defaultdict
import os
from flask import Flask, render_template
from sqlalchemy.sql.expression import func
from flask_sqlalchemy import SQLAlchemy

file_path = os.path.abspath(os.getcwd())+"/app/db/app.db"
print("sqlite:////"+file_path)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+file_path
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Edit(db.Model):
    __table__=db.Model.metadata.tables["edit"]

    def __repr__(self):
        return Edit()

@app.route("/")
def index():
    row =  Edit.query.order_by(func.random()).first()
    img_path = "/static/images/"+str(row.id)+".jpg"
    vid_path = "/static/videos/"+str(row.id)+".mp4"
    artist_song =  row.song_artist
    if row.song_name !=  '':
        artist_song = artist_song + " — " + row.song_name
    if row.black_text:
      font_color = "#1f1f1f"
    else:
      font_color = "white"
    print(font_color)
    return render_template('index.html',query=row,video=vid_path,image=img_path,artist_song=artist_song,color=font_color)

if __name__ == "__main__":
    app.run()