# Udacity - Web Development - Lesson 2a Templates - Introducing templates
# Comment: using the jinja2 template.

import os

import jinja2
import webapp2

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
		self.render("main_page.html")


class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get("n", 0)
		if n:
			n = int(n)

		self.render("fizzbuzz.html", n=n)

class ShoppingListHandler(Handler):
	def get(self):
		#self.write("Shopping List App")
		items = self.request.get_all("food")
		self.render("shopping_list.html", items=items)

app = webapp2.WSGIApplication([
	("/", MainPage),
	("/fizzbuzz", FizzBuzzHandler),
	("/shopping-list", ShoppingListHandler)
	])