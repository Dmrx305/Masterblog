from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)
@app.route("/")
def index():
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]

        with open("blog_posts.json", "r", encoding="utf-8") as file:
            blog_posts = json.load(file)
        new_id = max((post["id"] for post in blog_posts), default=0) +1

        new_post = {
            "id": new_id,
            "title": title,
            "author": author,
            "content": content,
        }

        blog_posts.append(new_post)
        with open("blog_posts.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file,indent=4)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

        blog_posts = [post for post in blog_posts if post["id"] != post_id]

    with open("blog_posts.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file,indent=4)

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)