# PyFlink with Flink Kubernetes Operator
This directory contains resources and configurations for deploying PyFlink applications on Kubernetes using the Flink Kubernetes Operator. The setup allows for scalable and managed execution of PyFlink jobs within a Kubernetes environment.

## Overview
Deploying PyFlink applications on Kubernetes involves several steps, including setting up the Flink Kubernetes Operator, creating a FlinkDeployment resource, and configuring your PyFlink job to run within the Kubernetes cluster. This guide will walk you through these steps to get your PyFlink application running on Kubernetes.

## Prerequisites
- Docker
- Minikube
- helm

Ensure Docker Desktop for Windows/Mac is installed for seamless integration with Minikube.


## Steps
1. **Set Docker Context (Windows Users Only)**
   Open your terminal and execute:
   ```
   Docker context use default
   ```
2. **Start Minikube**
   ```
   minikube start
   ```
   Note: Starting Minikube may take a few minutes.

3. **Deploy the certificate manager**
   ```bash
   kubectl create -f https://github.com/jetstack/cert-manager/releases/download/v1.8.2/cert-manager.yaml
   ```
   Cert-manager automates the management and issuance of TLS certificates within Kubernetes.
   
4. Deploy Flink Kubernetes Operator
   ```
   helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.8.0/
   helm install flink-kubernetes-operator flink-operator-repo/flink-kubernetes-operator
   ```
   Verify the installation:
   ```
   kubectl get pods
   ```
5. Clone the Repository
   ```
   git clone https://github.com/databugs/data-streaming-with-pyflink.git
   ````
6. Navigate to Directory
   ```
   cd pyflink-with-flink-kubernetes-operator
   ```

7. Create configMap
   Fill in the necessary values in `app_config.yaml`. Then, apply them:
   ```
   kubectl apply -f app_config.yaml
   kubectl apply -f py_config.yaml
   ```
   Check the creation:
   ```
   kubectl get configMap
   ```
8. Deploy the Flink app to start data streaming
   ```
   kubectl apply -f deployment.yaml
   ```
   Monitor the deployment status:
   ```
   bash kubectl rollout status deployment/sales-dev
   ```

## Bonus
Install [K9s](https://k9scli.io/topics/install/) is a terminal-based interface to interact with your Kubernetes clusters. Install it to easily view and manage your clusters:
```
k9s -c pods
```

## Monitoring and Troubleshooting

After deployment, monitor your PyFlink application by accessing logs and metrics. Common issues and troubleshooting tips will be added here.
   
