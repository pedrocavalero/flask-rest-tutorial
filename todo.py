from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse
from flask_httpauth import HTTPBasicAuth
import datetime
from flask import request
from functools import wraps

app = Flask(__name__)
api = Api(app)

auth = HTTPBasicAuth()
USER_DATA = {
	"admin": "SuperSecretPwd"
}
#route to verify the password
@auth.verify_password
def verify(username, password):
	if not(username and password):
		return False
	return USER_DATA.get(username) == password

def time(function=None):
    @wraps(function)
    def wrapper(*args, **kwargs):
        s = datetime.datetime.now()
        _ = function(*args, **kwargs)
        e = datetime.datetime.now()
        print("Execution Time : {} ".format(e-s))
        return _
    return wrapper

def monitor(function=None):
    @wraps(function)
    def wrapper(*args, **kwargs):
        _ = function(*args, **kwargs)
        print("Ip Address  : {} ".format(request.remote_user))
        print("Cookies : {} ".format(request.cookies))
        print(request.user_agent)
        return _
    return wrapper

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    @time
    @monitor
    #@auth.login_required
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
