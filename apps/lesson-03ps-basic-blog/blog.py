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

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

# this class may be resued in many other jinja2 backend codes!
class BlogHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **parms):
		t = jinja_env.get_template(template)
		return t.render(parms)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(BlogHandler):
	def get(self):
		self.write("Hello, Udacity!")

####### Blog stuff

# Define blog_key of the blog parent
def blog_key(name="default"):
	return db.Key.from_path("blogs", name)

class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)

	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return render_str("post.html", p = self)

class BlogFront(BlogHandler):
	def get(self):
		#posts = Post.all().order("-created")

		posts = db.GqlQuery("select * from Post order by created desc limit 10")
		self.render("front.html", posts=posts)

class PostPage(BlogHandler):
	def get(self, post_id):
		key = db.Key.from_path("Post", int(post_id), parent=blog_key())
		post = db.get(key)

		if not post:
			self.error(404)
			return

		self.render("permalink.html", post=post)

class NewPost(BlogHandler):
	def get(self):
		self.render("newpost.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			p = Post(parent=blog_key(), subject=subject, content=content)
			p.put()
			self.redirect("/blog/%s" % str(p.key().id()))
		else:
			error = "subject and content, please!"
			self.render("newpost.html", subject=subject, content=content, error=error)


app = webapp2.WSGIApplication([
	("/", MainPage),
	("/blog/?", BlogFront),
	("/blog/([0-9]+)", PostPage),
	("/blog/newpost", NewPost)
	], debug=True)