from ariadne import ObjectType, graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

#load_schema
type_defs = load_schema_from_path('./schema.graphql')

#sample data
myStudent = [
    {
        'id': 1,
        'name': "fay"
    }
]

myClass = [
    {
        'id': 1,
        'name': "CMPE273",
        'students':[]
    }
]

#define query filed
query = ObjectType("Query")

@query.field("hello")
def hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent

@query.field("students")
def students(obj,info):
    return myStudent

@query.field("student")
def student(obj,info,id):
    for s in myStudent:
        if s['id']  == id:
            return s
    return None

@query.field("classes")
def students(obj,info):
    return myClass

@query.field("class")
def student(obj,info,id):
    for c in myClass:
        if c['id']  == id:
            return c
    return None

#define mutation filed
mutation = ObjectType("Mutation")

@mutation.field("addStudent")
def addStudent(obj,info,name):
    myStudent.append({'id':len(myStudent)+1, 'name':name})
    return True

@mutation.field("addClass")
def addStudent(obj,info,name):
    myClass.append({'id':len(myClass)+1, 'name':name})
    return True

@mutation.field("enrollClass")
def enrollClass(obj,info,sid,cid):
    for s in myStudent:
        #vaildate sid
        if s['id'] ==  sid:
            for c in myClass:
                ##vaildate cid
                if c['id'] == cid:
                    for ss in c['students']:
                        ###check if student is already in the class
                        if ss['id'] == sid:
                            return False
                        ###
                    c['students'].append(s)
                    return True
                ##sid, cid both validated, student can enroll
            return False
        #
    return False

schema = make_executable_schema(type_defs, query,mutation)
######################DONE WITH GRAPHQL########################

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)