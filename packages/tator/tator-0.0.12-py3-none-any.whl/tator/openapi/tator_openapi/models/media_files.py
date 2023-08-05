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


class MediaFiles(object):
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
        'archival': 'list[VideoDefinition]',
        'audio': 'list[AudioDefinition]',
        'streaming': 'list[VideoDefinition]'
    }

    attribute_map = {
        'archival': 'archival',
        'audio': 'audio',
        'streaming': 'streaming'
    }

    def __init__(self, archival=None, audio=None, streaming=None, local_vars_configuration=None):  # noqa: E501
        """MediaFiles - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._archival = None
        self._audio = None
        self._streaming = None
        self.discriminator = None

        if archival is not None:
            self.archival = archival
        if audio is not None:
            self.audio = audio
        if streaming is not None:
            self.streaming = streaming

    @property
    def archival(self):
        """Gets the archival of this MediaFiles.  # noqa: E501


        :return: The archival of this MediaFiles.  # noqa: E501
        :rtype: list[VideoDefinition]
        """
        return self._archival

    @archival.setter
    def archival(self, archival):
        """Sets the archival of this MediaFiles.


        :param archival: The archival of this MediaFiles.  # noqa: E501
        :type archival: list[VideoDefinition]
        """

        self._archival = archival

    @property
    def audio(self):
        """Gets the audio of this MediaFiles.  # noqa: E501


        :return: The audio of this MediaFiles.  # noqa: E501
        :rtype: list[AudioDefinition]
        """
        return self._audio

    @audio.setter
    def audio(self, audio):
        """Sets the audio of this MediaFiles.


        :param audio: The audio of this MediaFiles.  # noqa: E501
        :type audio: list[AudioDefinition]
        """

        self._audio = audio

    @property
    def streaming(self):
        """Gets the streaming of this MediaFiles.  # noqa: E501


        :return: The streaming of this MediaFiles.  # noqa: E501
        :rtype: list[VideoDefinition]
        """
        return self._streaming

    @streaming.setter
    def streaming(self, streaming):
        """Sets the streaming of this MediaFiles.


        :param streaming: The streaming of this MediaFiles.  # noqa: E501
        :type streaming: list[VideoDefinition]
        """

        self._streaming = streaming

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
        if not isinstance(other, MediaFiles):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MediaFiles):
            return True

        return self.to_dict() != other.to_dict()
