from collections import defaultdict
import os
from flask import Flask, render_template, request
from sqlalchemy.sql.expression import func
from flask_sqlalchemy import SQLAlchemy

file_path = os.path.abspath(os.getcwd())+"/app/db/app.db"
# print("sqlite:////"+file_path)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+file_path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:////'+file_path
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Edit(db.Model):
    __table__=db.Model.metadata.tables["edit"]

    def __repr__(self):
        return Edit()


prev_ids = []
prev_ids.append("")
@app.route("/", methods=['GET', 'POST'])
def index():
  get_id = request.args.get('edit')
  if get_id:
    edit = Edit.query.filter_by(id=get_id).first()
    prev_ids.append(edit.id)
  elif request.method == 'POST' and request.form.get('prev'):
    get_id = request.form.get('prev')
    edit = Edit.query.filter_by(id=get_id).first()
    prev_ids.pop()
  else:
    edit = Edit.query.order_by(func.random()).first()
    while edit.id == prev_ids[-1]:
      print("prev id same as new id, finding new vid")
      edit = Edit.query.order_by(func.random()).first()
    prev_ids.append(edit.id)
  # print(get_id)
  print(prev_ids)
  img_path = "/static/images/"+str(edit.id)+".jpg"
  vid_path = "/static/videos/"+str(edit.id)+".mp4"
  artist_song =  edit.song_artist
  if edit.song_name !=  '':
      artist_song = artist_song + " — " + edit.song_name
  if edit.black_text:
    font_color = "#1f1f1f"
  else:
    font_color = "white"
  return render_template('index.html',
    prev_edit_id=prev_ids[-2],
    curr_edit=edit,
    video=vid_path,
    image=img_path,
    artist_song=artist_song,
    color=font_color).format(edit.id)

if __name__ == "__main__":
    app.run()