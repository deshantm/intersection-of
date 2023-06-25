#import BaseHTTPServer, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import openai
import json

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

    def MyServer(self):
        #start with empty topics dictionary
        self.topics_dict = {}
    

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


        if "well-know" not in request_path:

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
        elif request_path == "about-anything":
            #print the about message
            #build html_about with about message
            html_about = """
            <h1>We are creating the future</h1>
            <div class="box">
            <p>Hi.</p>
            </div>
            """
            self.wfile.write(bytes(html_about, "utf-8"))
        elif request_path == "browse":
            #print the browse message
            #build html_browse with browse message
            html_browse = "<p>This is the browse page</p>"
            #go through list of topics and print the topic and content for it
            topics_dict = self.read_topics()
            for topic in topics_dict:
                html_browse = html_browse + "<p><a href='/" + topic + "'>" + topic + "</a></p>"

            intersections_dict = self.get_topic_pairs_intersections()

            #go through list of intersections and print the intersection and content for it
            for intersection in intersections_dict:
                topics = intersection.split('_')
                num_topics = len(topics)
                index = 0
                for topic in topics:
                    if index == 0:
                        html_browse = html_browse + "<p><a href='/" + topic + "'>" + topic + "</a>"
                    elif index == num_topics - 1:
                        html_browse = html_browse + " and <a href='/" + topic + "'>" + topic + "</a></p>"
                    else:
                        html_browse = html_browse + ", <a href='/" + topic + "'>" + topic + "</a>"
                    index = index + 1
                    
            self.wfile.write(bytes(html_browse, "utf-8"))
        else:
            # Split the path into topics by slashes
            topics = request_path.split('/')
            #with open("/home/public/" + topics[0] + "/" + topics[1] + "/" + topics[2], 'r') as myfile:
            #            data=myfile.read()
            #            self.wfile.write(bytes(data, "utf-8"))
            #            return

            #debug code to print topics
            if os.environ.get('ENV') == 'dev':
                #print topic: topic
                print("topics: " + str(topics))

            #debug print lenth of topics
            if os.environ.get('ENV') == 'dev':
                print("length of topics: " + str(len(topics)))

            # If there is only one topic, display that topic's content
            if len(topics) == 1:

                if topics[0] == "favicon.ico":
                    return
                

                #read existing topics
                single_topics = self.read_topics()

                topic_name = topics[0]
                #debug code to print single topic
                if os.environ.get('ENV') == 'dev':
                    print("single topic: " + topic_name)

                if topic_name in single_topics:

                    #strip quotes from the beginning of the article
                    article_content = single_topics[topic_name].lstrip('"')

                    self.wfile.write(bytes("<p>Topic: %s</p>" % topic_name, "utf-8"))
                    self.wfile.write(bytes("<p>Content: %s</p>" % article_content, "utf-8"))
                else: #topic not found in single_topics
                    #build prompt to write a sentence
                    prompt = "write a sentence that ends with a period and doesn't start wtih a quote and is written with flair about " + topic_name + ":"
                    #openai completion


                    #debug code to print prompt
                    if os.environ.get('ENV') == 'dev':
                        print("prompt: " + str(prompt))

                    openai.api_key = os.environ.get('OPENAI_API_KEY')

                        
                    messages = [{"role": "user", "content": prompt}]

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        stop=["."],
                        temperature=1.0,
                    )
                    article_content = response['choices'][0]['message']['content']
                    
                    #strip quotes from the beginning of the article
                    article_content = article_content.lstrip('"')

                    # Write the response to the page
                    self.wfile.write(bytes("<p>%s.</p>" % article_content, "utf-8"))

                    # Print the generated article
                    if os.environ.get('ENV') == 'dev':
                            print (article_content)

                    #cache the generated article in the topics dictionary
                    single_topics[topic_name] = article_content + "\n"
                    self.write_topics(single_topics)
                

                
            
           # If there are multiple topics, display the intersection of those topics
            elif len(topics) >= 2:

                #if first topic is ".well-known" then return
                if topics[0] == ".well-known" and topics[1] == "acme-challenge":
                    #read topics[2] and write as response
                    with open("/home/public/" + topics[0] + "/" + topics[1] + "/" + topics[2], 'r') as myfile:
                        data=myfile.read()
                        self.wfile.write(bytes(data, "utf-8"))
                        return

                topic_pairs_intersections = self.get_topic_pairs_intersections()
                topic_key = "_".join(sorted(topics))

                #debug code to print topic_key
                if os.environ.get('ENV') == 'dev':
                    print("topic_key: " + str(topic_key))

                if topic_key in topic_pairs_intersections.keys():
                    #debug code to print topic_key
                    if os.environ.get('ENV') == 'dev':
                        print("topic_key: " + str(topic_key))

                    #debug code to print topic_pairs_intersections[topic_key]
                    if os.environ.get('ENV') == 'dev':
                        print("topic_pairs_intersections[topic_key]: " + str(topic_pairs_intersections[topic_key]))

                    #build prompt to write a sentence
                    prompt = "write a sentence that ends with a period and doesn't start wtih a quote and is written with flair about " + topic_key + ":"


                    #debug code to print prompt
                    if os.environ.get('ENV') == 'dev':
                        print("prompt: " + str(prompt))


                    openai.api_key = os.environ.get('OPENAI_API_KEY')

                    
                    messages = [{"role": "user", "content": prompt}]

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        stop=["."],
                        temperature=1.0,
                    )
                    article_content = response['choices'][0]['message']['content']
                   
                    # Write the response to the page
                    self.wfile.write(bytes("<p>%s.</p>" % article_content, "utf-8"))

                    # Print the generated article
                    if os.environ.get('ENV') == 'dev':
                         print (article_content)

                    #cache the generated article in the insersections topics dictionary
                    topic_pairs_intersections[topic_key] = article_content + "\n"
                    self.write_topic_pairs_intersections(topic_pairs_intersections)





                

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
                    
                    #split the topic_key into topics
                    topics = topic_key.split('_')
                    prompt = "write a sentence that ends with a period and doesn't start wtih a quote and is written with flair about " + topics[0]
                    rest_of_topics = topics[1:]
                    index = 1
                    for topic in rest_of_topics:
                        if index != rest_of_topics[len(rest_of_topics) -1]:
                            prompt += " and "
                        index += 1
                        prompt += topic
                       
                    
                    #debug code to print prompt
                    if os.environ.get('ENV') == 'dev':
                        print("prompt: " + str(prompt))


                    openai.api_key = os.environ.get('OPENAI_API_KEY')

                    
                    messages = [{"role": "user", "content": prompt}]

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        stop=["."],
                        temperature=1.0,
                    )
                    article_content = response['choices'][0]['message']['content']
                   
                    # Write the response to the page
                    self.wfile.write(bytes("<p>%s.</p>" % article_content, "utf-8"))

                    # Print the generated article
                    if os.environ.get('ENV') == 'dev':
                         print (article_content)

                    #cache the generated article in the topic_pairs_intersections
                    topic_pairs_intersections[topic_key] = article_content + "\n"
                    self.write_topic_pairs_intersections(topic_pairs_intersections)
                        
            # If the request path is invalid, display a message
            else:
                self.wfile.write(b"Invalid request path")
        
        # End the HTML response
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def write_topic(self, topics_dict):
        #write topic to file
        with open:
            #write topics_dict to file
            with open('topics_dict.json', 'w') as outfile:
                #write topics_dict to file
                json.dump(topics_dict, outfile)


    def get_topic_pairs_intersections(self):
        #load topic_pairs_intersections from file cache topic_pairs_intersections.json or create if it doesn't exist
        
        #check if file exists
        if os.path.isfile('topic_pairs_intersections.json'):

            with open('topic_pairs_intersections.json') as json_file:
                topic_pairs_intersections = json.load(json_file)
                print("topic_pairs_intersections: " + str(topic_pairs_intersections))
                return topic_pairs_intersections
        else:
            topic_pairs_intersections = {}
            #create empty file
            with open('topic_pairs_intersections.json', 'w') as outfile:
                #write empty json to file
                json.dump(topic_pairs_intersections, outfile)

            return topic_pairs_intersections

    def write_topic_pairs_intersections(self, topic_pairs_intersections):
        #write topic_pairs_intersections to file cache topic_pairs_intersections.json
        with open('topic_pairs_intersections.json', 'w') as outfile:
            json.dump(topic_pairs_intersections, outfile)
    
    def read_topics(self):
        #load topics from file cache topics.json or create if it doesn't exist
        topics = {}
        #check if file exists
        if os.path.isfile('topics.json'):

            with open('topics.json') as json_file:
                topics = json.load(json_file)
                print("topics: " + str(topics))
                return topics
        else:
            topics = {}
            #create empty file
            with open('topics.json', 'w') as outfile:
                #write empty json to file
                json.dump(topics, outfile)

            return topics
        
    def write_topics(self, topics):
        #write topics to file cache topics.json
        with open('topics.json', 'w') as outfile:
            json.dump(topics, outfile)
    


if __name__ == "__main__":       

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

    
