# Autoscaling system with Kubernetes, Azure function and KEDA
## Overview
The project aim to creat and deploy a hybrid autoscaling system that dynamically adjusts application resources based on workload demand.
It intergrates the advantages of: Kubernetes, Azure function, KEDA for scaling and Prometheus for metrics monitoring.

The system is deployed in a Python 3.9 virtual environment
# On Azure site,it is needed to creat a "Kubernetes cluster","Storage account", "Function App", "Container registry" and a "Resource group"

# Setup guide

## Installation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install needed library.

```bash
pip install requirements.txt
```

### Prerequisites

#### Azure Account

Lock in to Azure:
```bash
az login 
```
Set the active subscription 
```bash
az account set --subscription <subsription id>
```
#### Azure function Core Tools 

Azure function core tools enable user to deploy Azure function locally on the computer.
To install Azure function, run the following command:

```bash 
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

Once installed, run the following command to check the version of Azure Function Core Tools
```bash
func --version
```

Deploy the function to Azure
```bash
func azure functionapp publish <function-app-name>
```

#### Docker

Build and Push to ACR
Dockerfile and worker.py are visible in the project 
```bash
docker build -t container-registry.azurecr.io/queue-worker:latest
docker push container-registry.azurecr.io/queue-worker:latest 
``` 

#### Helm

Helm is a standard tool for finding, sharing and managing the installation, upgrading and deleting process of applications on Kubernetes.
[Helm](https://helm.sh/docs/intro/install/)

#### KEDA

Kubernetes Event-driven Autoscaling (KEDA) is a single-purpose and lightweight component that strives to make application autoscaling simple and is a Cloud Native Computing Federation (CNCF) Graduate project.

To install [KEDA] in Kubernetes cluster, run the following command: 
```bash
kubectl create namespace keda
kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.9.0/keda-2.9.0.yaml
```
*note: make sure to download the latest release on [github](https://github.com/kedacore/keda) 

#### kubectl

kubectl is connected to AKS cluster after: 
```bash
az aks get-credentials --resource-group <resource-group-name> --name <aks-cluster-name> 
```

#### Prometheus

For monitoring metrics, creat a keda-monitoring.yaml file and download Prometheus by running following command:
```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```
The command also installs: Alertmanager, Node exporters, Custom Resource Definitions(CRDs), Grafana

To confirm the installation, run: 
```bash
kubectl get pods -n monitoring
kubectl get pods -n keda
```

For local testing, run following command for port forwarding Prometheus:
```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090
```
Access at: [Prometheus](http://localhost:9090)

#### React 

A simple UI is created for this project to simplyfy the scenario when a huge of customer purchase item in the store replicates the burst load of messages sent to the Azure queue(clicking "buy" button multiple times), to access the UI, run the following command to start the frontend:
```bash
npm run dev
```

## Creat Kubernestes Secrets for the Azure Storage connection string

Store storage account key out side of the application's code and configuration files.
```bash
kubectl create secret generic azure-storage-secret \
  --from-literal=connectionString="DefaultEndpointsProtocol=https;AccountName=storageaccount;AccountKey=<KEY>;EndpointSuffix=core.windows.net"
```

## Verify the deployment

To apply the worker, deployment run:
```bash
kubectl -f apply <rule.yaml>
```
for example: kubectl -f apply worker-deployment.yaml

Run:
```bash
kubectl get pods
kubectl get hpa
```

## Testing
After finish all the creation of files, install neccessary tools and library, let's get started!!

Start the function
```bash
func start 
```

To view the scaling process in real time run:
```bash
kubectl get hpa -w 
kubectl get pods -w 
```

### Queue triggering

#### Method 1
Go to UI and continously click "Buy" button 

#### Method 2 
run:
```bash
for /l %i in (1,1,1000) do start "" /b curl -s -X POST http://localhost:7071/api/send -H "Content-Type: application/json" -d "{\"message\":\"test %i\"}"
```

### Monitoring
For collecting and monitoring mterics, run: 
```bash 
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring
```
Use for example: "keda_scaler_metrics_value" 
# That's all, good luck with your journey. Hope you enjoy KEDA!
Inspiration from [KEDA](https://github.com/kedacore/keda)