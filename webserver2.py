from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

#These commands were tkaen from the CRUD create
#video
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
# Now I can just call a method from session to query the database
session = DBSession()

#Handler Class

class WebserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				allRestauraunts = session.query(Restaurant).all()

				output = ""
				output = "<html><body>"
				output += "Here are the names of all the restaurants:"
				output += "<br>"
				for rest in allRestauraunts:
					# This is where I Will actually assign it to output
					output += "<h1>%s</h1>" % rest.name
					output += "<br>"
				output += "</html></body>"
				self.wfile.write(output.encode(encoding = "utf_8"))
				print(output)
				return
			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "&#161Hola!"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</html></body>"
				self.wfile.write(output.encode(encoding = "utf_8"))
				print(output)
				return
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(303)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			# Parses HTML form header, like content type into a main value and dictionary value parameter
			# Decipher the message sent from the server (the client)
			ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
			# Is it form data
			print("hello123")
			if ctype == 'multipart/form-data':
				pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')[0].decode('utf-8')
			output = ""
			output = "<html><body>"
			output += "<h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent
			output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
			output += "</html></body>"
			self.wfile.write(output.encode(encoding = "utf_8"))
			print(output)
		
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), WebserverHandler)
		print("Web server running on port %s" % port)
		server.serve_forever()
	
	except KeyboardInterrupt:
		print("^C entered, stopping web server...")
		server.socket.close()

if __name__ == '__main__':
	main()