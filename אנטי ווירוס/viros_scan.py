import os
import requests
import time

virus_total_api_key = 'ba755753ba4108e336a0175aa830ac659557da177e69d29a640a66fb3b874a55'
def itratza_files(folder_path):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path,filename)
        if os.path.isdir(full_path):
            itratza_files(full_path)
        else:
            scan_file(full_path)
        
def scan_file(file_path):
    reasponse = upload_file(file_path)
    scan_id = reasponse.get('scan_id')
    if scan_id:
        is_virus = get_report(scan_id=scan_id)
        if is_virus:
            print('VIRUS DETECTED!! file path: ', file_path)
        else:
            print('{} is not virus'.format(file_path))
    else:
        print('unexpected response, no scan id found for file: ', file_path)

def upload_file(file_path):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'

    params = {'apikey': virus_total_api_key}

    file_content = open(file_path , 'rb')
    file_name = os.path.basename(file_path)
    files = {'file': (file_name, file_content)}

    response = requests.post(url, files=files, params=params)

    return response.json()

def get_report(scan_id):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'

    params = {'apikey':'ba755753ba4108e336a0175aa830ac659557da177e69d29a640a66fb3b874a55' , 'resource': scan_id}
    time.sleep(0)
    response = requests.get(url, params=params)
    if not response:
        raise Exception('unexcepted error in response')
    if response.status_code == 200:    
        response = response.json()
        if response.get('response_code') != 1:
            print('Scan not complited...')
            time.sleep(15)
            get_report(scan_id)
        else:
            return response.get('positives') > 0
    elif response.status_code == 204:
        print('Empty response...')
        time.sleep(15)
        get_report(scan_id)
    else:
        print("recived unexcepted response with status code: " , response.status_code)
        return False



if __name__ == "__main__":
    itratza_files("C:\\Users\\dvirc\\VSCode\\dvir_python")
