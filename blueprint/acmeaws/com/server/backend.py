import boto
import boto.exception
import httplib
import socket

from blueprint import cfg
import librato
import statsd

import boto.s3


AWS_ACCESS_KEY_ID = cfg.get('s3', 'access_key')
AWS_SECRET_ACCESS_KEY = cfg.get('s3', 'secret_key')
bucket = cfg.get('s3', 'bucket')
region = cfg.get('s3', 'region')
s3_region = 's3' if 'US' == region else 's3-{0}'.format(region)

'''
bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)


bucket = conn.create_bucket(bucket_name,
    location=boto.s3.connection.Location.DEFAULT)

testfile = "replace this with an actual filename"
print 'Uploading %s to Amazon S3 bucket %s' % \
   (testfile, bucket_name)

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


k = Key(bucket)
k.key = 'my test file'
k.set_contents_from_filename(testfile,
    cb=percent_cb, num_cb=10)

'''


def delete(key):
    content_length = head(key)
    if content_length is None:
        return None
    librato.count('blueprint-acmeaws-com-server.requests.delete')
    statsd.increment('blueprint-acmeaws-com-server.requests.delete')

    c = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket(bucket, validate=False)
    try:
        b.delete_key(key)
        statsd.update('blueprint-acmeaws-com-server.storage', -content_length)
    except (boto.exception.BotoClientError,
            boto.exception.BotoServerError,
            httplib.HTTPException,
            socket.error,
            socket.gaierror):
        return False


def delete_blueprint(secret, name):
    return delete(key_for_blueprint(secret, name))


def delete_tarball(secret, name, sha):
    return delete(key_for_tarball(secret, name, sha))


def get(key):
    librato.count('blueprint-acmeaws-com-server.requests.get')
    statsd.increment('blueprint-acmeaws-com-server.requests.get')
    c = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket(bucket, validate=False)
    k = b.new_key(key)
    try:
        return k.get_contents_as_string()
    except (boto.exception.BotoClientError,
            boto.exception.BotoServerError,
            httplib.HTTPException,
            socket.error,
            socket.gaierror):
        return False


def get_blueprint(secret, name):
    return get(key_for_blueprint(secret, name))


def get_tarball(secret, name, sha):
    return get(key_for_tarball(secret, name, sha))


def head(key):
    librato.count('blueprint-acmeaws-com-server.requests.head')
    statsd.increment('blueprint-acmeaws-com-server.requests.head')
    c = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket(bucket, validate=False)
    try:
        k = b.get_key(key)
        if k is None:
            return None
        return k.size
    except (boto.exception.BotoClientError,
            boto.exception.BotoServerError,
            httplib.HTTPException,
            socket.error,
            socket.gaierror):
        return False


def head_blueprint(secret, name):
    return head(key_for_blueprint(secret, name))


def head_tarball(secret, name, sha):
    return head(key_for_tarball(secret, name, sha))


def key_for_blueprint(secret, name):
    return '{0}/{1}/{2}'.format(secret, name, 'blueprint.json')


def key_for_tarball(secret, name, sha):
    return '{0}/{1}/{2}.tar'.format(secret, name, sha)


def list(key):
    librato.count('blueprint-acmeaws-com-server.requests.list')
    statsd.increment('blueprint-acmeaws-com-server.requests.list')
    c = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket(bucket, validate=False)
    try:
        return b.list(key)
    except (boto.exception.BotoClientError,
            boto.exception.BotoServerError,
            httplib.HTTPException,
            socket.error,
            socket.gaierror):
        return False


def put(key, data):
    librato.count('blueprint-io-server.requests.put')
    statsd.increment('blueprint-io-server.requests.put')
    statsd.update('blueprint-io-server.storage', len(data))
    c = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket(bucket, validate=False)
    k = b.new_key(key)
    try:
        k.set_contents_from_string(data,
                                   policy='public-read',
                                   reduced_redundancy=True)
        return True
    except (boto.exception.BotoClientError,
            boto.exception.BotoServerError,
            httplib.HTTPException,
            socket.error,
            socket.gaierror):
        return False


def put_blueprint(secret, name, data):
    return put(key_for_blueprint(secret, name), data)


def put_tarball(secret, name, sha, data):
    return put(key_for_tarball(secret, name, sha), data)


def url_for(key):
    return 'https://{0}.{1}.amazonaws.com/{2}'.format(bucket, s3_region, key)


def url_for_blueprint(secret, name):
    return url_for(key_for_blueprint(secret, name))


def url_for_tarball(secret, name, sha):
    return url_for(key_for_tarball(secret, name, sha))