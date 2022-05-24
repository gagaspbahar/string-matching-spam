import time
from string import punctuation
import re
import os

def clean_email(email):
    email = re.sub(r'http\S+', ' ', email)
    email = re.sub("\d+", " ", email)
    email = email.replace('\n', ' ')
    email = email.translate(str.maketrans("", "", punctuation))
    email = email.lower()
    return email

def CalculateTable(substr):
	table = [0 for i in range(257)]
	for i in range(0, 257):
		table[i] = -1
	for i in range(0, len(substr)):
		table[ord(substr[i])] = i
	return table
  
def Boyermoore(string, substr, table):
	# table = CalculateTable(substr)
	len_sub = len(substr)
	len_str = len(string)
	if len_sub > len_str:
		return 0
	elif len_sub == len_str:
		if string == substr:
			return 1
		return 0
	i = 0
	for i in range(-1, len_str - len_sub):
		j = len_sub - 1
		while (j >= 0 and string[i+j] == substr[j]):
			j -= 1
		if j < 0:
			return 1
		slide = j - table[ord(string[i+j])]
		if slide < 1:
			slide = 1
		i += slide
	return 0

def CalculatePrefixSuffix(substr):
	table = [0 for i in range(len(substr) + 1)]
	table[0] = 0
	j = 0
	i = 1
	while (i < len(substr)):
		if substr[i] == substr[j]:
			table[i] = j + 1
			i += 1
			j += 1
		elif j == 0:
			table[i] = 0
			i += 1
		else:
			j = table[j - 1]
	return table

def KMP(str, substr, table):
	# table = CalculatePrefixSuffix(substr)
	len_sub = len(substr)
	len_str = len(str)
	if len_sub > len_str:
		return 0
	elif len_sub == len_str:
		if str == substr:
			return 1
		return 0
	i, j = 0, 0
	while (i < len_str):
		if str[i] == substr[j]:
			i += 1
			j += 1
		elif j == 0:
			i += 1
		else:
			j = table[j-1]
		if len_sub == j:
			return 1
	return 0

# brute force algorithm for string matching
def BruteForce(str, substr):
  len_sub = len(substr)
  len_str = len(str)
  if len_sub > len_str:
    return 0
  elif len_sub == len_str:
    if str == substr:
      return 1
    return 0
  i = 0
  for i in range(0, len_str - len_sub + 1):
    j = 0
    while (j < len_sub and str[i+j] == substr[j]):
      j += 1
    if j == len_sub:
      return 1
  return 0

f = open("./spam.txt", "r")
spamwords = []
for i in f:
  spamwords.append(i.strip())
f.close()



directory = os.fsencode("./test3")

# spamcount = 0
# for file in os.listdir(directory):
#   filename = os.fsdecode(file)
#   if filename.endswith(".txt"):
#     f = open("./test/" + filename, "r")
#     email = f.read()
#     email = clean_email(email)
#     f.close()
#     for word in spamwords:
#       if KMP(email, word) == 1:
#         spamcount += 1
#         break

spamcount = 0

emails = ["" for i in range(101)]
emailcount = 0
for file in os.listdir(directory):
  filename = os.fsdecode(file)
  if filename.endswith(".txt"):
    f = open("./test3/" + filename, "r")
    email = f.read()
    emails[emailcount] = clean_email(email)
    emailcount += 1
    f.close()
  # print("still looping...")

start_time = time.time()

for word in spamwords:
  # KMP
  # table = CalculatePrefixSuffix(word)

  # BM
  # table = CalculateTable(word)

  for email in emails:
    if BruteForce(email, word) == 1:
      spamcount += 1
      break
  

print("Brute Force: " + str(time.time() - start_time) + " s")
print("Spam count: " + str(spamcount))

start_time = time.time()
spamcount = 0

for word in spamwords:
  # KMP
  table = CalculatePrefixSuffix(word)

  for email in emails:
    if KMP(email, word, table) == 1:
      spamcount += 1
      break
  

print("KMP: " + str(time.time() - start_time) + " s")
print("Spam count: " + str(spamcount))

start_time = time.time()
spamcount = 0

for word in spamwords:
  # BM
  table = CalculateTable(word)

  for email in emails:
    if Boyermoore(email, word, table) == 1:
      spamcount += 1
      break
  

print("Boyer-Moore: " + str(time.time() - start_time) + " s")
print("Spam count: " + str(spamcount))
