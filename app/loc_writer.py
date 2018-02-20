import json
import yaml
import os

FILENAME="sites.json"
DEST_CONF_DIR="/etc/nginx/conf.d/"

#TODO
def readfrom_json():

	data = {}
        try:
		with open(FILENAME,'r') as infile:
			data = yaml.safe_load(infile)
	
	except IOError:
		print("Sites file does not exist")

	
	return data


def writeto_json(data):

	with open(FILENAME,'w') as outfile:
		json.dump(data,outfile)


def site_exists(url,shrt,sites):
	if url in sites.keys():
		return True

	if shrt in sites.keys():
		return True

	return False


def add_site(url,shrt,sites):
	sites[url]=shrt
	sites[shrt]=url

	return sites	

def write_new_loc(url,shrt):

	outbuffer="location /{} {{ return 302 {}; }}".format(shrt,url)
	loc_filename= DEST_CONF_DIR + "{}.loc".format(shrt)

	with open(loc_filename,'w') as loc_file:
		loc_file.write(outbuffer)
	
	loc_file.close()


if __name__ == "__main__":
	
	d = readfrom_json()
	
	

	site="http://storage.home"
	goLink="marie"

		
	if not site_exists(site,goLink,d):
		d = add_site(site,goLink,d)
		writeto_json(d)
		write_new_loc(site,goLink)		

	else: 
		print(d)


#DEF WRITE_LOC_FILE


