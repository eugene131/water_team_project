from string import digits
import re

f_input=open("/home/eugene131/waterpy/w_file/wet_string.txt","r")
f_output=open("/home/eugene131/waterpy/w_file/water.txt","w")
#print(f_input.readline())
string_wet_list=[]
for a in f_input.readlines():
    if a not in string_wet_list:
        string_wet_list.append(a)

print(string_wet_list)

for i in string_wet_list:
    f_output.write(i)