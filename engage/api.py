#coding: utf-8

from exceptions import EngageException
from lxml import etree
from copy import deepcopy
import requests


class EngageApi(object):
    ENVELOPE_TEMPLATE = etree.XML(u'<Envelope><Body></Body></Envelope>')

    def __init__(self, api_endpoint, ftp_endpoint=None):
        """.

        parameters
            -api_endpoint: str ou unicode with the URL of the endpoint used
            by you account.
            -ftp_endpoint: str ou unicode with the URL of the endpoint used
            by you account."""
        self.api_endpoint = api_endpoint
        self.ftp_endpoint = ftp_endpoint
        #self.encoding = None
        self.jsessionid = ''

    def setEncoding(self, encoding):
        """Set the encondig pass to the request. If enconding isn't defined,
        the Silverpop Organization's default setting is used.

        parameters
            -encoding: str ou unicode representinf enconding information like 
            in Content-Type Header(e.g. "UTF-8")"""
        self.encoding = encoding

    def __envelope(self):
        """Returns the base XML body of a Silverpop's request

        return type: ElementTree"""
        return deepcopy(self.ENVELOPE_TEMPLATE)

    def __post(self, xml, encoding=None):
        data = {'xml': xml}
        headers = {}
        if encoding:
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

    def __buildAction(self, action, **parameters):
        requestEnvelope = self.__envelope()
        body = requestEnvelope.xpath('Body')[0]
        actionElement = etree.SubElement(body, action)
        for name, value in parameters.items():
            etree.SubElement(actionElement, name).text = value
        xml = etree.tostring(requestEnvelope)
        return xml

    def login(self, username, password):
        parameters = {'USERNAME': username,
                        'PASSWORD': password,}
        xml = self.__buildAction('Login', **parameters)
        responseEnvelope = self.__post(xml)
        self.jsessionid = self.__getSessionId(responseEnvelope)

    def logout(self):
        parameters = {}
        xml = self.__buildAction('Logout', **parameters)
        responseEnvelope = self.__post(xml)
        self.jsessionid = ''

    def getAggregateTrackingForUser(self, dateStart, dateEnd, **parameters):
        parameters = {'DATE_START': dateStart,
                        'DATE_END': dateEnd,}
        xml = self.__buildAction('GetAggregateTrackingForUser', **parameters)
        responseEnvelope = self.__post(xml)
        return responseEnvelope

    def getMailingTemplates(self, visibility, **parameters):
        parameters = {'VISIBILITY': visibility,}
        xml = self.__buildAction('GetMailingTemplates', **parameters)
        responseEnvelope = self.__post(xml)
        return responseEnvelope