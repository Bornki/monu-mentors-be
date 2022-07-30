from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMU_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(512))

    def __repr__(self):
        return f"<Post {self.title}>"

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")
        model = Post

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = Post(
            title=request.json["title"],
            content = request.json["content"]
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)
        
        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)
    
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204
    
api.add_resource(PostResource, '/posts/<int:post_id>')
api.add_resource(PostListResource, "/posts")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route('/')
def index():
    name = "My posts!"
    return render_template('index.html', title='Welcome', posts=Post.query.all())
    
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)