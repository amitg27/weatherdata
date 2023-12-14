import pymysql  # Import the pymysql module to enable MySQL database connections in Python.

def getconnection():
    s = '127.0.0.1'  # Server address (host) for the database, here it's set to localhost.
    d = 'projectdata'  # Database name to which you want to connect.
    u = 'root'  # Username for the database login.
    p = 'jobs1471#'  # Password for the database login.
    
    # Establish and return a connection to the database using the provided credentials.
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn
