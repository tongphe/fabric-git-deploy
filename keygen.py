__author__ = 'tongphe'

import uuid
import base64
import hashlib
import string

class Keygen(str):
	__secret = 'iRxECyMNNFLS740V9VDGFkR'

	def __new__(self):
		uuid1 = str(uuid.uuid1())
		uuid2 = str(uuid.uuid1())
		digest = hashlib.sha256(uuid1 + self.__secret + uuid2).digest()
		digest = base64.b64encode(digest)
		digest = digest.translate(string.maketrans('+/=', 'xyz'))
		return digest

print Keygen()
