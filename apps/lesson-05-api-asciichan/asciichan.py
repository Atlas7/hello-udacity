# Udacity - Web Development - Lesson 5 - API - ascii art with location plot on static google map
# inspired by http://chris.com/ascii/ and Udacity web development course
# Comment: using the jinja2 template.
# localhost:7777/_ah/admin

import os
import jinja2
import webapp2
import urllib2

from xml.dom import minidom
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
	autoescape=True)

# this class may be resued in many other jinja2 backend codes!
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **parms):
		t = jinja_env.get_template(template)
		return t.render(parms)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

# Get location coordinates (lat and long) based on IP
IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
	ip = "4.2.2.2"
	url = IP_URL + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except urllib2.URLError:
		return

	if content:
		d = minidom.parseString(content)
		coords = d.getElementByTagName("gml:coordinates")
		if coords and coords[0].childNodes[0].nodeValue:
			lon, lat = coords[0].childNodes[0].nodeValue.split(',')
			return db.GeoPt(lat, lon)

# A GoogleStore data table
class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	coords = db.GeoPtProperty()


class MainPage(Handler):
	def render_front(self, error="", title="", art=""):
		arts = db.GqlQuery(
			"SELECT * "
			"FROM Art "
			"ORDER BY created DESC "
			"LIMIT 10"
			)
		self.render("front.html", error=error, title=title, art=art, arts=arts)

	def get(self):
		#self.write(repr(get_coords(self.request.remote_addr)))
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")
		error = ""

		if title and art:
			p = Art(title=title, art=art)

			#coords = get_coords(self.request.remote_addr)
			coords = "51.50, -0.12"
			# if we have coordinates, add them to the Art
			if coords:
				p.coords = coords

			p.put()  # store this new Art object into the GAE database

			self.redirect("/")

		else:
			error = "we need both a title and some artwork!"
			self.render_front(error=error, title=title, art=art)

app = webapp2.WSGIApplication([
	("/", MainPage)
	])