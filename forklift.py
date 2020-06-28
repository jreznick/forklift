from compadre_core import refresh_request
from datetime import datetime
import sqlite3
from time import sleep


class ForkLift:

	def __init__(self):
		'''Check and store the software version of the process running, every
		process run is owned by a batch id so that is called in __init__ context'''
		from __version__ import __version__ as version
		batch = True
		self.version = version
		self.batch_init()
		self.proc_key=None
		self.etl_key=None
		self.proc_action=None
		self.proc_status=None
		self.outcome_key=None
		
	def __str__(self):
		result = f'ETL Auditor: {self.batch_key}|{self.proc_key}|{self.etl_key}|{self.date}|{self.time}|{self.proc_action}|{self.proc_status}|{self.outcome_key}'

		return result

	@staticmethod
	def wrap_up(sql):
		conn = sqlite3.connect('testy.db')
		c = conn.cursor()
		
		c.execute(sql)
		conn.commit()
		output = c.lastrowid

		print(output)

		return output

	@staticmethod
	def inject_now(self):
		'''Buddy can you spare me the time?'''

		now = datetime.now()
		self.date = now.strftime("%Y-%m-%d")
		self.time = now.strftime("%H:%M:%S")

	def gen_pkey(self, batch):
		'''Create a new primary key using psql serialization, return the key'''
		
		self.inject_now(self)
		sql = f'INSERT INTO id_source(version, batch_key, created_on, created_at) VALUES \
				(\'{self.version}\', \'{self.batch}\', \'{self.date}\', \'{self.time}\')'
		
		result_id = self.wrap_up(sql)

		return result_id

	def batch_init(self):
		'''initialize a new key which is a batch or parent key'''

		self.inject_now(self)
		self.batch=True
		self.batch_key = self.gen_pkey(self.batch)

		sql = f'INSERT INTO batch_audit(row_id, created_on, created_at) VALUES \
				(\'{self.batch_key}\', \'{self.date}\', \'{self.time}\')'
	
		batch_id = self.wrap_up(sql)

		return batch_id

	def proc_init(self, proc_action=1):
		'''initialize a new key which is a process or child key'''

		self.inject_now(self)
		self.batch=False
		self.proc_key = self.gen_pkey(self.batch)
		self.proc_action = proc_action

		sql = f'INSERT INTO proc_audit(row_id, batch_id, proc_action, created_on, created_at) VALUES \
				(\'{self.proc_key}\', \'{self.batch_key}\', \'{self.proc_action}\', \
				 \'{self.date}\', \'{self.time}\')'
	
		proc_id = self.wrap_up(sql)

		return proc_id

	def proc_update(self, payload, insert=False):
		'''Update the status on a given ETL process for a given row'''
		
		self.inject_now(self)
		row_key, status = payload
				
		if insert:
			sql = f'INSERT INTO etl_audit(batch_id, proc_id, row_id, status_id, updated_on, updated_at) \
					VALUES (\'{self.batch_key}\', \'{self.proc_key}\', \'{row_key}\', \'1\', \
					\'{self.date}\', \'{self.time}\')'
		else:
			sql = f'UPDATE etl_audit SET status_id = {status}, \
					updated_on = \'{self.date}\', updated_at = \'{self.time}\' \
					WHERE batch_id = {self.batch_key} AND proc_id = {self.proc_key} \
					AND row_id = {row_key}'

		etl_id = self.wrap_up(sql)
		self.etl_key = etl_id
		self.proc_status = status
		
		return etl_id

	def set_outcome(self, message):

		self.inject_now(self)
		sql = f'INSERT INTO etl_outcome(etl_id, message, created_on, created_at) VALUES \
				(\'{self.etl_key}\', \'{message}\', \'{self.date}\', \'{self.time}\')'
		outcome_id = self.wrap_up(sql)

		self.outcome_key = outcome_id

		return outcome_id



def build_warehouse():
	conn = sqlite3.connect('testy.db')
	c = conn.cursor()

	import __model__ as model
	sql_list = model.sql_list

	for sql in sql_list:
		c.execute(sql)
		conn.commit()
	conn.close()
