#!/bin/bash

echo "🔍 Verifying kubeconfig context..."
kubectl config current-context

echo "📦 Applying Kubernetes manifests in kube/ ..."
kubectl apply -f kube/deployment.yaml
kubectl apply -f kube/service.yaml
kubectl apply -f kube/hpa.yml
kubectl apply -f kube/network-policy.yaml

echo "⏳ Waiting for pods to become ready..."
kubectl rollout status deployment/dvwa

echo "📡 Fetching service details..."
kubectl get svc

echo "✅ DVWA has been deployed. Access it using the LoadBalancer EXTERNAL-IP."
