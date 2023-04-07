#import BaseHTTPServer, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

#for local development use localhost,
#but for production use 0.0.0.0

#if dev
#if system ENV variable is set to dev, use localhost
if os.environ.get('ENV') == 'dev':
    hostName = "localhost"
else:
    hostName = "0.0.0.0"

#if ENV is dev, use port 8080
#else use port 80
if os.environ.get('ENV') == 'dev':
    serverPort = 8080
else:   
    serverPort = 80

class MyServer(BaseHTTPRequestHandler):

    def read_topics(self):
        # hardcode topics for now
        # create topics as map of topic name and string content
        topics = {}
        topics["ai"] = "This is all about ai"
        topics["robots"] = "This is all about robots"
        print("read_topics called")
        print("topics_dict: " + str(topics))
        return topics


    def get_topic_pairs_intersections(self):
        #hardcode topic pairs for now
        #create topic pairs as map of topic pair and intersection
        topic_pairs_intersections = {}
        topic_pairs_intersections["ai_robots"] = "This is the intersection of ai and robots"
        topic_pairs_intersections["ai_dogs_robots"] = "This is the intersection of ai and dogs and robots"
        # add more topic intersections here...

        return topic_pairs_intersections

    

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://attheintersectionof.com</title></head>", "utf-8"))
        
        # Get the path requested by the client
        request_path = self.path
        
        #debug code to print request path
        if os.environ.get('ENV') == 'dev':
            print(request_path)

        #strip of the initial slash
        request_path = request_path[1:]

        #debug code to print request path
        if os.environ.get('ENV') == 'dev':
            print(request_path)

        #print beginning of html
        self.wfile.write(bytes("<html><body>", "utf-8"))

        if request_path == "":
            #print the welcome message
            self.wfile.write(bytes("<p>Welcome to https://attheintersectionof.com</p>", "utf-8"))
        
        else:
            # Split the path into topics by slashes
            topics = request_path.split('/')

            #debug code to print topics
            if os.environ.get('ENV') == 'dev':
                #print topic: topic
                print("topics: " + str(topics))

            #debug print lenth of topics
            if os.environ.get('ENV') == 'dev':
                print("length of topics: " + str(len(topics)))

            # If there is only one topic, display that topic's content
            if len(topics) == 1:
                print("here")
                topic_name = topics[0]
                topics_dict = self.read_topics()

                #debug code to print topics_dict
                if os.environ.get('ENV') == 'dev':
                    print("topics_dict: " + str(topics_dict))

                if topic_name in topics_dict.keys():
                    self.wfile.write(bytes("<p>Topic: %s</p>" % topic_name, "utf-8"))
                    self.wfile.write(bytes("<p>Content: %s</p>" % topics_dict[topic_name], "utf-8"))
            
           # If there are multiple topics, display the intersection of those topics
            elif len(topics) >= 2:
                topic_pairs_intersections = self.get_topic_pairs_intersections()
                topic_key = "_".join(sorted(topics))

                #debug code to print topic_key
                if os.environ.get('ENV') == 'dev':
                    print("topic_key: " + str(topic_key))

                

                if topic_key in topic_pairs_intersections.keys():

                    #debug code to print topic_pairs_intersections
                    if os.environ.get('ENV') == 'dev':
                        print("topic_pairs_intersections: " + str(topic_pairs_intersections))

                    
                    intersection = topic_pairs_intersections[topic_key]
                    self.wfile.write(bytes("<p>Intersection: %s</p>" % intersection, "utf-8"))
            
            # If the request path is invalid, display a message
            else:
                self.wfile.write(b"Invalid request path")
        
        # End the HTML response
        self.wfile.write(bytes("</body></html>", "utf-8"))



if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")