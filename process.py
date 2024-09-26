
import random

UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.<>/?|\'\"~"
BASE_CHAR = UPPER_CASE + LOWER_CASE + DIGITS + SPECIAL_CHARACTERS

LOW = 8
HIGH = 15

# scramble_string(s) returns the scrambled string of s
def scramble_string(s):
  lis = list(s)
  random.shuffle(lis)
  return ''.join(lis)

def generate_password(data):
  string = ""
  # get the special character
  cur = random.choices(SPECIAL_CHARACTERS, k=data["specialChar"])
  cur = ''.join(cur)
  string += cur
  
  # get the uppercase letter
  cur = random.choices(UPPER_CASE, k=data["upperCase"])
  cur = ''.join(cur)
  string += cur
  
  # create k len string of random characters other than from the two above
  k = random.randint(LOW, HIGH)
  arr = LOWER_CASE + DIGITS
  cur = random.choices(arr, k=k)
  cur = ''.join(cur)
  string += cur
  
  return scramble_string(string)

# print(generate_password({"specialChar": 5, "upperCase": 3}))
