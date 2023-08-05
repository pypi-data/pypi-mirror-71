# -- coding:utf-8 --
import base64
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from .LMServiceError import ServiceErrorCode


class RSAUtil(object):
    """ RSA加密工具类

    """

    @staticmethod
    def rsaEncrypt(content, publicKey):
        """ RSA加密

        :param content: 待加密的内容
        :param publicKey: 公钥
        :return:<str> 密文
        """
        default_lenth = 117
        msg_lenth = len(content)
        byte_content = content.encode()
        pubilc_key = "-----BEGIN PUBLIC KEY-----\n" + publicKey + "\n-----END PUBLIC KEY-----"
        cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(pubilc_key))

        if msg_lenth < default_lenth:
            encrypt_text = cipher.encrypt(byte_content)
            return base64.encodebytes(encrypt_text).decode()
        else:
            offset = 0
            encrypt_slice = []
            while msg_lenth - offset > 0:
                if msg_lenth - offset > default_lenth:
                    encrypt_text_slice = cipher.encrypt(byte_content[offset:offset+default_lenth])
                    encrypt_slice.append(encrypt_text_slice)
                else:
                    encrypt_text_slice = cipher.encrypt(byte_content[offset:])
                    encrypt_slice.append(encrypt_text_slice)
                offset += default_lenth
            byte_encrypt_text = b''.join(encrypt_slice)
            return base64.encodebytes(byte_encrypt_text).decode()

    @staticmethod
    def rsaDecrypt(content, privateKey):
        """ RSA解密

        :param content: RSA加密后的内容
        :param privateKey: 私钥
        :return: 明文
        """
        encrypt_text = base64.decodebytes(content.encode())
        default_lenth = 128
        msg_lenth = len(encrypt_text)
        private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + privateKey + "\n-----END RSA PRIVATE KEY-----"
        cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(private_key))
        if msg_lenth < default_lenth:
            decrypt_text = cipher.decrypt(encrypt_text, json.dumps({"code": ServiceErrorCode["SERVICE_ERROR"], "message": "RSA解密失败!"}).encode())
            return decrypt_text.decode()
        else:
            offset = 0
            decrypt_slice = []
            while msg_lenth - offset > 0:
                if msg_lenth - offset > default_lenth:
                    encrypt_text_slice = cipher.decrypt(encrypt_text[offset:offset+default_lenth], json.dumps({"code": ServiceErrorCode["SERVICE_ERROR"], "message": "RSA解密失败!"}).encode())
                    decrypt_slice.append(encrypt_text_slice)
                else:
                    encrypt_text_slice = cipher.decrypt(encrypt_text[offset:], json.dumps({"code": ServiceErrorCode["SERVICE_ERROR"], "message": "RSA解密失败!"}).encode())
                    decrypt_slice.append(encrypt_text_slice)
                offset += default_lenth
            byte_decrypt_text = b''.join(decrypt_slice)
            return byte_decrypt_text.decode()

    @staticmethod
    def rsa2Sign(content, privateKey):
        """ 通过SHA256WithRSA(RSA2)算法进行签名

        :param content: 需要验签的内容.
        :param privateKey: 私钥
        :return: 验签结果
        """
        private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + privateKey + "\n-----END RSA PRIVATE KEY-----"
        signer = Signature_pkcs1_v1_5.new(RSA.importKey(private_key))
        rand_hash = SHA256.new()
        rand_hash.update(content.encode())
        signature = signer.sign(rand_hash).hex()
        return signature
