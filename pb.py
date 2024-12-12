from Cryptodome.Cipher import AES
from pubnub.crypto import PubNubCryptoModule, AesCbcCryptoModule
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
# pn_config.uuid = config.get("GOOGLE_ADMIN_ID")
pn_config.secret_key = config.get("PUBNUB_SECRET_KEY")
pn_config.cipher_key = cipher_key
pn_config.cipher_mode = AES.Mode_GCM
pn_config.fallback_cipher_mode = AES.MODE_CBC
pn_config.crypto_module = AesCbcCryptoModule(pn_config)
pubnub = PubNub(pn_config)


def revoke_access(Token):
    envelope = pubnub.revoke_token(Token)


def parse_token(Token):
    token_details = pubnub.parse_token(Token)
    print("Parsing the token")
    print(token_details)
    #check the what the values for the read and write are saved as (i.e. are they read or Read)
    # uuid = token_details["authorized_uuid"]
    return token_details["timestamp"], token_details["ttl"]
