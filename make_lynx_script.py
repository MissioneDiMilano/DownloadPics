import sys

def accept_cookies(our_file, count):
	for i in range(count):
		our_file.write("key y\n")
	return our_file

def write_string(our_file, our_string):
	for i in range(len(our_string)):
		our_file.write("key "+our_string[i]+"\n")
	return our_file

def init_file(path):
	return open(path, "w")

def write_meta(our_file):
	our_file.write("# Command logfile created by Lynx 2.8.7rel.1 (05 Jul 2009)\n# Arg0 = lynx\n# Arg1 = -cmd_log=download.txt\n# Arg2 = https://imos.ldschurch.org/imos/index.jsf\n")
	our_file.flush()
	return our_file

def write_open_connection(our_file, user, password):
	# Get past the invalid cookie prompts
	our_file = accept_cookies(our_file, 2)	

	# Log in

	# Selects the user name box
	our_file.write("key <space>\n") # Selects the user name box

	# Enters the user name in the box
	our_file = write_string(our_file, user)

	# Selects the password box
	for i in range(2):
		our_file.write("key <tab>\n")

	# Enters the password in the box
	our_file = write_string(our_file, password)

	# Selects the submit button
	for i in range(2):
		our_file.write("key <tab>\n")

	# Submits the form
	our_file.write("key ^J\n")

	# Get past the invalid cookie prompts again. :\
	our_file = accept_cookies(our_file, 2)

	our_file.flush()

	return our_file

def get_picture(our_file, location, mID):
	base_url = "https://imos.ldschurch.org/imos/imageResource?imageType=MISSIONARY_PROFILE&imageId="
	complete_url = base_url + mID
	
	# TODO what kind of path are they giving me? Windows or Linux?
	# For now it's the complete Linux path.

	save_string = location
	if save_string[len(location)-1] == "/":
		save_string = save_string + mID + ".jpg"
	else:
		save_string = save_string + "/"+mID+".jpg"

	# Start listening for the url
	our_file.write("key g\n")

	# Write the url we need.
	our_file = write_string(our_file, complete_url)

	# Send it
	our_file.write("key ^J\n")

	# Download the picture
	our_file.write("key d\n")

	# Select the save option and choose it
	our_file.write("key Down Arrow\n")
	our_file.write("key ^J\n")

	# Delete the complete_url (plus some safety) which will automatically be save location
	for i in range(len(complete_url)+5):
		our_file.write("key <delete>\n")

	# Enter the correct file and location
	our_file = write_string(our_file, save_string)

	# Submit that to save the file
	our_file.write("key ^J\n")
	return our_file

def close_lynx(our_file):
	our_file.write("key q\n")
	our_file.write("key y")
	return our_file

def main(location, script_name, mIDs, user, password):
	f = init_file(script_name)
	
	f = write_meta(f)
	
	f = write_open_connection(f, user, password)
	
	
	for id in mIDs:
		f = get_picture(f, location, id)

	f = close_lynx(f)
	
	f.close()
	
if __name__ == "__main__":
	argv = sys.argv
	print argv
	argv[3] = raw_input("Re-enter mIDs here: ")
	main(argv[1], argv[2], argv[3].split(":"), argv[4], argv[5])