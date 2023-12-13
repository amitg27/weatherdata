import pymysql

def getconnection():
    s = '127.0.0.1' #Your server(host) name 
    d = 'projectdata' 
    u = 'root' #Your login user
    p = 'jobs1471#' #Your login password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn