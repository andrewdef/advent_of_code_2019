valid_passwords = 0

for i in range(206938, 679128 + 1):
	password = str(i)
	prev_c = int(password[0])
	
	has_same_digits = False
	is_ascending = True
	
	for k in range(1, 6):
		c = int(password[k])
		
		if c < prev_c:
			is_ascending = False
			break
		elif c == prev_c:
			has_same_digits = True
			
		prev_c = c
		
	if has_same_digits and is_ascending:
		valid_passwords += 1
		
print(valid_passwords)