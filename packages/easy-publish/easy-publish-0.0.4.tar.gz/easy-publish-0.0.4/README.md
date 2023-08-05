### Easy Publish
---
Easy publish is a Python library that provides a simple abstraction for publishing text files as blog posts. 


### Installation
---
Requires: Python >= 3.6
`pip install easy-publish`


### Usage
---
To use easy publish call the `generate_posts` function pointing it to the directory your files are located in. Below is an example flask app with jinja templating that utilizes easy publish, however any web framework/templating engine should work with easy publish.
```
from flask import Flask
from easy_publish import generate_posts

app = Flask(__name__)
posts = generate_posts(~/my/blogposts)

@app.route("/blog")
def blog():
  return render_template("blog.html", metadata=posts.metadata)

@app.route("/blog/<p>")
def blogpost(p):
  return render_template("post.html", post=posts.posts[p])
```

Then you can use the `metadata` and `post` objects in your projects. Metadata is useful for listing all of you blog posts while Post is useful for templating the content. `blog.html` and `post.html` might look like the following:

##### blog.html
```
{{% for post in metadata %}}
  <li>{{ post.title }}</li>
  <li>{{ post.date }}</li>
  <li>{{ post.tags }}</li>
  <li>{{ post.author }}</li>
{{% endfor %}}
```

##### post.html
```
<h1>{{ post.title }}</h1>
<h4>{{ post.date }}</h1>
<h4>{{ post.author }}</h1>
<p>{{ post.content }}</p>
```

### Contributing
---
Currently in heavy development and not a stable interface. Feel free to contribute ideas as issues or as a pull request.

### License
---
MIT
