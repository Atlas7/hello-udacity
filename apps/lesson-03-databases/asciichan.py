# Udacity - Web Development - Lesson 3 databases - ascii art
# inspired by http://chris.com/ascii/ and Udacity web development course
# Comment: using the jinja2 template.

import os

import jinja2
import webapp2
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

# A GoogleStore data table
class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
	def render_front(self, error="", title="", art=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		self.render("front.html", error=error, title=title, art=art, arts=arts)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")
		error = ""

		if title and art:
			#self.write("Thanks!")
			a = Art(title=title, art=art)  # define a new Art object
			a.put()  # store this new Art object into the GAE database

		else:
			error = "we need both a title and some artwork!"
		
		self.render_front(error, title, art)

app = webapp2.WSGIApplication([
	("/", MainPage)
	])