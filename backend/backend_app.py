from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = request.get_json()

        if not validate_post_data(new_post):
            return jsonify({"error": "title or content are missing"}), 400
        else:
            # Generate a new ID for the post
            new_id = int(max(post['id'] for post in POSTS) + 1)
            new_post['id'] = new_id
            # Add the new post to our list
            POSTS.append(new_post)
            return jsonify(new_post), 201
    else:
        # Handle the GET request
        sort_field = request.args.get('sort', None)
        direction = request.args.get('direction', 'asc')

        # Validate the sort field and direction
        if sort_field and sort_field not in ['title', 'content']:
            return jsonify({"error": "Invalid sort field. It should be 'title' or 'content'."}), 400

        if direction not in ['asc', 'desc']:
            return jsonify({"error": "Invalid direction. It should be 'asc' or 'desc'."}), 400

        # Sort the posts if sorting parameters are provided
        if sort_field:
            POSTS.sort(key=lambda x: x[sort_field].lower(), reverse=(direction == 'desc'))

        return jsonify(POSTS)


def find_post_by_id(post_id):
    """Find the post with the id `post_id`. If there is no post with this id, return None."""
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return '', 404

    # Remove the post from the list
    POSTS.remove(post)

    # Return the message
    return jsonify(f"Post with id {id} has been deleted successfully.")


@app.route('/api/posts/<int:id>', methods=['PUT'])
def handle_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return '', 404

    # Update the post with the new data
    new_data = request.get_json()
    post.update(new_data)

    # Return the updated post
    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()


    matching_posts = []

    for post in POSTS:
        title_match = title_query in post['title'].lower() if title_query else True
        content_match = content_query in post['content'].lower() if content_query else True


        if title_match or content_match:
            matching_posts.append(post)

    return jsonify(matching_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
