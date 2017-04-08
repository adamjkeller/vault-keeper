#!/usr/bin/env python

import argparse


class Args(object):

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('-H',
                            '--hostname',
                            action='store',
                            dest='hostname',
                            default='',
                            help='Vault Hostname',
                            type=str,
                            required=True)
        parser.add_argument('-r',
                            '--region',
                            action='store',
                            dest='region',
                            help='AWS Region',
                            type=str,
                            required=True)
        parser.add_argument('-b',
                            '--bucket-alias',
                            action='store',
                            dest='bucket_alias',
                            help='Name of bucket',
                            type=str,
                            required=True)
        parser.add_argument('-k',
                            '--key-alias',
                            action='store',
                            dest='key_alias',
                            help='Name of KMS key alias',
                            type=str,
                            required=True)
        return parser.parse_args()


if __name__ == '__main__':
    args = Args
    print args.get_args()
