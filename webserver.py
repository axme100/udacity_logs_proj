from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

#Handler Class

class WebserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output = "<html><body>"
				output += "&#161 Hola"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>Qué quieres que diga, wey?</h2><input name ="message" type="text" ><input type="submit" value="Submit"> </form>'''
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
				output += "&#161 Hola"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>Qué quieres que diga, wey?</h2><input name ="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</html></body>"
				self.wfile.write(output.encode(encoding = "utf_8"))
				print(output)
				return
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			# Parses HTML form header, like content type into a main value and dictionary value parameter
			# Decipher the message sent from the server (the client)
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			# Is it form data
			if ctype == 'multipart/form-data':
				# Collect all fields in the form
				fields = cgi.parse_multipart(self.rfile, pdict)
				# Store the values (or some into an array)
				messagecontent = fields.get('message')
		output = ""
		output ="<html><body>"
		output += "<h2> Okay, how about this: </h2>"
		output += "<h1> %s </h1>" % messagecontent[0]
		output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>Qué quieres que diga, wey?</h2><input name ="message" type="text" ><input type="submit" value="Submit"> </form>'''
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