from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/heyo"):
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "Hello world!"
				output += '''<form method='POST' enctype='multipart/form-data' action='/heyo'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(bytes(output, "utf8"))
				print(output)
				return
			if self.path.endswith("/shikamoo"):
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "shikamoo!"
				output += '''<form method='POST' enctype='multipart/form-data' action='/heyo'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"

				self.wfile.write(bytes(output, "utf8"))
				print(output)
				return
		except IOError:
			self.send_error(404, "Uh oh!, the file wasn't found! %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header("Content-type", "text/html")
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
			pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
			print(ctype)
			if ctype == "multipart/form-data":
				fields = cgi.parse_multipart(self.rfile, pdict)
				print(fields)
				messagecontent = fields.get("message")

				output = ""
				output += "<html><body>"
				output += "<h2> Okay, here you go: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0].decode("utf-8")
				output += '''<form method='POST' enctype='multipart/form-data' action='/heyo'>'''
				output += '''<h2>What would you like me to say?</h2><input name="message" type="text" >'''
				output += '''<input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(bytes(output, "utf8"))
				print(output)
				return

		except Exception as e:
			print(e)
			print("Error")



def main():
	try:
		port = 8080
		server = HTTPServer(("", port), webServerHandler)
		print("Web server running on port %s" % port)
		server.serve_forever()

	except KeyboardInterrupt:
		print("^C entered, killing web server")
		server.socket.close()


if __name__ == "__main__":
	main()