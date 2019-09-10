import os, json, uuid, sys

import flask
from azure.storage.blob import BlockBlobService, PublicAccess

app = flask.Flask(__name__)

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

    blobname = data["data"]["url"].split("/")[-1]
    content = block_blob_service.get_blob_to_text(container_landing, blobname).content
    

    block_blob_service.create_blob_from_text(container_staging,blobname,preprocessing(content))
    block_blob_service.delete_blob(container_landing,blobname,delete_snapshots='include')


@app.route('/', methods=['PUT','POST'])
def receive():
    process(flask.request.get_json())
    return flask.Response(status=202)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(8080))

