#coding: utf-8

from exceptions import EngageException

from lxml import etree
from copy import deepcopy
import requests

class EngageApi(object):
    ENVELOPE_TEMPLATE = etree.XML(u'<Envelope><Body></Body></Envelope>')

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.jsessionid = ''

    def __envelope(self):
        return deepcopy(self.ENVELOPE_TEMPLATE)

    def __post(self, xml):
        data = {'xml': xml}
        url = 'https://{endpoint};jsessionid={jsessionid}'.format(endpoint=self.endpoint, jsessionid=self.jsessionid)
        #response = requests.request('POST', 'https://' + self.endpoint + ';jsessionid=' + self.jsessionid, data=data)
        response = requests.post(url, data=data)
        response = etree.XML(response.content)
        if not self.__success(response):
            raise EngageException
        return response

    def __success(self, xml):
        return xml.xpath('//SUCCESS/text()')[0].lower() == 'true'

    def __getSessionId(self, xml):
        return xml.xpath('//SESSIONID/text()')[0]

    def login(self, username, password):
        requestEnvelope = self.__envelope()
        body = requestEnvelope.xpath('Body')[0]
        actionElement = etree.SubElement(body, 'Login')
        etree.SubElement(actionElement, 'USERNAME').text = username
        etree.SubElement(actionElement, 'PASSWORD').text = password
        xml = etree.tostring(requestEnvelope)
        responseEnvelope = self.__post(xml)
        self.jsessionid = self.__getSessionId(responseEnvelope)

    def logout(self):
        requestEnvelope = self.__envelope()
        body = requestEnvelope.xpath('Body')[0]
        etree.SubElement(body, 'Logout')
        xml = etree.tostring(requestEnvelope)
        responseEnvelope = self.__post(xml)
        if self.__success(responseEnvelope):
            self.jsessionid = ''

