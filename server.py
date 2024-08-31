from flask import Flask, request, Response
import requests
import os
import logging
import json

app = Flask(__name__)

# SOCKS5 proxy configuration from environment variable
socks_proxy = os.getenv('SOCKS_PROXY')
if not socks_proxy:
    raise EnvironmentError('SOCKS_PROXY environment variable is not set')

proxies = {
    'http': socks_proxy,
    'https': socks_proxy,
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Load authorized tokens from JSON file
with open('authorized_tokens.json') as f:
    authorized_tokens = json.load(f)['tokens']


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    # Check for the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response('Forbidden', status=403)

    token = auth_header.split(' ')[1]
    if token not in authorized_tokens:
        return Response('OpenAI token not authorized in Proxy', status=403)

    url = f'https://api.openai.com/{path}'
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            proxies=proxies,
            stream=True  # Enable streaming
        )

        logger.info(f"Request from {request.remote_addr} to {url}")

        headers = [(name, value) for name, value in response.raw.headers.items()]

        def generate():
            try:
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk
            except requests.RequestException as e:
                print(e)

        return Response(generate(), response.status_code, headers)
    except requests.RequestException as e:
        print(e)
        return Response('Proxy error', status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
