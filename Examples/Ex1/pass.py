dbms_pass = "123"
get_cred = input()
if (dbms_pass == get_cred.trim()):
    print("Logged In!")
else:
	print ("Incorrect Password.")