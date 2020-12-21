from sample.app import Application
from horseman.response import Response


app = Application()


@app.route('/hello/minimal')
def minimal(request):
    return Response.to_json(body={'message': 'Hello, World!'})


@app.route('/hello/with/{parameter}')
def parameter(request, parameter):
    return Response.to_json(body={'parameter': parameter})


@app.route('/hello/cookie')
def cookie(request):
    response = Response.to_json(body={'cookie': request.cookies['test']})
    response.cookies.set(name='bench', value='value')
    return response


@app.route('/hello/query')
def query(request):
    response = Response.to_json(body={'query': request.query.get('query')})
    return response


@app.route('/hello/full/with/{one}/and/{two}')
def full(request, one, two):
    response = Response.to_json(body={
        'parameters': f'{one} and {two}',
        'query': request.query.get('query'),
        'cookie': request.cookies['test'],
    })
    response.cookies.set(name='bench', value='value')
    return response


if __name__ == '__main__':
    import bjoern
    bjoern.run(app, '127.0.0.1', 8000)
