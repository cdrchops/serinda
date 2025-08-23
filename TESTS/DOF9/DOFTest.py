import requests


API_ENDPOINT = "http://192.168.0.11:8000/dofdata?dofdata=sent"

#data = {'api_dev_key':API_KEY, 
#        'api_option':'paste', 
#        'api_paste_code':source_code, 
#        'api_paste_format':'python'} 

data = {}
        
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
#pastebin_url = r.text 
#print("The pastebin URL is:%s"%pastebin_url) 
