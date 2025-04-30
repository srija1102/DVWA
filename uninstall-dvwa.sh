#!/bin/bash

echo "⚠️  This will delete DVWA deployment, service, HPA, and network policy."
read -p "Are you sure? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "❌ Uninstallation aborted."
  exit 1
fi

echo "🧹 Deleting resources in kube/..."
kubectl delete -f kube/network-policy.yaml --ignore-not-found
kubectl delete -f kube/hpa.yml --ignore-not-found
kubectl delete -f kube/service.yaml --ignore-not-found
kubectl delete -f kube/deployment.yaml --ignore-not-found

echo "🔍 Verifying resources are removed..."
kubectl get all -l app=dvwa

echo "✅ Uninstallation complete."
