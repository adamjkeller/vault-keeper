# Vault Keeper

Monitors Vault and does the following:

- Check if the vault is initialized, if not, it will initialize it and encrypt the root token (KMS) and store it for that stack.
- Check if vault is sealed, if so, it will unseal it using the KMS encrypted root token and unlock tokens (3 total)

# Install

```
docker pull adam9098/vault-keeper:latest
```

# Usage

This can be ran ad-hoc, or on a regularly scheduled interval. When running, make sure that the user/instance running
this has the ability to encrypt/decrypt kms keys and access the specified bucket.

```
docker run -ti adam9098/vault-keeper -r region -b bucket_name -k key_alias
```

```
usage: vault_keeper.py [-h] -H HOSTNAME -r REGION -b BUCKET_ALIAS -k KEY_ALIAS

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Vault Hostname
  -r REGION, --region REGION
                        AWS Region
  -b BUCKET_ALIAS, --bucket-alias BUCKET_ALIAS
                        Name of bucket
  -k KEY_ALIAS, --key-alias KEY_ALIAS
                        Name of KMS key alias
```

# Requirements

- Vault (https://www.vaultproject.io/)

- Amazon Web Services (S3, KMS)
