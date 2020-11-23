import os, csv, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Tables import Base,Edit
import requests as rq
import re
from pathlib import Path

file_path = os.path.abspath(os.getcwd())+"/app/db/app.db"
engine = create_engine('sqlite:///'+file_path)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
counter = 0

def import_from_csv(csv_filepath):
  rows = []
  with open(csv_filepath,"r") as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    tiers = next(data)
    for row in data:
      rows.append(row)
    for row in rows:
      insert_download(row)

def insert_download(row):
  global counter
  counter = counter + 1
  entry = Edit(
    url=row[0],
    creator_tag=row[1],
    black_text=check_text(row[2]),
    anime_name=row[3],
    song_name=row[4],
    song_artist=row[5])
  try:
    session.add(entry)
    session.commit()
  except Exception as e:
    # print(str(counter),e)
    print("error w/ db")
    session.rollback()
  download(fetch_content(row[0]), str(entry.id))

def check_text(cell):
  if(cell == 'y'):
    return True
  return False   

def get_response(url):
  r = rq.get(url)
  while r.status_code != 200:
    r = rq.get(url) # In case of network issue
  return r.text

def get_urls(matches):
  print(match.replace("\\u0026","&") for match in matches)
  return list({match.replace("\\u0026","&") for match in matches})

def fetch_content(url):
    content = []
    response = get_response(url)
    print(response)
    vids = re.findall('"video_url":"([^"]+)"',response) # find all video url links and filter out ""
    imgs = re.findall('"display_url":"([^"]+)"',response) # find all video url links and filter out ""
    content = [get_urls(vids), get_urls(imgs)]
    print(vids, content[0])
    for c in content:
      if c:
        print('Found content: \n{0}'.format('\n'.join(c)))
    return content

# def convert_id_to_5_digits(id):
#   if len(id) < 5:
#     id = "0"+id
#     convert_id_to_5_digits(id)
#   return id

def download(content, id):
  # convert_id_to_5_digits(id)
  img_path = os.path.abspath(os.getcwd())+"/app/static/images/"+id+".jpg"
  vid_path = os.path.abspath(os.getcwd())+"/app/static/videos/"+id+".mp4"
  print("Looking for " +  vid_path + '\n' +  "Looking for " + img_path)
  if not Path(vid_path).is_file():
    print(vid_path + " does not exist!")
    for v in content[0]:
      r = rq.get(v)
      with open(vid_path+"", 'wb') as f:
        f.write(r.content)
  if not Path(img_path).is_file():
    print(img_path + " does not exist!")
    for i in content[1]:
      r = rq.get(i)
      with open(img_path+"", 'wb') as f:
        f.write(r.content)

# import from csv
if len(sys.argv)-1 == 1: # 1 paramter
  csv_path = os.path.abspath(os.getcwd())+"/app/db/"+sys.argv[1]
  import_from_csv(csv_path)
  print("Inserted successfully!")
  print("Downloading...")
# import from user input
else:
  print("No csv provided, going to user input...")
  valid_input = False
  params = []
  while not valid_input:
    for param in params:
      params.pop(0)
    params.append(input("Instagram url: "))
    params.append(input("Creator tag: "))
    params.append(input("Black nav text?: "))
    params.append(input("Anime name: "))
    params.append(input("Song name: "))
    params.append(input("Artist name: "))
    print(params)
    check = input("Is this correct? (Y/N): ")
    if check.lower() == "y":
      valid_input = True
  insert_download(params)
  print("Script complete.")
  