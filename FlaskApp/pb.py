from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.uuid import UUID
from pubnub.models.consumer.v3.group import Group
from .config import config

pn_config = PNConfiguration()

cipher_key = config.get("PUBNUB_CIPHER_KEY")
pn_config.publish_key = config.get("PUBNUB_PUBLISH_KEY")
pn_config.subscribe_key = config.get("PUBNUB_SUBSCRIBE_KEY")
pn_config.uuid = config.get("GOOGLE_ADMIN_ID")
pn_config.secret_key = config.get("PUBNUB_SECRET_KEY")
#pn_config.cipher_key = cipher_key
pubnub = PubNub(pn_config)


def grant_read_write_access(Email_Address):
    print(f"GRANTING READ AND WRITE ACCESS {Email_Address}")
    envelope = pubnub.grant_token() \
    .channels([Channel.id("Tempify-Channel").read().write()]) \
    .authorized_uuid(Email_Address) \
    .ttl(60) \
    .sync()
    return envelope.result.Token


def grant_read_access(Email_Address):
    print(f"GRANTING READ ACCESS {Email_Address}")
    envelope = pubnub.grant_token() \
    .channels([Channel.id("Tempify-Channel").read()]) \
    .authorized_uuid(Email_Address) \
    .ttl(60) \
    .sync()
    return envelope.result.Token


def grant_write_access(Email_Address):
    print(f"GRANTING WRITE ACCESS {Email_Address}")
    envelope = pubnub.grant_token() \
    .channels([Channel.id("Tempify-Channel").write()]) \
    .authorized_uuid(Email_Address) \
    .ttl(60) \
    .sync()
    return envelope.result.Token


def revoke_access(Token):
    envelope = pubnub.revoke_token(Token)


def parse_token(Token):
    token_details = pubnub.parse_token(Token)
    print("Parsing the token")
    print(token_details)
    #check the what the values for the read and write are saved as (i.e. are they read or Read)
    read_access = token_details["resources"]["channels"]["Tempify-Channel"]["read"]
    write_access = token_details["resources"]["channels"]["Tempify-Channel"]["write"]
    uuid = token_details["authorized_uuid"]
    return token_details["timestamp"], token_details["ttl"], uuid, read_access, write_access
