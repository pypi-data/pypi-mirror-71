s3-kvs
======

A python wrapper for an S3 backed key-value store.

Usage
=====

Import and create a client instance, setting a domain and optionally a namespace:


    from s3_kvs import ReadOnlyClient

    client = ReadOnlyClient(domain='kvs.example.com')

    OR

    client = ReadOnlyClient(domain='kvs.example.com', namespace='test')


Then use then use the getitem notation to retrieve values from the key store:

    client['foo']

    > 'bar'

Or, use the get method to provide a default if no matching value is found:

    client.get('foo', 'oops')

    > 'oops'

By default returned values are text. You can also treat them as json and automatically parse them:

    text_client = ReadOnlyClient(domain='kvs.example.com')

    client['foo']

    > '{"bar": "baz"}'  # a json string

    json_client = ReadOnlyClient(domain='kvs.example.com', value_format='json')

    client['foo']

    > {'bar': 'baz'}  # a python dict
