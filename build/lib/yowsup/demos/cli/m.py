# import Cli
# import clicmd
from yowsup.demos.cli import cli 
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
import sys
from yowsup.common import YowConstants
import datetime
import time
import os
import logging
import threading
import base64
from yowsup.layers.protocol_groups.protocolentities import *
from yowsup.layers.protocol_presence.protocolentities import *
from yowsup.layers.protocol_messages.protocolentities import *
from yowsup.layers.protocol_ib.protocolentities import *
from yowsup.layers.protocol_iq.protocolentities import *
from yowsup.layers.protocol_contacts.protocolentities import *
from yowsup.layers.protocol_chatstate.protocolentities import *
from yowsup.layers.protocol_privacy.protocolentities import *
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities import *
from yowsup.common.tools import Jid
from yowsup.common.optionalmodules import PILOptionalModule
from yowsup.layers.axolotl.protocolentities.iq_key_get import GetKeysIqProtocolEntity


class YowsupCliLayer(YowInterfaceLayer):
    PROP_RECEIPT_AUTO = "org.openwhatsapp.yowsup.prop.cli.autoreceipt"
    PROP_RECEIPT_KEEPALIVE = "org.openwhatsapp.yowsup.prop.cli.keepalive"
    PROP_CONTACT_JID = "org.openwhatsapp.yowsup.prop.cli.contact.jid"
    EVENT_LOGIN = "org.openwhatsapp.yowsup.event.cli.login"
    EVENT_START = "org.openwhatsapp.yowsup.event.cli.start"
    EVENT_SENDANDEXIT = "org.openwhatsapp.yowsup.event.cli.sendandexit"

    MESSAGE_FORMAT = "[%s(%s)]:[%s]\t %s"

    FAIL_OPT_PILLOW = "No PIL library installed, try install pillow"
    FAIL_OPT_AXOLOTL = "axolotl is not installed, try install python-axolotl"

    DISCONNECT_ACTION_PROMPT = 0
    DISCONNECT_ACTION_EXIT = 1

    ACCOUNT_DEL_WARNINGS = 4

    def __init__(self):
        super(YowsupCliLayer, self).__init__()
        YowInterfaceLayer.__init__(self)
        self.accountDelWarnings = 0
        self.connected = True
        self.username = None
        self.sendReceipts = True
        self.sendRead = True
        self.disconnectAction = self.__class__.DISCONNECT_ACTION_PROMPT

        # add aliases to make it user to use commands. for example you can then do:
        # /message send foobar "HI"
        # and then it will get automaticlaly mapped to foobar's jid
        self.jidAliases = {
            "Siddharth": "916204556171@s.whatsapp.net"
        }

    ######################################

    # @clicmd("Send message to a friend")
    def assertConnected(self):
        if self.connected:
            return True
        else:
            self.output("Not connected", tag = "Error", prompt = False)
            return False

    # @clicmd("Send an image with optional caption")
    def image_send(self, number, path, caption=None):
        self.media_send(
            number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE)
    def onRequestUploadResult(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):

        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendMedia(mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: self.doSendMedia(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, self.onUploadError, self.onUploadProgress, asynchronous=False)
            mediaUploader.start()


    def media_send(self, number, path, mediaType, caption=None):
        if self.assertConnected():
            jid = '916204556171@s.whatsapp.net'
            entity = RequestUploadIqProtocolEntity(mediaType, filePath=path)

            def successFn(successEntity, originalEntity): return self.onRequestUploadResult(
                jid, mediaType, path, successEntity, originalEntity, caption)
            def errorFn(errorEntity, originalEntity): return self.onRequestUploadError(
                jid, path, errorEntity, originalEntity)
            self._sendIq(entity, successFn, errorFn)

    def doSendMedia(self, mediaType, filePath, url, to, ip=None, caption=None):
        if mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
            entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(
                filePath, url, ip, to, caption=caption)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
            entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(
                filePath, url, ip, to)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
            entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(
                filePath, url, ip, to, caption=caption)
        self.toLower(entity)

    def output(self, message, tag = "general", prompt = True):
        print("hi")


        self.lastPrompt = prompt

        if tag is not None:
            print("%s: %s" % (tag, message))
        else:
            print(message)
        if prompt:
            self.printPrompt()
    

a=YowsupCliLayer()
a.image_send(916204556171,'/Users/siddharthdeo/Downloads/yowsup-cli-2.0/pro2file.jpeg')