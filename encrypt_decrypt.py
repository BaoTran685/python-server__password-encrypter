import random
from generate import generate_password

#----------CONSTANTS----------------------------------------------------------------------------------------------
UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.<>/?|\'\"~"
BASE_CHAR = UPPER_CASE + LOWER_CASE + DIGITS + SPECIAL_CHARACTERS
BASE_CHAR_LEN = len(BASE_CHAR)

PRIME = 2147483647

PREFIX_LEN = 5
ALTERNATE_LEN = 4 # alternate length is 3, i.e 4 - 1, use for salting

DATA_BASE_LEN = 100001

#----------MYSQL----------------------------------------------------------------------------------------------
from connect_to_database import get_db

def get_base(N: int):
  # we will query the database to get the BASE_CHAR we want
  db = get_db()
  mycursor = db.cursor()
  idx = (N % DATA_BASE_LEN) + 1 # database index start from 1
  query = f"SELECT base_char FROM base WHERE id = {idx}"
  mycursor.execute(query)
  arr = mycursor.fetchall()
  return arr[0][0]

#----------HELPER FUNCTIONS----------------------------------------------------------------------------------------------
def get_dic(base: str):
  k = len(base)
  # dic is a bijective map from each character in base to its index
  dic = {}
  for i in range(k):
    dic[base[i]] = i
  return dic

def get_coordinate(dic: dict, text: str):
  k = len(text)
  # coordinate is a array where each element is dic[text[i]]
  # a coordinate vector
  coordinate = [dic[text[i]] for i in range(k)]
  return coordinate

def get_string(base: str, coordinate: list):
  k = len(coordinate)
  # convert the coordinate vector back into its string representation
  # in other words, this function is the inverse of get_coordinate
  arr = ['' for _ in range(k)]
  for i in range(k):
    arr[i] = base[coordinate[i]]
  return ''.join(arr)

def get_unique_number_representation(coordinate: list):
  k = len(coordinate)
  # total is similar to converting binary number representation to base 10
  # in our case, we convert the 92 (BASE_CHAR_LEN) representation to base 10, which is
  # uniquely determined by coordinate
  total = 0
  for i in range(k):
    total += coordinate[i] * BASE_CHAR_LEN ** i
  return total

def to_base(number: int, base: int):
  if (number == 0):
    return 0
  digits = []
  while (number != 0):
    digits.append(str(number % base))
    number //= base
  return int(''.join(digits))

#----------MAIN FUNCTIONS----------------------------------------------------------------------------------------------
def en_salt(coordinate: list, prefix_len: int):
  k = len(coordinate)
  arr_len = ALTERNATE_LEN * k + prefix_len
  arr = [0 for _ in range(arr_len)]
  # get the random prefix of length prefix_len
  for i in range(prefix_len):
    arr[i] = random.randint(0, BASE_CHAR_LEN - 1)
  
  # get the number N
  number_N_prefix = get_unique_number_representation(arr[:prefix_len]) % PRIME
  random_coordinate = [random.randint(0, BASE_CHAR_LEN - 1) for _ in range((ALTERNATE_LEN - 1) * k)]
  # put the coordinate vector elements to arr
  idx1, idx2 = 0, 0
  if (number_N_prefix % 2 == 0):
    # N even
    idx1, idx2 = prefix_len, prefix_len + 1
  else:
    # N odd
    idx1, idx2 = prefix_len + ALTERNATE_LEN - 1, prefix_len
  for i in range(k):
    arr[idx1] = coordinate[i]
    for j in range(ALTERNATE_LEN - 1):
      arr[idx2 + j] = random_coordinate.pop()
    idx1 += ALTERNATE_LEN
    idx2 += ALTERNATE_LEN
  return arr

def de_salt(coordinate: list, prefix_len: int):
  prefix = coordinate[:prefix_len] # grab the first prefix_len characters
  number_N_prefix = get_unique_number_representation(prefix) % PRIME
  k = len(coordinate)
  arr_len = (k - prefix_len) // ALTERNATE_LEN
  arr = [0 for _ in range(arr_len)]
  # get the wanted characters out
  if (number_N_prefix % 2 == 0):
    # N even
    for i in range(arr_len):
      idx = prefix_len + ALTERNATE_LEN * i
      arr[i] = coordinate[idx]
  else:
    # N ood
    for i in range(arr_len):
      idx = prefix_len + ALTERNATE_LEN * (i + 1) - 1
      arr[i] = coordinate[idx]
  return arr
      
def hash(coordinate: list, N: int):
  k = len(coordinate)
  for i in range(k):
    coordinate[i] = (coordinate[i] + N * i) % BASE_CHAR_LEN
  return coordinate

def encrypt(base: str, hash_lis: list, password: str):
  dic = get_dic(base)
  coordinate_password = get_coordinate(dic, password)
  # we are going to hash it multiple times
  coordinate_hash_password = coordinate_password
  for hash_number in hash_lis:
    coordinate_hash_password = hash(coordinate_hash_password, hash_number)
  coordinate_salt_password = en_salt(coordinate_hash_password, PREFIX_LEN)
  return get_string(base, coordinate_salt_password)

def decrypt(base: str, hash_lis: list, password: str):
  # hash_lis.reverse() # I actually dont have to reverse the order of hash because they are commutative
  dic = get_dic(base)
  dic_reverse = get_dic(base[::-1])
  coordinate_password = get_coordinate(dic, password[:PREFIX_LEN]) + get_coordinate(dic_reverse, password[PREFIX_LEN:])
  coordinate_salt_password = de_salt(coordinate_password, PREFIX_LEN)
  # perform hash, remember that the order of hash is opposite to in encrypt
  coordinate_hash_password = coordinate_salt_password
  for hash_number in hash_lis:
    coordinate_hash_password = hash(coordinate_hash_password, hash_number)
  return get_string(base[::-1], coordinate_hash_password)


def function_password(key: str, password: str, type: str):
  dic_base_char = get_dic(BASE_CHAR) # dic for the 92 base characters
  coordinate_key = get_coordinate(dic_base_char, key) # the key in its coordinate vertor
  number_N_key = get_unique_number_representation(coordinate_key) % PRIME
  # print("N", number_N_key)
  my_base_char = get_base(number_N_key) # the base characters got from key
  hash_lis = [number_N_key] # the hash list for performing hash
  # check for which function to apply
  if (type == "encrypt"):
    return encrypt(my_base_char, hash_lis, password)
  elif (type == "decrypt"):
    # if the len is less than PREFIX_LEN, then the password to decrypt cannot be executed
    if (len(password) < PREFIX_LEN):
      return ""
    return decrypt(my_base_char, hash_lis, password)
  else:
    print("Error in type name")
  
#----------TEST----------------------------------------------------------------------------------------------
def test_accuracy(number_of_test: int):
  for _ in range(number_of_test):
    my_key = ''.join([BASE_CHAR[random.randint(0, BASE_CHAR_LEN - 1)] for _ in range(int(1e2))])
    special_char = random.randint(0, 10)
    upper_case = random.randint(0, 10)
    password = generate_password(special_char, upper_case)
    a = function_password(my_key, password, "encrypt")
    b = function_password(my_key, a, "decrypt")
    if (b != password):
      print('wrong')
      break

def test_security(number_of_test: int):
  cnt = 0
  t = 0
  for _ in range(number_of_test):
    my_key = ''.join([BASE_CHAR[random.randint(0, BASE_CHAR_LEN - 1)] for _ in range(int(3))])
    password = function_password(my_key, "1234abcd@", "encrypt")
    arr = []
    for i in range(BASE_CHAR_LEN):
      for j in range(BASE_CHAR_LEN):
        for h in range(BASE_CHAR_LEN):
          cur = ''.join([BASE_CHAR[i], BASE_CHAR[j], BASE_CHAR[h]])
          arr.append(cur)
    for i in range(len(arr)):
      key = arr[i]
      if (key == my_key): continue
      b = function_password(key, password, "decrypt")
      if (b == "1234abcd@"):
        cnt += 1
        t += i
        print("error", my_key, key, i)
        break
  print(cnt, t // cnt)
  

# test_security(10)
# test_accuracy(10000)

# print(function_password('fdslk', '1234', 'encrypt'))