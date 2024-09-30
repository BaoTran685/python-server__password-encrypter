
from connect_to_database import get_db

db = get_db()
mycursor = db.cursor()

query_create_base_table = "CREATE TABLE base (id int PRIMARY KEY AUTO_INCREMENT, base_char varchar(92) NOT NULL)"

query_insert_char = "INSERT INTO base (base_char) VALUES (%s)"

#----------CREATE DATA----------------------------------------------------------------------------------------------

# now we have to create an array of tupples of strings, where each string is 92 characters and should be unique
import random
from encrypt_decrypt import get_dic, get_coordinate, get_string


UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.<>/?|\'\"~"
BASE_CHAR = UPPER_CASE + LOWER_CASE + DIGITS + SPECIAL_CHARACTERS
BASE_CHAR_LEN = len(BASE_CHAR)


def scramble_string(s):
  lis = list(s)
  random.shuffle(lis)
  return ''.join(lis)

number_of_entries = 100001
arr = [('',) for _ in range(number_of_entries)]

for i in range(number_of_entries):
  string = scramble_string(BASE_CHAR)
  arr[i] = (string, )
  # print(arr[i], len(arr[i][0]))  

random.shuffle(arr)
# mycursor.executemany(query_insert_char, arr)
# db.commit()

