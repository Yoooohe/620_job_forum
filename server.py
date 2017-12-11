from flask import (Flask, Response, request, render_template, make_response,
                   redirect)
from flask_restful import Api, Resource, reqparse, abort

import json
import random
import string
from datetime import datetime
from functools import wraps

with open('data.json') as data:
    data = json.load(data)


def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    return Response(
        'Please authenticate yourself', 401,
        {'WWW-Authenticate': 'Basic realm="message"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def generate_mid(size=6, chars=string.ascii_lowercase + string.digits):
    return 'm'+''.join(random.choice(chars) for _ in range(size))


def generate_rid(size=6, chars=string.ascii_lowercase + string.digits):
    return 'r'+''.join(random.choice(chars) for _ in range(size))


# Respond with 404 Not Found if no help ticket with the specified ID exists.
def error_if_message_not_found(message_id):
    if message_id not in data['discussion_list']['discussion_industry&company']['messages']:
        message = "No message with ID: {}".format(message_id)
        abort(404, message=message)



def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s


new_message_parser = reqparse.RequestParser()
for arg in ['Author', 'Title', 'MContent']:
    new_message_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))


new_reply_parser = reqparse.RequestParser()
for arg in ['Author', 'Title', 'RContent']:
    new_reply_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))

update_message_parser = reqparse.RequestParser()
update_message_parser.add_argument(
    'Title', type=str, default='')
update_message_parser.add_argument(
    'MContent', type=str, default='')


def render_message_as_html(message):
    return render_template(
        'message.html',
        message=message)


def render_discussion_as_html(discussion):
    # print(discussion)
    return render_template(
        'discussion.html',
        discussion = discussion)


class Reply(Resource):

    # If a help ticket with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, reply_id, message_id):
        error_if_message_not_found(reply_id)
        return make_response(
            render_message_as_html(
                data['discussion_list']['discussion_industry&company']['messages'][message_id]['replies']), 200)

    # If a help ticket with the specified ID does not exist,
    # respond with a 404, otherwise update the help ticket and respond
    # with the updated HTML representation.
    # @requires_auth
    # def patch(self, message_id):
    #     error_if_message_not_found(message_id)
    #     message = data['discussion_list']['discussion_industry&company']['messages'][message_id]
    #     update = update_message_parser.parse_args()
    #     if len(update['Title'].strip()) > 0:
    #         message.setdefault('Title', []).append(update['Title'])
    #     return make_response(
    #         render_message_as_html(message), 200)


class Message(Resource):

    # If a help ticket with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, message_id):
        error_if_message_not_found(message_id)
        return make_response(
            render_message_as_html(
                data['discussion_list']['discussion_industry&company']['messages'][message_id]), 200)

    # If a help ticket with the specified ID does not exist,
    # respond with a 404, otherwise update the help ticket and respond
    # with the updated HTML representation.
    @requires_auth
    def patch(self, message_id):
        error_if_message_not_found(message_id)
        message = data['discussion_list']['discussion_industry&company']['messages'][message_id]
        update = update_message_parser.parse_args()
        if len(update['Title'].strip()) > 0:
            message.setdefault('Title', []).append(update['Title'])
        return make_response(
            render_message_as_html(message), 200)

    # post reply to message
    def post(self,message_id):
        reply = new_reply_parser.parse_args()
        reply_id = generate_rid()
        reply['ID'] = 'request/' + reply_id
        reply['Time'] = datetime.isoformat(datetime.now())
        data['discussion_list']['discussion_industry&company']['messages'][message_id]['replies'][reply_id] = reply
        return make_response(
            render_message_as_html(data['discussion_list']['discussion_industry&company']['messages'][message_id]), 201)

    @requires_auth
    def delete(self, message_id):
        del data['discussion_list']['discussion_industry&company']['messages'][message_id]
        return make_response(
            render_discussion_as_html(data['discussion_list']['discussion_industry&company']), 200)




class MessagetAsJSON(Resource):

    # If a help ticket with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, message_id):
        error_if_message_not_found(message_id)
        message = data['discussion_list']['discussion_industry&company']['messages'][message_id]
        message['@context'] = data['@context']
        return message


class Discussion(Resource):
    # Respond with an HTML representation of the help ticket list, after
    # applying any filtering and sorting parameters.
    def get(self):
        return make_response(
            render_discussion_as_html(data['discussion_list']['discussion_industry&company']), 200)


    def post(self):
        message = new_message_parser.parse_args()
        print(message)
        message_id = generate_mid()
        message['ID'] = 'request/' + message_id
        message['Time'] = datetime.isoformat(datetime.now())
        data['discussion_list']['discussion_industry&company']['messages'][message_id] = message
        data['discussion_list']['discussion_industry&company']['messages'][message_id]['replies'] = {}
        return make_response(
            render_discussion_as_html(data['discussion_list']['discussion_industry&company']), 201)

    @requires_auth
    def delete(self, message_id):
        del data['discussion_list']['discussion_industry&company']['messages'][message_id]
        return make_response(
            render_discussion_as_html(data['discussion_list']['discussion_industry&company']), 200)


class DiscussionAsJSON(Resource):
    def get(self):
        return data['discussion_list']['discussion_industry&company']



app = Flask(__name__)
api = Api(app)
api.add_resource(Discussion, '/discussion')
api.add_resource(DiscussionAsJSON, '/discussion.json')
api.add_resource(Message, '/discussion/<string:message_id>')
api.add_resource(MessagetAsJSON, '/discussion/<string:message_id>.json')


@app.route('/')
def index():
    return redirect(api.url_for(Discussion), code=303)


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Now we can start the server.

if __name__ == '__main__':  ## entrance
    app.run(
        host='0.0.0.0',
        port=5555,
        debug=True,
        use_debugger=False,
        use_reloader=False)


# /<string:discussion_id>