def remove_empty_trains():
    root = "static/uploads/train"
    folders = list(os.walk(root))[1:]
    for folder in folders:
        if not folder[2]:
            os.rmdir(folder[0])

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def folder_name_generator(name):
    name = name.split(" ")
    name = name[0].capitalize()+" "+name[1].capitalize()
    return name

def file_name_generator(name,count):
    dir_path = f"static/uploads/train/{name}"
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return str(count)+".jpg"

def directory_genartor(name):
    path = f"static/uploads/train/{name}"
    try: 
        os.mkdir(path) 
    except OSError as error: 
        pass