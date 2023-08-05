# coding: utf-8

"""
    Tator REST API

    Interface to the Tator backend.  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tator_openapi.configuration import Configuration


class BadRequestResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'details': 'str',
        'message': 'str'
    }

    attribute_map = {
        'details': 'details',
        'message': 'message'
    }

    def __init__(self, details=None, message=None, local_vars_configuration=None):  # noqa: E501
        """BadRequestResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._details = None
        self._message = None
        self.discriminator = None

        if details is not None:
            self.details = details
        if message is not None:
            self.message = message

    @property
    def details(self):
        """Gets the details of this BadRequestResponse.  # noqa: E501

        Detailed error message for bad request.  # noqa: E501

        :return: The details of this BadRequestResponse.  # noqa: E501
        :rtype: str
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this BadRequestResponse.

        Detailed error message for bad request.  # noqa: E501

        :param details: The details of this BadRequestResponse.  # noqa: E501
        :type details: str
        """

        self._details = details

    @property
    def message(self):
        """Gets the message of this BadRequestResponse.  # noqa: E501

        Error message for bad request.  # noqa: E501

        :return: The message of this BadRequestResponse.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this BadRequestResponse.

        Error message for bad request.  # noqa: E501

        :param message: The message of this BadRequestResponse.  # noqa: E501
        :type message: str
        """

        self._message = message

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BadRequestResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BadRequestResponse):
            return True

        return self.to_dict() != other.to_dict()
