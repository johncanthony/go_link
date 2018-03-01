from flask import Flask,request,render_template,redirect
from wtforms import Form,StringField,validators
import loc_writer
import json

app = Flask(__name__)

#TODO
#Creation FORM
class SiteCreationForm(Form):

	shrt_link_regex="^[a-z0-9_\-]*$"	
	shrt_validation_err="Invalid input. Accepted Characters: a-z,-,_,0-9"

	shrt = StringField("go/",[validators.Regexp(shrt_link_regex,flags=0,message=shrt_validation_err),
				  validators.DataRequired(message="Field cannot be empty")
	])
	url = StringField("URL: ",[validators.URL(require_tld=False)])

#GET CURRENT SITES LIST
@app.route("/sites", methods=['GET'])
def list_sites():
        return json.dumps(loc_writer.readfrom_json())



def add_it(url,shrt,cur_sites):
    link = {}
    
    link['url']=url
    link['shrt']=shrt
    link['link']="go/"+str(shrt)
    
    cur_sites=loc_writer.add_site(url,shrt,cur_sites)
    loc_writer.writeto_json(cur_sites)
    
    return link


#GET SITE

#CREATE NEW SITE

#FRONT_PAGE
@app.route("/",methods=['GET'])
def index():

        form = SiteCreationForm(request.form)
	return render_template('site_creation.html',form=form)


@app.route("/site/add/",methods=['POST'])
def add_sites():
    
    status={}
    response=0

    if(request.is_json):
        
        json_data = request.get_json()
        url = json_data['url']
        shrt = json_data['shrt']
    
    else:

        form = SiteCreationForm(request.form)
        if form.validate():
            url = form.url.data
            shrt = form.shrt.data
        else:
            status['status']="failed: invalid form data"
            response=400
            return json.dumps(status),response
        #if form.validate():

    sites_data=loc_writer.readfrom_json()

    if not loc_writer.site_exists(url,shrt,sites_data):

        status = add_it(url,shrt,sites_data)
        status['status']="success"
        response=200
    else:
        status['status']="already exists"
	response=422

    return json.dumps(status), response



@app.route("/<string:shrt>")
def router(shrt):
	sites = loc_writer.readfrom_json()
	if shrt in sites.keys():
		return redirect(sites[shrt],302)


if __name__=="__main__":
	app.run(host="0.0.0.0")
