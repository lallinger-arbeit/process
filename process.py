import os, json, uuid, sys

from flask import Flask
from flask import request
from azure.storage.blob import BlockBlobService, PublicAccess

app = Flask(__name__)

def fibo(count):
    if count==1 or count==2:
        return 1

    return fibo(count-1)+fibo(count-2)

def preprocessing(data):
    pieces = data.split(",")
    pieces[1] = str(fibo(int(pieces[1])))
    return ','.join(pieces)


def process(data):
    user=os.environ['STORAGE_USERNAME']
    password=os.environ['STORAGE_PASSWORD']
    container_landing ='landingzone'
    container_staging = 'staging'
    block_blob_service = BlockBlobService(account_name=user, account_key=password)

    local_path = os.path.expanduser("~/tmp")
    local_file_name = data["data"]["url"].split("/")[-1]
    full_path_to_file = os.path.join(local_path, local_file_name)

    block_blob_service.get_blob_to_path(container_landing, local_file_name, full_path_to_file)

    f = open(full_path_to_file,"r")
    content = f.read()
    f.close()

    f = open(full_path_to_file,"w")
    f.write(preprocessing(content))
    f.close()

    block_blob_service.create_blob_from_path(container_staging, local_file_name, full_path_to_file)
    os.remove(full_path_to_file)
    block_blob_service.delete_blob(container_landing,local_file_name,delete_snapshots='include')


@app.route('/', methods=['PUT','POST'])
def receive():
    process(request.get_json())
    return 'OK\n'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(8080))

