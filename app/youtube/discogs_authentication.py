import discogs_client

from conf.configurator import get_values_section, get_value, set_value


def authenticate():
    access_token = get_value('discogs', 'oauth_token')
    if access_token is None or access_token in ('', ' ', False):
        return oauth_authentication_req()
    else:
        conf = get_stored_credentials()
        ds = discogs_client.Client(
            conf['user_agent'],
            consumer_key=conf['consumer_key'],
            consumer_secret=conf['consumer_secret'],
            token=conf['oauth_token'],
            secret=conf['oauth_token_secret']
        )
        me = ds.identity()
        return ds


def oauth_authentication_req():
    conf = get_stored_credentials()

    consumer_key = conf['consumer_key']
    consumer_secret = conf['consumer_secret']

    d = discogs_client.Client(conf['user_agent'])
    d.set_consumer_key(consumer_key, consumer_secret)

    token, secret, url = d.get_authorize_url()
    print('Please browse to the following URL {0}'.format(url))

    verifier = input("'Verification code :'")
    access_token, access_secret = d.get_access_token(verifier)
    me = d.identity()
    print("I'm {0} ({1}) from {2}.".format(me.name, me.username, me.location))

    # fixme not sure if values get saved
    set_value('discogs', 'oauth_token', access_token)
    set_value('discogs', 'oauth_token_secret', access_secret)
    return d


def get_stored_credentials():
    user_settings = get_values_section('discogs')
    return user_settings
