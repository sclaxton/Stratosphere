from csv import *
import exceptions
import time
from subprocess import call

# ------------------------------------------------------------------------
#                              Global Data
# ------------------------------------------------------------------------

PROJECTS=0
COUNTS=1

PNAME  =0
PTAG   =1
PCOUNT =2
PERMISSIONS=3

users={}

# ------------------------------------------------------------------------
#                          Function Definitions
# ------------------------------------------------------------------------


def num (s):
    try:
        return int(s)
    except exceptions.ValueError:
        return s

def import_users(userDatabase):
    with open(userDatabase, 'rb') as usercsv:
        csvreader = reader(usercsv, delimiter=',', quotechar='|')
        for row in csvreader:
            users[row[0]] = {}
            for i in range(1,3):
                temp = [a for a in row[i].split(":")]
                users[row[0]][temp[0]] = temp[1:]
            
def get_u_proj_data(user, database):
    if user in users:
        if database in users[user]:
            return users[user][database]
        else:
            return []
    else:
        return []

def get_u_databases(user):
    if user in users:
        return [a for a in users[user]]
    else:
        return []

def write_database():
    userdb = open('users.csv','w')
    for a in users:
        dbs = get_u_databases(a)
        userdb.write(a)
        for b in dbs:
            # print a+","+",".join([":".join(users[a][b]) for b in dbs])
            userdb.write(","+b+":"+":".join(users[a][b]))
        userdb.write("\n")

def increment_count(user, database):
    if user in users:
        if database in users[user]:
            users[user][database][2]=str(num(users[user][database][2])+1)
        else:
            return []
    else:
        return []

def read_last_user(path):
    with open(path, 'rb') as usercsv:
        csvreader = reader(usercsv, delimiter=' ', quotechar='|')
        for row in csvreader:
            print row[2]
    


# ------------------------------------------------------------------------
#                                  Main
# ------------------------------------------------------------------------



user = "jmiller"
userDatabase = "./users.csv"
logpath = "/var/log/apache2/access.log"

while (1):

    import_users(userDatabase)
    increment_count(user, "biomass")
    write_database()    
    
    call(["diff", logpath, "oldaccess.log"])

    read_last_user(logpath)
    time.sleep(1)
    call(["cp", logpath, "oldaccess.log"])
        

