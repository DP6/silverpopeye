#coding: utf-8

from exceptions import EngageException
from lxml import etree
from copy import deepcopy
import requests


class EngageApi(object):
    ENVELOPE_TEMPLATE = etree.XML(u'<Envelope><Body></Body></Envelope>')

    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.encoding = None
        self.jsessionid = ''

    def setEncoding(self, encoding):
        """Set the encondig to be passed to request. If enconding isn't defined,
        the Silverpop Organization's default setting is used.

        -encoding: str ou unicode representing enconde information like 
        in Content-Type Header(e.g. "UTF-8")"""
        self.encoding = encoding

    def __envelope(self):
        """Returns a etree.XML object with the base body of a Silverpop's request"""
        return deepcopy(self.ENVELOPE_TEMPLATE)

    def __get(self, xml):
        pass

    def __post(self, xml):
        data = {'xml': xml}
        headers = {}
        if self.encoding:
            headers['Content-Type'] = 'text/xml;charset={encoding}'.format(encoding=encoding)
        url = 'https://{api_endpoint};jsessionid={jsessionid}'.format(api_endpoint=self.api_endpoint, jsessionid=self.jsessionid)
        response = requests.post(url, data=data, headers=headers)
        response = etree.XML(response.content)
        if not self.__success(response):
            raise EngageException
        return response

    def __success(self, xml):
        """Check if the API's requests has success.

        returns type: boolean"""
        return xml.xpath('//SUCCESS/text()')[0].lower() == 'true'

    def __getSessionId(self, xml):
        return xml.xpath('//SESSIONID/text()')[0]

    def __buildAction(self, action, **optionals):
        requestEnvelope = self.__envelope()
        body = requestEnvelope.xpath('Body')[0]
        actionElement = etree.SubElement(body, action)
        for name, value in optionals.items():
            element = etree.SubElement(actionElement, name)
            if not value:
                continue
            element.text = value
        xml = etree.tostring(requestEnvelope)
        return xml

    def login(self, username, password):
        optionals = {'USERNAME': username,
                        'PASSWORD': password,}
        xml = self.__buildAction('Login', **optionals)
        responseEnvelope = self.__post(xml)
        self.jsessionid = self.__getSessionId(responseEnvelope)

    def logout(self):
        optionals = {}
        xml = self.__buildAction('Logout', **optionals)
        responseEnvelope = self.__post(xml)
        self.jsessionid = ''

    def getAggregateTrackingForUser(self, dateStart, dateEnd, **optionals):
        optionals['DATE_START'] = dateStart
        optionals['DATE_END'] = dateEnd
        xml = self.__buildAction('GetAggregateTrackingForUser', **optionals)
        responseEnvelope = self.__post(xml)
        return responseEnvelope

    def getMailingTemplates(self, visibility, **optionals):
        optionals['VISIBILITY'] = visibility
        xml = self.__buildAction('GetMailingTemplates', **optionals)
        responseEnvelope = self.__post(xml)
        return responseEnvelope
        
