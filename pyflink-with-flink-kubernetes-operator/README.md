# PyFlink with Flink Kubernetes Operator
This directory contains resources and configurations for deploying PyFlink applications on Kubernetes using the Flink Kubernetes Operator. The setup allows for scalable and managed execution of PyFlink jobs within a Kubernetes environment.

## Overview
Deploying PyFlink applications on Kubernetes involves several steps, including setting up the Flink Kubernetes Operator, creating a FlinkDeployment resource, and configuring your PyFlink job to run within the Kubernetes cluster. This guide will walk you through these steps to get your PyFlink application running on Kubernetes.

## Prerequisites
- Docker
- Minikube
- helm

Start up docker and follow the next steps.

## Steps
1. For Windows users, you need to run this before starting minikube
   ```bash
   Docker context use default
   ```
2. Start Minikube
   ```
   minikube start
   ```
3. Deploy the certificate manager
   ```bash
   kubectl create -f https://github.com/jetstack/cert-manager/releases/download/v1.8.2/cert-manager.yaml
   ```
4. Deploy Flink Kubernetes Operator
   ```
   helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.8.0/
   helm install flink-kubernetes-operator flink-operator-repo/flink-kubernetes-operator
   ```
   You may verify your installation by running
   ```
   kubectl get pods
   ```
6. Create configMap
   
