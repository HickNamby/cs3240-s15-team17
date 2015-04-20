__author__ = 'Nick'
from easygui import *
import os, random, struct, uuid
from Crypto.Cipher import AES
import hashlib
from FileEncrypter import encrypt_file
from FileEncrypter import decrypt_file
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
import requests

msg1="Would You Like to Encrypt or Decrypt a File?"
choices1=["Encrypt", "Decrypt", "Connect"]
EDchoice=buttonbox(msg=msg1, title="EZ-Encrypt",choices=choices1, image="sp.gif")

if EDchoice=="Encrypt":
    # print("herp")
    # msgbox(msg="Choose a file to encrypt", title="Encryption in progress")
    fte=fileopenbox(msg="Choose File to be Encrypted", title="Encryption in Progress")
    # print(fte)

    msg = "Please Enter the Following:"
    title = "File Encryption in Progress"
    fieldNames = ["Secret Key","Output File Name"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.' %fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

    SecretKey=hashlib.sha256(fieldValues[0].encode('utf-8')).digest()
    OutputFNAME=fieldValues[1]

    encrypt_file(SecretKey, fte, OutputFNAME)
    msgbox(msg="Operation Successful", title="File Encryption Complete")
elif EDchoice=="Decrypt":
    fte=fileopenbox(msg="Choose File to be Decrypted", title="Decryption in Progress")
    # print(fte)

    msg = "Please Enter the Following:"
    title = "File Decryption in Progress"
    fieldNames = ["Secret Key","Output File Name"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.' %fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

    SecretKey=hashlib.sha256(fieldValues[0].encode('utf-8')).digest()
    OutputFNAME=fieldValues[1]

    decrypt_file(SecretKey, fte, OutputFNAME)
    
    msgbox(msg="Operation Successful", title="File Decryption Complete")
    
elif EDchoice=="Connect":
    url_login='http://127.0.0.1:8000/login/'
    msg = "Please Enter Your Credentials"
    title= "Log in and Connect"
    fieldNames = ["Username", "Password"]
    #loginValues = multenterbox(msg,title, fieldNames)
    loginValues = ['hamby', 'password']
    url_list='http://127.0.0.1:8000/profile'
    with requests.session() as client:
        client.get(url_login, verify=False)
        csrftoken=client.cookies['csrftoken']
        payload = {'username': loginValues[0], 'password':loginValues[1],'csrfmiddlewaretoken':csrftoken}
        r0 = client.post(url_login, data=payload, verify=False)
        r1 = client.get(url_list, verify=False)
        c=r1.text
        print(c)