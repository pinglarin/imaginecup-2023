import os
import sqlite3
from sqlite3 import Error


def insert_into_database(video_name, file_path_name, file_blob): 
  try:
    print("[INFO] : to insert into database")  
    conn = sqlite3.connect('videoDatabase.db')
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    sql_insert_file_query = '''INSERT INTO video(video_name, file_path_name, file_blob) VALUES(?, ?, ?)'''
    cur.execute(sql_insert_file_query, (video_name, file_path_name, file_blob, ))
    conn.commit()
    print("[INFO] : The blob for ", file_path_name, " is in the database.") 
    last_updated_entry = cur.lastrowid
    print("current id after input: ", last_updated_entry) ; print()
    return last_updated_entry
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "Oh shucks, something is wrong here."

def convert_into_binary(file_path):
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary


def read_blob_data(entry_id):
  try:
    conn = sqlite3.connect('videoDatabase.db')
    cur = conn.cursor()
    print("[INFO] : Connected to SQLite to read_blob_data")
    sql_fetch_blob_query = """SELECT * from video where id = ?"""
    cur.execute(sql_fetch_blob_query, (entry_id,))
    record = cur.fetchall()
    for row in record:
      converted_file_name = row[3]
      photo_binarycode  = row[4]
      # parse out the file name from converted_file_name
      # Windows developers should reverse "/" to "\" to match your file path names 
      last_slash_index = converted_file_name.rfind("/") + 1 
      final_file_name = converted_file_name[last_slash_index:] 
      write_to_file(photo_binarycode, final_file_name)
      print("[DATA] : Image successfully stored on disk. Check the project directory. \n")
    cur.close()
  except sqlite3.Error as error:
    print("[INFO] : Failed to read blob data from sqlite table", error)
  finally:
    if conn:
        conn.close()

def write_to_file(binary_data, file_name):
  with open(file_name, 'wb') as file:
    file.write(binary_data)
  print("[DATA] : The following file has been written to the project directory: ", file_name)


def delete_from_database(video_name): 
  try:
    print("[INFO] : to delete from database")  
    conn = sqlite3.connect('videoDatabase.db')
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    sql_delete_file_query = '''DELETE from video where video_name = ?'''
    cur.execute(sql_delete_file_query, (video_name, ))
    conn.commit()
    last_updated_entry = cur.lastrowid
    return last_updated_entry
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "ERROR!!"


def main():
    task = input("What do you want to do?: [insert/delete]:\n") 
    if(task == "insert"):
        file_path_name = input("Enter full file path:\n") 
        video_name = input("Enter name of video to insert:\n") 
        file_blob = convert_into_binary(file_path_name)
        print("[INFO] : the last 100 characters of blob = ", file_blob[:100]) 
        last_updated_entry = insert_into_database(video_name, file_path_name, file_blob)
        read_blob_data(last_updated_entry)
        print("Successfully inserted into database!\n")
    else: #delete row from database
        video_name = input("Enter name of video to delete:\n") 
        delete_from_database(video_name)


if __name__ == "__main__":
  main()


# first video: 
# C:\Users\Aekky\OneDrive - Mahidol University\Desktop\VS Code work\Imagine Cup work\sqlite3_videos\videos\comVidCutMP3.mp3
# second video: C:\Users\Aekky\OneDrive - Mahidol University\Desktop\VS Code work\Imagine Cup work\sqlite3_videos\videos\comVidCutMP4.mp4




