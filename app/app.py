from flask import Flask,request,render_template,redirect
from wtforms import Form,StringField,validators
import loc_writer

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

#GET SITE

#CREATE NEW SITE

#FRONT_PAGE
@app.route("/",methods=['GET','POST'])
def index():

	form = SiteCreationForm(request.form)
	if request.method == 'POST' and form.validate():
		sites_data=loc_writer.readfrom_json()
		if not loc_writer.site_exists(form.url.data,form.shrt.data,sites_data):
			
			sites_data = loc_writer.add_site(form.url.data,	form.shrt.data,sites_data)
			loc_writer.writeto_json(sites_data)

			return "Successfully Created Link"
		else:
			return "Go Link Already Exists"
	
	return render_template('site_creation.html',form=form)


@app.route("/<string:shrt>")
def router(shrt):
	sites = loc_writer.readfrom_json()
	if shrt in sites.keys():
		return redirect(sites[shrt],302)


if __name__=="__main__":
	app.run(host="0.0.0.0")
