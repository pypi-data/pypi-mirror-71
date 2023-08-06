import sys
from logging import getLogger
from logging import NullHandler

import grpc

import python_liftbridge.api_pb2_grpc

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class BaseClient(object):

    """
        Connect creates a Client connection for the given Liftbridge cluster.
    """

    def __init__(self, ip_address='127.0.0.1:9292', timeout=5, tls_cert=None):
        self.ip_address = ip_address
        self.timeout = timeout
        if tls_cert:
            logger.debug(
                'Creating a secure channel with address: %s' %
                self.ip_address,
            )
            self.channel = self._secure_channel(self.ip_address,tls_cert)
            self.stub = self._connect()
        else:
            logger.debug(
                'Creating an insecure channel with address: %s' % self.ip_address,
            )
            self.channel = grpc.insecure_channel(self.ip_address)
            self.stub = self._connect()

    def _connect(self):
        try:
            grpc.channel_ready_future(
                self.channel,
            ).result(timeout=self.timeout)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        else:
            return python_liftbridge.api_pb2_grpc.APIStub(self.channel)

    def _secure_channel(self, address, secure_file):
        with open(secure_file) as f:
            trusted_certs = f.read().encode()
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        return grpc.secure_channel(address, credentials)
        

    def close(self):
        logger.debug('Closing channel')
        self.channel.close()

    def __repr__(self):
        return str(self.__dict__)
