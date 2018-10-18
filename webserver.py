from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base

#connext to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
		
			if(self.path.endswith("/restaurants")):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				restaurantList = session.query(Restaurant).all()
				list=""
				output=""
				output+="</body></html>"
				output+="<a href='/restaurants/new'>Add new restaurant</a></br></br>"
				for restaurant in restaurantList:
					output += restaurant.name
					output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    # Objective 4 -- Replace Edit href
					output += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
					output += "</br>"
					output += "<a href ='/restaurants/%s/delete'> Delete </a>" % restaurant.id
					output += "</br></br></br>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			if(self.path.endswith("/restaurants/new")):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output=""
				output += "<html><body>"
				output += "<form method = 'POST' enctype='multipart/form-data' >"
				output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
				output += "<input type='submit' value='Create'>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				
				
			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(
					id=restaurantIDPath).one()
				if myRestaurantQuery:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = "<html><body>"
					output += "<h1>"
					output += myRestaurantQuery.name
					output += "</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
					output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)
					
			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]

				myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
				if myRestaurantQuery:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
					output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
					output += "<input type = 'submit' value = 'Yes'>"
					output += "</form>"
					output+= "<a href='/restaurants'><button >No</button></a>"
					output+= "</body></html>"
					
					self.wfile.write(output)
            

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
					newRestaurant = Restaurant(name=messagecontent[0])
					session.add(newRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
					
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					restaurantIDPath = self.path.split("/")[2]

					myRestaurantQuery = session.query(Restaurant).filter_by(
						id=restaurantIDPath).one()
					if myRestaurantQuery != []:
						myRestaurantQuery.name = messagecontent[0]
						session.add(myRestaurantQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()
						
			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
				if myRestaurantQuery:
					session.delete(myRestaurantQuery)
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
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()