# Udacity - Web Development - Lesson 3 databases -  Problem set - basic blog
# inspired by http://chris.com/ascii/ and Udacity web development course
# Comment: using the jinja2 template.

import os

import webapp2
import jinja2

from google.appengine.ext import db

# Configure Jinja2 template environment
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

class MainPage(Handler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		visits = self.request.cookies.get("visits", "0")
		#print type(visits)
		if visits.isdigit():
			visits = int(visits) + 1
		else:
			visits = 0
		self.response.headers.add_header("Set-Cookie", "visits=%s" % visits)

		message = "You have been here %s times" % visits + "!"
		if visits > 10:
			message += " You are the best ever!"
		self.write(message)
		# Run this in Google Chrome Developer Console to (cheat) reset visit
		# document.cookie="visits=5"

app = webapp2.WSGIApplication([
	("/", MainPage),
	], debug=True)