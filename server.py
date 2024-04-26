from kubernetes import client, config
from kubernetes.client.rest import ApiException
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
app = Flask(__name__)
# app.run(debug = True)

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    # your code here
    try:
        config.load_kube_config()
        batch_v1 = client.BatchV1Api()        
        api_response = batch_v1.list_pod_for_all_namespaces(watch=False)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)

    pods = [{"name": pod.metadata.name, "ip": pod.status.pod_ip, "namespace": pod.metadata.namespace, "node":pod.spec.node_name, "status": pod.status.phase } for pod in api_response.items]
    output = {"pods": pods}
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here

    yaml_obj= open("free-job.yaml")  # path to the correct .yaml  file
    job = yaml.safe_load(yaml_obj)
    
    api_response = kubernetes.client.BatchV1Api().create_namespaced_job(
            namespace="free-service",
            body=job)

    return "success"


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    yaml_obj= open("prem-job.yaml")  # path to the correct .yaml  file
    job = yaml.safe_load(yaml_obj)
    
    api_response = kubernetes.client.BatchV1Api().create_namespaced_job(
            namespace="default",
            body=job)
    
    return "success"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
