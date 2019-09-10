docker build -t lallinger/process . --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$http_proxy
docker push lallinger/process
oc project process
oc delete -f service.yaml
oc create -f service.yaml