from string import digits
import re
share_url="/home/eugene131/waterpy/w_file/"
f_input=open(share_url+"wet_string.txt","r")
f_output=open(share_url+"water.txt","w")
#print(f_input.readline())
string_wet_list=[]
for a in f_input.readlines():
    if a not in string_wet_list:
        string_wet_list.append(a)

print(string_wet_list)

for i in string_wet_list:
    f_output.write(i)