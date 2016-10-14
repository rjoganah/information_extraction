'''
Created on 5 oct. 2016

@author: jogr0001
'''
import argparse
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
import pickle
import unidecode
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/sqlservice.admin']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'namedentities-8d456256977d.json', scopes)

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

def main(text):
  '''Run a NER request on text '''

    http = httplib2.Http()
    
    http=httplib2.Http()
    
     
    service = discovery.build('language', 'v1beta1',
                              http=http, discoveryServiceUrl=DISCOVERY_URL,developerKey='AIzaSyA2bqWVSY9Xl5RUjR3QCuPArcm-2SbmMfU')
    
      
    service_request = service.documents().analyzeEntities(
    body={
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        }
    })
    
    response = service_request.execute()
    entities = response['entities']
      
    return entities

if __name__ == '__main__':
    pdf = pickle.load(open('../garnissage_pdfs_en.pkl','rb'))
    entities = []
    for file in pdf:
        entities.append(main(unidecode.unidecode(file)))
    pickle.dump(entities,open('ner_google.txt','wb'))