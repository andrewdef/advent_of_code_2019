valid_passwords = 0

for i in range(206938, 679128 + 1):
	password = str(i)
	prev_c = int(password[0])
	
	has_group_of_2_consecutive_digits = False
	same_digits_in_a_row = 1
	is_ascending = True
	
	for k in range(1, 6):
		c = int(password[k])
		
		if c < prev_c:
			is_ascending = False
			break
			
		if c == prev_c:
			same_digits_in_a_row += 1
			
			if k == 5 and same_digits_in_a_row == 2:
				has_group_of_2_consecutive_digits = True
		else:
			if same_digits_in_a_row == 2:
				has_group_of_2_consecutive_digits = True

			same_digits_in_a_row = 1
			
		prev_c = c
		
	if has_group_of_2_consecutive_digits and is_ascending:
		valid_passwords += 1
		
print(valid_passwords)