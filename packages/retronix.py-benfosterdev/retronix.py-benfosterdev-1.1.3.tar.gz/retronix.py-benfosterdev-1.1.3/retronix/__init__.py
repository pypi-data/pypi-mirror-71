#!/usr/bin/env python

# Retronix Public API Python Library
# Developed by Ben Foster - All Rights Reserved.
"""__init__.py > Library Entrypoint"""

# Copyright and Metadata Smeg
__author__ = "Ben Foster"
__copyright__ = "Copyright 2020, Retronix"
__license__ = "MIT"
__version__ = "1.1.3"
__maintainer__ = "Ben Foster"
__email__ = "ben@retronixmc.org"
__status__ = "Development"

# Imports would go here
#import asyncio


class Client:
    """
    Retronix API Client

    Attributes:
        censor (list): Censored words list
        tld (list): List of censored Top Level Domains
    """

    def __init__(self, subs:dict=None):
        """
        Initialise a new instance of the Retronix Client.

        Store this as a variable for use as this is what you'll need to interact with the API.

        Parameters:
            subs (dict): (Optional) Dictionary of subscriptions to initialise
        """
        print("Hello World")
    def get(self, op):
        """
        Query API for up-to-date contents of specified list

        Will also update the variables in the process

        Parameters:
            op (Type): (Required) Type of list to query from API

        Returns:
            list: Raw return content from API
        
        Raises:
            RateLimitError: This happens when the API returns an error stating that the token used is currently in cooldown.
            ClientNotStartedError: Thrown when the client class hasn't been started.
        """
        return []
    def getState(self):
        """
        Checks to see if the client is online or not.
        """
    def login(self, token):
        """
        Start the client and log into the API.

        Parameters:
            token (str): (Required) Token to use when signing onto the API.

        Raises:
            TokenIncorrectError: This will be thrown if the API responds that the token provided is incorrect.
            TokenBarredError: This will be thrown if the API responds that the token provided has been blocked.
        """
        self.__token = token