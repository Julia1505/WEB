import cgi

def app(environ, start_response):
    post_env = environ.copy()
    get_parameters = ("GET PARAMETERS:\n" + environ['QUERY_STRING'] + "\n").encode('utf-8')

    post_env['QUERY_STRING'] = ''
    post = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=post_env,
        keep_blank_values=True
    )
    post_parameters = "POST PARAMETERS:\n"
    for key in post.keys():
        value = str(post.getvalue(key))
        post_parameters += str(key + " : " + value) + "\n"

    post_parameters = post_parameters.encode('utf-8')

    data =get_parameters + post_parameters
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    print(post)
    start_response(status, response_headers)
    return iter([data])
