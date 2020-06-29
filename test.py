import sqlite3
conn = sqlite3.connect('testy.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS id_source'
	)
c.execute('''
	CREATE TABLE id_source(
	id 			INTEGER PRIMARY KEY AUTOINCREMENT,
	version 	TEXT,
	batch_key 	BOOLEAN,
	created_on 	TEXT,
	created_at 	TEXT
)
	'''
	)

c.execute('''INSERT INTO id_source(version, batch_key, created_on, created_at) VALUES
			('1.0.0',1,'2020-06-28','19:00:01'),
			('1.0.0',1,'2020-06-28','19:00:02')
			'''
)
conn.commit()

for row in c.execute('SELECT * FROM id_source'):
	print(row)

conn.close()

def build_warehouse():
	conn = sqlite3.connect('testy.db')
	c = conn.cursor()

	import __model__ as model
	sql_list = model.sql_list

	for sql in sql_list:
		c.execute(sql)
	conn.commit()
	conn.close()
