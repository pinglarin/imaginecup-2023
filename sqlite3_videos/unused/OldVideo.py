import os
import sqlite3
from sqlite3 import Error

def insert_into_database(file_path_name, file_blob): 
  try:
    conn = sqlite3.connect('video.db')
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    sql_insert_file_query = '''INSERT INTO videos(file_name, file_blob) VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql_insert_file_query, (file_path_name, file_blob, ))
    conn.commit()
    print("[INFO] : The blob for ", file_path_name, " is in the database.") 
    last_updated_entry = cur.lastrowid
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
    conn = sqlite3.connect('video.db')
    cur = conn.cursor()
    print("[INFO] : Connected to SQLite to read_blob_data")
    sql_fetch_blob_query = """SELECT * from videos where id = ?"""
    cur.execute(sql_fetch_blob_query, (entry_id,))
    record = cur.fetchall()
    for row in record:
      converted_file_name = row[1]
      photo_binarycode  = row[2]
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

def main():
  file_path_name = input("Enter full file path:\n") 
  file_blob = convert_into_binary(file_path_name)
  print("[INFO] : the last 100 characters of blob = ", file_blob[:100]) 
  last_updated_entry = insert_into_database(file_path_name, file_blob)
  read_blob_data(last_updated_entry)


if __name__ == "__main__":
  main()


# cd C:\Program Files (x86)\sqlite
# https://www.sqlitetutorial.net/sqlite-commands/
#https://www.twilio.com/blog/intro-multimedia-file-upload-python-sqlite3-database << upload videos onto database



#Sucessful output >>bc for some reason I can't capture screen
# Enter full file path:
# C:\Users\Aekky\OneDrive - Mahidol University\Desktop\VS Code work\Imagine Cup work\comVidCut.mp3
# [INFO] : the last 100 characters of blob =  b'ID3\x04\x00\x00\x00\x00\x01\nTXXX\x00\x00\x00\x12\x00\x00\x03major_brand\x00isom\x00TXXX\x00\x00\x00\x13\x00\x00\x03minor_version\x00512\x00TXXX\x00\x00\x00$\x00\x00\x03compatible_brands\x00isom'
# [INFO] : Successful connection!
# [INFO] : The blob for  C:\Users\Aekky\OneDrive - Mahidol University\Desktop\VS Code work\Imagine Cup work\comVidCut.mp3  is in the database.
# [INFO] : Connected to SQLite to read_blob_data
# [DATA] : The following file has been written to the project directory:  C:\Users\Aekky\OneDrive - Mahidol University\Desktop\VS Code work\Imagine Cup work\comVidCut.mp3
# [DATA] : Image successfully stored on disk. Check the project directory. 


# PATH:  C:\Users\Aekky\OneDrive - Mahidol University\Desktop\VS Code work\Imagine Cup work> 
# video path: C:\Users\Aekky\OneDrive - Mahidol University\Desktop\VS Code work\Imagine Cup work\sqlite3_videos\videos\comVidCutMP3.mp3