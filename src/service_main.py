from fastapi import FastAPI, Depends, HTTPException
from endpoints.service_endpoints import GET_ALL_RESOURCE_GROUPS
from common.utilities import AZURE_TOKEN_URL, RESPONSE_AUTHENTICATION_FAILED_MESSAGE, RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE, AZURE_RESOURCE_GROUPS_URL, RESPONSE_RESOURCEGROUP_FAILED_MESSAGE, AZURE_RESOURCE_BY_GROUP_NAME_URL, RESPONSE_RESOURCE_BY_GROUP_NAME_FAILED_MESSAGE, AZURE_RESOURCE_BY_ID, RESPONSE_RESOURCE_BY_ID_FAILED_MESSAGE, RESPONSE_DELETE_RESOURCE_BY_ID_FAILED_MESSAGE, AZURE_DELETE_RESOURCE_GROUP_URL, RESPONSE_RESOURCEGROUP_DELETE_FAILED_MESSAGE
import requests
import os
from dotenv import load_dotenv


app  = FastAPI()
load_dotenv()


async def get_token():
    client_id = os.getenv('SERVICE_PRINCIPAL_CLIENT_ID')
    client_secret = os.getenv('SERVICE_PRINCIPAL_CLIENT_SECRET')
    scope = os.getenv('AZURE_SCOPE_URL')

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    print(payload)
  
  
    # Check if the request was successful
    response = requests.post(AZURE_TOKEN_URL, data=payload)
    if response.status_code == 200:
        # Extract the access token from the response
        access_token = response.json().get('access_token')
        return access_token
    else:
        return None


@app.get('/api/resource_group_data')
def get_all_resource_group_data(access_token = Depends(get_token)):
    response_items = []
    if access_token is None:
        return HTTPException(status_code=RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE, detail=RESPONSE_AUTHENTICATION_FAILED_MESSAGE)
    else:
        headers = {
            'Authorization' : f'Bearer {access_token}'
        }
       
        response = requests.get(url=AZURE_RESOURCE_GROUPS_URL, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            for res in response_json['value']:
                print(res['name'])
                resource_group_name = res['name']
                url = AZURE_RESOURCE_BY_GROUP_NAME_URL.replace('resourceGroupName', resource_group_name)
                resource_group_response = requests.get(url=url, headers=headers)
                if resource_group_response.status_code == 200:
                    resource_group_items =  resource_group_response.json()['value']
                    res['items'] = resource_group_items
                    response_items.append(res)
                else:
                    return HTTPException(status_code=response.status_code, detail=RESPONSE_RESOURCE_BY_GROUP_NAME_FAILED_MESSAGE)
        else:
            return HTTPException(status_code=response.status_code, detail=RESPONSE_RESOURCEGROUP_FAILED_MESSAGE)
    
    return response_items



@app.get('/api/get_all_resource_groups')
def allresourcegroups(access_token = Depends(get_token)):
    if access_token is None:
        return HTTPException(status_code=RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE, detail=RESPONSE_AUTHENTICATION_FAILED_MESSAGE)
    else:
        headers = {
            'Authorization' : f'Bearer {access_token}'
        }
        print(AZURE_RESOURCE_GROUPS_URL)
        response = requests.get(url=AZURE_RESOURCE_GROUPS_URL, headers=headers)
        print(response)
        if response.status_code == 200:
            return response.json()
        else:
            return HTTPException(status_code=response.status_code, detail=RESPONSE_RESOURCEGROUP_FAILED_MESSAGE)
        

@app.get('/api/get_all_resource_by_groupname/{resource_group_name}')
def resourcebygroupname(resource_group_name:str, access_token = Depends(get_token)):
    if access_token is None:
        return HTTPException(status_code=RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE, detail=RESPONSE_AUTHENTICATION_FAILED_MESSAGE)
    else:
        headers = {
            'Authorization' : f'Bearer {access_token}'
        }
        url = AZURE_RESOURCE_BY_GROUP_NAME_URL.replace('resourceGroupName', resource_group_name)

        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return HTTPException(status_code=response.status_code, detail=RESPONSE_RESOURCE_BY_GROUP_NAME_FAILED_MESSAGE)


@app.get('/api/get_resource_by_id/{resource_id:path}')
def resourcebyid(resource_id: str, access_token = Depends(get_token)):
    if access_token is None:
        return HTTPException(status_code=RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE, detail=RESPONSE_AUTHENTICATION_FAILED_MESSAGE)
    else:
        headers = {
            'Authorization' : f'Bearer {access_token}'
        }
        url = AZURE_RESOURCE_BY_ID.replace('RESOURCEID', resource_id)
        print(url)

        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return HTTPException(status_code=response.status_code, detail=RESPONSE_RESOURCE_BY_ID_FAILED_MESSAGE)



@app.delete('/api/delete_resource_by_id/{resource_id:path}')
def deleteresourcebyid(resource_id: str, access_token = Depends(get_token)):
    if access_token is None:
        return HTTPException(status_code=RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE, detail=RESPONSE_AUTHENTICATION_FAILED_MESSAGE)
    else:
        headers = {
            'Authorization' : f'Bearer {access_token}'
        }
        url = AZURE_RESOURCE_BY_ID.replace('RESOURCEID', resource_id)
        print(url)
        response = requests.delete(url=url, headers=headers)
        # print(f'{response.json()}')
        if response.status_code == 200:
            return response.json()
        else:
            return HTTPException(status_code=response.status_code, detail=RESPONSE_DELETE_RESOURCE_BY_ID_FAILED_MESSAGE)
        

@app.delete('/api/delete_resourcegroup/{resource_group_name}')
def deleteresourcegroup(resource_group_name: str, access_token = Depends(get_token)):
    if access_token is None:
        return HTTPException(status_code=RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE, detail=RESPONSE_AUTHENTICATION_FAILED_MESSAGE)
    else:
        headers = {
            'Authorization' : f'Bearer {access_token}'
        }
        url = AZURE_DELETE_RESOURCE_GROUP_URL.replace('resourceGroupName', resource_group_name)
        print(url)
        response = requests.delete(url=url, headers=headers)
        # print(f'{response.json()}')
        if response.status_code == 200:
            return response.json()
        else:
            return HTTPException(status_code=response.status_code, detail=RESPONSE_RESOURCEGROUP_DELETE_FAILED_MESSAGE)