""" 
    Module: exception_message.py
    
    Author: Nashith vp
    
    Description:
    
    Created On: 21-02-2026
"""
from enum import Enum


class ExceptionMessage(str, Enum):
    INTERNET_CONNECTION_ERROR = "Please check your internet connection and try again"
    UNKNOWN = "Unknown error"
