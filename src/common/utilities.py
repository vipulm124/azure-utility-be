import os

TENANT_ID = os.getenv('TENANT_ID')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')



AZURE_TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
AZURE_RESOURCE_GROUPS_URL = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourcegroups?api-version=2021-04-01"
AZURE_RESOURCE_BY_GROUP_NAME_URL=f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/resourceGroupName/resources?api-version=2021-04-01"
AZURE_RESOURCE_BY_ID = f"https://management.azure.com/RESOURCEID?api-version=2024-04-01"
AZURE_DELETE_RESOURCE_GROUP_URL = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourcegroups/resourceGroupName?api-version=2021-04-01"


RESPONSE_AUTHENTICATION_FAILED_MESSAGE = "Unable to authenticate, please try again later."
RESPONSE_AUTHENTICATION_FAILED_STATUS_CODE = 400
RESPONSE_RESOURCEGROUP_FAILED_MESSAGE = "Unable to fetch resource groups information."
RESPONSE_RESOURCEGROUP_DELETE_FAILED_MESSAGE = "Unable to delete resource group."
RESPONSE_RESOURCE_BY_GROUP_NAME_FAILED_MESSAGE = "Unable to fetch resources by resource group name."
RESPONSE_RESOURCE_BY_ID_FAILED_MESSAGE = "Unable to fetch resource by resource Id."
RESPONSE_DELETE_RESOURCE_BY_ID_FAILED_MESSAGE = "Unable to delete resource by resource Id."

