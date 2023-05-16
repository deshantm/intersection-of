#import BaseHTTPServer, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import openai

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


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        
        # Get the path requested by the client
        request_path = self.path
        
        #debug code to print request path
        if os.environ.get('ENV') == 'dev':
            print(request_path)

        #strip of the initial slash
        request_path = request_path[1:]

        #strip of the trailing slash
        if request_path.endswith('/'):
            request_path = request_path[:-1]

        #debug code to print request path
        if os.environ.get('ENV') == 'dev':
            print(request_path)

        #build html_style
        html_style = """
        <style>
         body {
            font-family: sans-serif;
            font-size: 16px;
            color: #fff;
            background-color: #222;
            }
            
            h1, h2, h3 {
            font-weight: bold;
            color: #fff;
            text-align: center;
            }
            
            p {
            margin-bottom: 1em;
            }
            
            a {
            color: #fff;
            text-decoration: none;
            }
            
            a:hover {
            text-decoration: underline;
            }
            
            nav {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #222;
            padding: 10px;
            }
            
            nav ul {
            list-style-type: none;
            }
            
            nav li {
            display: inline-block;
            margin: 0 10px;
            }
            
            nav li a {
            color: #fff;
            text-decoration: none;
            padding: 10px 20px;
            border: 1px solid #fff;
            border-radius: 5px;
            }
            
            nav li a:hover {
            background-color: #fff;
            color: #222;
            }

            .box {
            width: 500px;
            height: 300px;
            background-color: #fff;
            border: 1px solid #222;
            padding: 20px;
            margin: 0 auto;
            text-align: center;
            color: #222;
            }
        </style>
        """
            
        #build html_header
        html_header = "<html><head><title>https://attheintersectionof.com</title>" + html_style + "</head><body>"

        #build navigation bar with home about and browse articles
        html_nav = "<nav><ul><li><a href='/'>Home</a></li> | <li><a href='/about'>About</a></li> | <li><a href='/browse'>Browse Articles</a></li></ul></nav>"


        #print beginning of html
        self.wfile.write(bytes(html_header, "utf-8"))
        self.wfile.write(bytes(html_nav, "utf-8"))

        if request_path == "":
            #print the welcome message
            #build html_home with welcom message and mailing list signup
            html_home = "<p>Welcome to https://attheintersectionof.com</p><p>Sign up for our mailing list</p>"
            self.wfile.write(bytes(html_home, "utf-8"))
        elif request_path == "about":
            #print the about message
            #build html_about with about message
            html_about = """
            <h1>We are creating the future</h1>
            <div class="box">
            <p>We are a community of generalists who are working alongside AI to create a future that includes both humans and AI. We are creating the future.</p>
            <p>We create articles, tutorials, and courses with human skills and with the help of state-of-the-art AI.</p>
            <p>We believe that AI has the potential to make the world a better place, and we are committed to using AI for good.</p>
            <p>We are a diverse group of people from all walks of life, and we are united by our shared belief in the power of AI to make the world a better place.</p>
            <p>We are creating the future, and we invite you to join us.</p>
            </div>
            """
            self.wfile.write(bytes(html_about, "utf-8"))
        elif request_path == "browse":
            #print the browse message
            #build html_browse with browse message
            html_browse = "<p>This is the browse page</p>"
            self.wfile.write(bytes(html_browse, "utf-8"))
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
                    #debug print topic_key found
                    if os.environ.get('ENV') == 'dev':
                        print("topic_key found")
                        self.wfile.write(bytes("<p>Topic: %s</p>" % topic_key, "utf-8"))

                    #debug code to print topic_pairs_intersections
                    if os.environ.get('ENV') == 'dev':
                        print("topic_pairs_intersections: " + str(topic_pairs_intersections))

                    
                    intersection = topic_pairs_intersections[topic_key]
                    self.wfile.write(bytes("<p>Intersection: %s</p>" % intersection, "utf-8"))
                else:
                    
                    #debug print topic_key not found
                    if os.environ.get('ENV') == 'dev':
                        print("topic_key not found")
                    # Set up OpenAI API credentials
                    openai.api_key = os.environ["OPENAI_API_KEY"]

                    # Define the prompt for the article
                    prompt = "Write an article about the benefits of meditation."

                    # Generate the article using the GPT-3 API
                    response = openai.Completion.create(
                        engine="davinci",
                        prompt=prompt,
                        max_tokens=1024,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )
                    #write the response to the page
                    self.wfile.write(bytes("<p>Response: %s</p>" % response, "utf-8"))

                    # Print the generated article
                    if os.environ.get('ENV') == 'dev':
                        print(response.choices[0].text)
                        
            # If the request path is invalid, display a message
            else:
                self.wfile.write(b"Invalid request path")
        
        # End the HTML response
        self.wfile.write(bytes("</body></html>", "utf-8"))

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

    

    


if __name__ == "__main__":       

    #add option when starting HTTPServer to do hot reloads
    #https://stackoverflow.com/questions/7023052/configure-httpserver-to-do-hot-reloads

  
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

    
