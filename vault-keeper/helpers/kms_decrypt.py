#!/usr/bin/env python

import base64
from boto3 import Session


class KmsDecrypt(object):

    def __init__(self, region='us-west-2', session=None):
        self.region = region
        self.session = self.configure_session(session_input=session)
        self.client = self.session.client('kms')

    def configure_session(self, session_input):
        if not session_input:
            return Session(region_name=self.region)
        else:
            return session_input

    def decrypt_secret(self, base64_ciphertext):
        blob_ciphertext = base64.b64decode(base64_ciphertext)
        response = self.client.decrypt(CiphertextBlob=blob_ciphertext)
        return response['Plaintext'].replace("\n", "")

