import sys
import logging

from msal_extensions import *


def build_persistence(location, fallback_to_plaintext=False):
    if sys.platform.startswith('win'):
        return FilePersistenceWithDataProtection(location)
    if sys.platform.startswith('darwin'):
        return KeychainPersistence(location, "my_service_name", "my_account_name")
    if sys.platform.startswith('linux'):
        try:
            return LibsecretPersistence(
                location,
                schema_name="my_schema_name",
                attributes={"my_attr1": "foo", "my_attr2": "bar"},
                )
        except:
            if not fallback_to_plaintext:
                raise
            logging.exception("Encryption unavailable. Opting in to plain text.")
    return FilePersistence(location)
