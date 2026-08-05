# Introduction
Technically, this isn't kubernetes, its k3s a lightweight version of kubernetes.
So I copy the config to the default route so I dont have compatibility issues:
`cp /etc/rancher/k3s/k3s.yaml ~/.kube/config`

# pod vs deployment
a pod is a unique instance of a service, like a container.
a deployment handles the replicas of this pod, if the pod falls, the deployment will try to raise it again, creating a new pod.

# delete services
``` bash
kubectl delete -f vault-infra.yaml
```
# start services
reapplies config if you changed the .yaml file
```bash
kubectl apply -f vault-infra.yaml
```
# status
``` bash
kubectl get pods -l app=vault
```
# logs
```bash
kubectl logs wallet-tracker-pod -c fetch-secrets
```
```bash
kubectl logs deployment/vault
```
``` bash
kubectl describe pod -l app=lanoiapintada | grep -A 10 Events:
```
# enter in bash
``` bash
kubectl exec -it deployment/mariadb -- /bin/sh
```
# restart deployment
this applies when you did not change the .yaml file
```bash
kubectl rollout restart deployment lanoiapintada-app
```
# force deployment of pods
``` bash
kubectl delete pods -l app=lanoiapintada
```