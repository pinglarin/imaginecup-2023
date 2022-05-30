import sqlite3

def main():
    conn = sqlite3.connect('videoDatabase.db')
    with open('schema.sql') as f:
        conn.executescript(f.read())
        print("[INFO] : Read schema!")

if __name__ == "__main__":
  main()