#!/usr/bin/env python

from hvac import Client
from ast import literal_eval

from helpers.kms_encrypt import KmsEncrypt
from helpers.kms_decrypt import KmsDecrypt
from helpers.s3_vault import S3Vault
from helpers.args import Args
from helpers.log import SetLogging


class VaultMonitor(object):

    def __init__(self, hostname,
                 aws_region=None,
                 key_alias=None,
                 bucket_alias=None):
        self.hostname = hostname
        self.aws_region = aws_region
        self.key_alias = key_alias
        self.bucket_alias = bucket_alias
        self.verify = True

    def logger(self, level, msg, exit_code=None):
        return SetLogging().log(level, msg, exit_code)

    def client(self, host, token=None):
        return Client(url="https://{0}:8200".format(host),
                      token=token,
                      verify=self.verify)

    def verify_initialization(self):
        """
        :return: True if vault is initialized and False if not
        """
        return self.client(host=self.hostname).is_initialized()

    def initialize_vault(self, shares, threshold):
        """
        :param shares: number of shares to be created
        :param threshold: threshold of shares needed to unlock vault
        :return: n shares and one root token in json format
        """
        return self.client(host=self.hostname).initialize(shares, threshold)

    def encrypt_vault_tokens(self, data):
        """
        :param data: data to be encrypted by kms
        :return: kms base64 encoded encrypted data
        """
        return KmsEncrypt(region=self.aws_region).return_encrypted_secret(secret=data,
                                                                          key_alias=self.key_alias)

    def store_token_s3(self, encrypted_data):
        """
        :param encrypted_data: encrypted data that will be stored into s3 as a bucket object
        """
        S3Vault(region=self.aws_region, bucket_alias=self.bucket_alias).put_token(encrypted_data=encrypted_data)

    def decrypt_data(self):
        """
        :return: decrypted vault secrets, ie root_token, unlock tokens
        """
        kms_data = S3Vault(region=self.aws_region, bucket_alias=self.bucket_alias).read_token_file()
        return KmsDecrypt(region=self.aws_region).decrypt_secret(base64_ciphertext=kms_data)

    def check_seal(self):
        """
        :return: True if vault is sealed, False if vault is unsealed
        """
        return self.client(self.hostname).is_sealed()

    def get_tokens(self, token_type):
        """
        :param token_type: Options are keys or root token
        :return: secret based off of requested param
        """
        if not self.verify_initialization():
            self.logger("info", "Vault is not initialized, starting initialization...")
            vault_data = self.initialize_vault(shares=5, threshold=3)
            encrypted_tokens = self.encrypt_vault_tokens(data=vault_data)
            self.store_token_s3(encrypted_data=encrypted_tokens)
        decrypted_data = self.decrypt_data()
        return literal_eval(decrypted_data).get(token_type)

    def unseal_vault(self):
        """
        Unseals vault. If tokens do not exist, it will create them.
        """
        root = self.get_tokens(token_type='root_token')
        if self.check_seal():
            self.logger("info", "Vault is sealed...Unlocking now...")
            unlock_keys = self.get_tokens(token_type='keys')
            self.client(self.hostname, token=root).unseal_multi(unlock_keys)
            self.logger("info", "Unsealed vault")
        else:
            self.logger("info", "There are no sealed vaults")


if __name__ == '__main__':
    args = Args.get_args()
    vault = VaultMonitor(hostname=args.hostname, aws_region=args.region,
                         key_alias=args.key_alias, bucket_alias=args.bucket_alias)
    vault.unseal_vault()
