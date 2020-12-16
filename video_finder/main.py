from video_finder import *
from flask import Flask
app = Flask(__name__)
url ="https://www.youtube.com/watch?v=1lwddP0KUEg"


@app.route('/')
def homepage():
    #print(filtered_links)
    text = ""
    for i in filtered_links:
        text+= '\n<iframe src="https://www.youtube.com/embed/{}" width="853" height="480" frameborder="15" allowfullscreen></iframe>'.format(i)
    print(text)
    return '<h1>Selected videos </h1>{}'.format(text)

if __name__ == '__main__':
    links = main()
    filtered_links = [ i.split("=")[-1] for i in links]
    #filtered_links =['1lwddP0KUEg', 'LJUqJ8dLzUQ', 'JJ4AOfVMO28']
    #print(filtered_links)
    app.run()
