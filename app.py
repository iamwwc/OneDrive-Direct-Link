# coding=utf-8
import requests
from flask import Flask, request, Response, send_file
from cachetools.func import ttl_cache

app = Flask(__name__,static_url_path='/')


@ttl_cache(1024, ttl=600)
def get_direct_url(ch, share_token):
    url_step1 = 'https://1drv.ms/{ch}/s!{share_token}'.format(
        ch=ch,  # the ch could be w u t or more
        share_token=share_token
    )
    resp_step1 = requests.get(url_step1, timeout=10, allow_redirects=False)
    url_step2 = resp_step1.headers['Location']
    url_step3 = url_step2.replace('/redir?', '/download?')
    resp_step3 = requests.get(url_step3, timeout=10, allow_redirects=False)
    url_final = resp_step3.headers['Location']

    return url_final


@app.route('/<ch>/s!<share_token>')
def share_ts(ch, share_token):
    url_direct = get_direct_url(ch, share_token)

    if 'txt' in request.args:
        # display plain text
        return url_direct
    else:
        # 301 redirect
        return Response('',
                        status=301,
                        headers={'Location': url_direct},
                        content_type='text/plain'
                        )


@app.route('/')
def index():
    return send_file('index.html')


if __name__ == '__main__':
    app.run()
