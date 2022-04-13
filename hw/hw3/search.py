import mysql.connector
import sys
import pymysql

user_input = sys.argv[1]


#print(user_input)
# eof
#user_input = "Jamie"
user_input = user_input.upper()


#cnx=mysql.connector.connect(user='dsci551',password='Dsci-551',host='localhost',database='sakila')

cnx=pymysql.connect(user='dsci551',password='Dsci-551',host='localhost',database='sakila', db='foo', cursorclass=pymysql.cursors.DictCursor)

cursor=cnx.cursor()

query="SELECT customer.first_name, customer.last_name, city.city FROM customer JOIN address ON customer.address_id = address.address_id JOIN city ON address.city_id = city.city_id WHERE upper(first_name) = %s ORDER BY first_name;"

#query="SELECT first_name FROM customer limit 5"
#cursor.execute(query)

cursor.execute(query, (user_input,))


# eof
# eof
for name in cursor.fetchall():
    print(name)


# eof

# eof
cursor.close()
cnx.close()