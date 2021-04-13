import psycopg2

  

mydb = psycopg2.connect(
  host='localhost',
  user='postgres',
  password='password',
  database='securitysystem'
)
mycursor = mydb.cursor()

sql = """
      SELECT to_regclass('schema_name.table_name');
      """
mycursor.execute(sql)

if mycursor.fetchone() != None :
  print("tables already exist, exiting database initialisation")
  exit();
mycursor.execute("CREATE TYPE type AS ENUM('RaspberryPi','Microbit')")

sql = '''CREATE TABLE  edge(
        edge_name VARCHAR(50) NOT NULL PRIMARY KEY,
        ip_address VARCHAR(30) NOT NULL,
        type type NOT NULL,
        is_active BOOLEAN NOT NULL
      );
      '''
mycursor.execute(sql)
print(mycursor.rowcount, 'record inserted.')

sql = '''CREATE TABLE  intrusion(
        edge_name VARCHAR(50) NOT NULL,
        date_time timestamp NOT NULL,
        PRIMARY KEY(edge_name, date_time),
        FOREIGN KEY (edge_name) REFERENCES edge(edge_name)
      );
      '''
mycursor.execute(sql)

sql = 'INSERT INTO edge(edge_name,ip_address,type,is_active) VALUES (%s, %s, %s, %s)'
val = ("EdgeProcessor1","1.1.1.1","RaspberryPi","True")
mycursor.execute(sql, val)
print(mycursor.rowcount, 'record inserted.')

mydb.commit()


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM edge")
results = mycursor.fetchall()
for result in results:
  print(result)
## Retrieve all people records
#mycursor = mydb.cursor()
#mycursor.execute("SELECT * FROM people")
#myresult = mycursor.fetchall()
#
#for x in myresult:
#  print(x)
#
