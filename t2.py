#Prereq - standart python
import re
from collections import Counter
#Setting path to logfile
logpath = 'D:\\log.log' 
#writing regexps for IP and http status (3 digits, so we take leading whitespace character too)
regex_ip = '([(\d\.)]+)'
regex_status = '([\s][\d][\d][\d])'
#Opening file, if any and loading it into the list row by row 
try:
   with open(logpath) as file:
	   array = [row.strip() for row in file]
   iparr = []
   starr = []
#Doing some regexp magic, filling the empty lists created earlier with IP's and status codes
   for i in array:
	   iparr.append(re.search(regex_ip,i).group())
	   starr.append(re.search(regex_status,i).group())
#Using counter and most_common to determine the top 10 in each list   
   ip = Counter(iparr).most_common(10)
   status = Counter(starr).most_common(10)

except FileNotFoundError:
	print("File not found")
else:
   print(ip)
   print(status)

