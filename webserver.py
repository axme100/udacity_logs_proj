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
			if self.path.endswith("/delete"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1> Delete Name of Restaurant </h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action = '%s'>" % self.path
				output += "<input type='submit' value='Delete'>"
				output += "</form></body></html>"
				self.wfile.write(output.encode(encoding = "utf_8"))

			if self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1> Edit Name of Restaurant </h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action = '%s'>" % self.path
				output += "<input name = 'newRestName' type = 'text' placeholder = 'Edit name here'>"
				output += "<input type='submit' value='Rename'>"
				output += "</form></body></html>"
				self.wfile.write(output.encode(encoding = "utf_8"))
				return
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1> Make New Rest </h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
				output += "<input name = 'newRestName' type = 'text' placeholder = 'New Restaurant Name'>"
				output += "<input type='submit' value='Create'>"
				output += "</form></body></html>"
				self.wfile.write(output.encode(encoding = "utf_8"))
				return
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				allRestauraunts = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				output += '''<a href="/restaurants/new"> Create new Restauruant </a>'''
				output += "<br>"
				output += "Here are the names of all the restaurants:"
				output += "<br>"
				for rest in allRestauraunts:
					# This is where I Will actually assign it to output
					# This idea came from a very specific stack overflow post:
					# https://stackoverflow.com/questions/3915917/make-a-link-use-post-instead-of-get
					output += "<h1>%s</h1>" % rest.name
					# <form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
					output +='''
					<a href="/restaurants/{}/edit"> Edit </a>
					<br>
					<a href="/restaurants/{}/delete"> Delete </a>
					'''.format(rest.id, rest.id)
					output += " "
					# Create delete button
					output += " "
					output += "<br>"
				output += "</body></html>"
				#print(output)
				self.wfile.write(output.encode(encoding = "utf_8"))
				return
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output = "<html><body>"
				output += "Hello:"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</html></body>"
				self.wfile.write(output.encode(encoding = "utf_8"))
				#print(output)
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
				#print(output)
				return
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/delete"):
				print("Your item is going to be deleted my friend: ")
				print("Here is the path, next line rest ID")
				print(self.path)
				print(self.path[-8])
				restaurantID = self.path.split("/")[2]
				toDelete = session.query(Restaurant).filter_by(id = restaurantID).one()
				session.delete(toDelete)
				session.commit()
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
				# This will extract the data 
				if ctype == 'multipart/form-data':
					pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
					fields = cgi.parse_multipart(self.rfile, pdict)
					messageContent = fields.get('newRestName')[0].decode('utf-8')
					print("TEST TEST TEST")
					print(messageContent)
				restaurantID = self.path.split("/")[2]
				targetRest = session.query(Restaurant).filter_by(id = restaurantID).one()
				print('You changed the followin gentry in the database: ')
				print("")
				print(targetRest.name)
				print("Is now called: " + messageContent)
				targetRest.name = messageContent
				session.add(targetRest)
				session.commit()
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

			if self.path.endswith("/restaurants/new"):
				
				ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
				print(ctype)
				# This will extract the data 
				if ctype == 'multipart/form-data':
					pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
					fields = cgi.parse_multipart(self.rfile, pdict)
					messageContent = fields.get('newRestName')[0].decode('utf-8')
				# Let's create  new instance of a class to add to the database
				newRest = Restaurant(name = messageContent)
				# Add the new restaurant to the staging area
				session.add(newRest)
				# Call commit to finalize the new change to the database
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
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