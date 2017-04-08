#!/usr/bin/env python

from boto3 import Session
from base64 import b64encode


class KmsEncrypt(object):

    def __init__(self, region=None, session=None):
        self.region = region
        self.session = self.configure_session(session_input=session)
        self.client = self.session.client('kms', region_name=region)

    def configure_session(self, session_input):
        if not session_input:
            return Session(region_name=self.region)
        else:
            return session_input

    def return_encrypted_secret(self, secret=None, key_alias=None):
        result = self.client.encrypt(KeyId='alias/{0}'.format(key_alias),
                                     Plaintext=b'{0}'.format(secret)
                                     )
        return b64encode(result['CiphertextBlob'])

