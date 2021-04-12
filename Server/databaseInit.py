import mysql.connector

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  passwd='password',
  database='security_system'
)

print(mydb)

myCursor = mydb.cursor()

sql = '''
      SELECT count(*)
      FROM information_schema.TABLES
      WHERE TABLE_NAME = 'edge' 
      '''
myCursor.execute(sql)
myResult = myCursor.fetchall()
if myResult > 0:
  print("Skipping Database Initialisation")
  exit()

sql = '''CREATE TABLE IF NOT EXIST \'edge\'(
        edge_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        address VARCHAR(100) NOT NULL,
        name VARCHAR(50) NOT NULL,
        type VARCHAR(30) NOT NULL,
        isActive ENUM('True','False') NOT NULL,
      );
      '''
myCursor.execute(sql)
print(myCursor.rowcount, 'record inserted.')


sql = '''CREATE TABLE IF NOT EXIST \'intrusion\'(
        intrusion_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        edge_id INT NOT NULL,
        dateTime DATETIME NOT NULL,
        FOREIGN KEY (edge_id) REFERENCES edge(edge_id)
      );
      '''
myCursor.execute(sql)
print(myCursor.rowcount, 'record inserted.')

sql = 'INSERT INTO people (fname, lname, timestamp) VALUES (%s, %s, now())'
val = ('Kent', 'Brockman')
myCursor.execute(sql, val)
print(myCursor.rowcount, 'record inserted.')

mydb.commit()



# Retrieve all people records
myCursor = mydb.cursor()
myCursor.execute("SELECT * FROM edge")
myresult = myCursor.fetchall()

for x in myresult:
  print(x)

