#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2
import re
import hashlib
import hmac

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir) , autoescape = True)
SECRET = 'imsosecret'

def hash_str(s):
	return hmac.new(SECRET,str(s)).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s , hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params ):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw ):
        self.write(self.render_str(template , **kw))

class MainPage(Handler):
	def get(self):
		#	self.response.headers['Content-Type'] = 'text/plain'
		visits = 0
		visits_cookie_val = self.request.cookies.get('visits')
		if visits_cookie_val:
			cookie_val = check_secure_val(visits_cookie_val)
			if cookie_val:
				visits =  int(cookie_val)

		visits += 1

		new_cookie_value = make_secure_val(str(visits))

		self.response.headers.add_header('Set-Cookie' , 'visits=%s' % new_cookie_value)

		self.write("You've been here %s times ! " % visits)

		if visits == 100 :
			self.write("This is your 100th login !!!")


   
app = webapp2.WSGIApplication([
    (r'/', MainPage)
], debug=True)