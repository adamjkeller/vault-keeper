#!/usr/bin/env python

import logging
from boto3 import Session


class S3Vault(object):

    def __init__(self, region, bucket_alias, session=None):
        self.region = region
        self.bucket_alias = bucket_alias
        self.filename = "root_token"
        self.session = self.configure_session(session_input=session)
        self.client = self.session.client('s3', region_name=region)

    def configure_session(self, session_input):
        if not session_input:
            return Session(region_name=self.region)
        else:
            return session_input

    def read_token_file(self):
        return self.client.get_object(Bucket=self.bucket_alias, Key=self.filename).get('Body').read().strip('vault_token: ')

    def put_token(self, encrypted_data):
        logging.info("Putting encrypted_data: {0} in bucket: {1}".format(encrypted_data, self.bucket_alias))
        self.client.put_object(Bucket=self.bucket_alias,
                               Body=b'{0}'.format(encrypted_data),
                               Key=self.filename)

