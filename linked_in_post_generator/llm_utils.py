""" 
    Module: llm_utils.py
    
    Author: Nashith vp
    
    Description:
    
    Created On: 15-02-2026
"""
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")


if __name__ == "__main__":
    response = llm.invoke("how to create sambar")
    print(response.content)
