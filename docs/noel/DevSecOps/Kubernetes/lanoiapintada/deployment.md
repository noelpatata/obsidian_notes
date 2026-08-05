## Step 1: Create Cloudflare Tunnel & Obtain Token

Before installing `cloudflared` inside Kubernetes, you must generate a tunnel token in Cloudflare Zero Trust.

1. Log in to the [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com).
    
2. Go to **Networks** $\rightarrow$ **Tunnels**.
    
3. Click **Add a tunnel** $\rightarrow$ Choose **Cloudflared** $\rightarrow$ Click **Next**.
    
4. Enter a Tunnel Name (e.g., `k3s-prod-tunnel`) and click **Save tunnel**.
    
5. Under **Install and run a connector**, look at the run command box.
    
6. Copy the long base64 string after `--token` (e.g., `eyJhIjoi...`). This is your **`TUNNEL_TOKEN`**.
    

## Step 2: Install Cloudflare Tunnel Agent via Helm

Install the official `cloudflare-tunnel` Helm chart inside the `kube-system` namespace.

### 2.1 Add Helm Repository

Bash

```
helm repo add cloudflare https://cloudflare.github.io/helm-charts
helm repo update
```

### 2.2 Install Chart using Secret Token

Run the installation command, passing your copied token:

Bash

```
helm install cloudflared cloudflare/cloudflare-tunnel \
  --namespace kube-system \
  --set cloudflare.tunnel_token='YOUR_CLOUDFLARE_TUNNEL_TOKEN'
```

### 2.3 Verify Connector Deployment

Check that the connector pod is active:

Bash

```
kubectl get pods -n kube-system -l app.kubernetes.io/name=cloudflare-tunnel
```

## Step 3: Configure Harbor Robot Account Permissions

To pull images securely without administrator credentials, create a dedicated Robot Account in Harbor.

### 3.1 Create Robot Account in Harbor

1. Log in to Harbor Dashboard (`[https://registry.downops.win](https://registry.downops.win)`).
    
2. Go to **Projects** $\rightarrow$ **`lanoiapintada`** $\rightarrow$ **Robot Accounts**.
    
3. Click **+ New Robot Account**:
    
    - **Name**: `lanoiapintada-pull`
        
    - **Expiration**: Set policy (e.g., Never or 365 Days).
        
4. Assign permissions for project `lanoiapintada`:
    
    - **Repository**: `Pull` / `Read` / `List`
        
    - **Artifact**: `Read` / `List`
        
5. Save and copy the generated **Secret Token** (`Yi9K2dNPTNg46C5EB0JhjOtiSzhDogIb`).
    

> **Note**: Harbor generates usernames in the format `robot$PROJECT_NAME-ROBOT_NAME` (e.g., `robot$lanoiapintada-pull`).

## Step 4: Create Kubernetes Registry Secret (`imagePullSecret`)

### 4.1 Understanding Bash Escaping

Harbor usernames contain `$`. In Bash shells, double quotes evaluate `$lanoiapintada` as an unset variable, altering the string. Always wrap the username in **single quotes (`'...'`)**.

### 4.2 Create Secret

Bash

```
kubectl create secret docker-registry harbor-secret \
  --docker-server=registry.downops.win \
  --docker-username='robot$lanoiapintada-pull' \
  --docker-password='Yi9K2dNPTNg46C5EB0JhjOtiSzhDogIb' \
  --namespace=default \
  --dry-run=client -o yaml | kubectl apply -f -
```

## Step 5: Apply Deployment and Service Manifests

Create `deployment.yaml` with the `Deployment` and `Service` resources. No `kind: Ingress` block is needed.

### 5.1 Save `deployment.yaml`

YAML

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lanoiapintada-app
  namespace: default
  labels:
    app: lanoiapintada
spec:
  replicas: 2
  selector:
    matchLabels:
      app: lanoiapintada
  template:
    metadata:
      labels:
        app: lanoiapintada
    spec:
      imagePullSecrets:
        - name: harbor-secret
      containers:
        - name: app
          image: registry.downops.win/lanoiapintada/web:v1.0.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: lanoiapintada-service
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: lanoiapintada
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
```

### 5.2 Apply Manifests

Bash

```
kubectl apply -f deployment.yaml
```

## Step 6: Kubernetes Internal DNS Resolution

Kubernetes CoreDNS automatically maps internal addresses.

### 6.1 FQDN Structure

The service address generated inside the cluster is:

`[http://lanoiapintada-service.default.svc.cluster.local:80](http://lanoiapintada-service.default.svc.cluster.local:80)`

|**Segment**|**Origin / Context**|
|---|---|
|`lanoiapintada-service`|`metadata.name` in Service manifest|
|`default`|`metadata.namespace` in Service manifest|
|`svc`|Standard Kubernetes Service domain identifier|
|`cluster.local`|Top-level cluster domain suffix|
|`:80`|`spec.ports.port` in Service manifest|

### 6.2 Cross-Namespace Routing

Because `cloudflared` runs in `kube-system` and the application runs in `default`, you must use the complete FQDN to bridge namespaces.

## Step 7: Configure Cloudflare Tunnel Routing

Map your public domain to the internal Kubernetes FQDN.

1. Open **Cloudflare Zero Trust** $\rightarrow$ **Networks** $\rightarrow$ **Tunnels**.
    
2. Select your tunnel $\rightarrow$ Click **Edit**.
    
3. Go to **Public Hostnames** $\rightarrow$ **Add a public hostname**.
    
4. Configure fields:
    
    - **Subdomain**: _(Leave blank for root domain `lanoiapintada.com`, or enter `www`)_
        
    - **Domain**: `lanoiapintada.com`
        
    - **Type**: `HTTP`
        
    - **URL**: `lanoiapintada-service.default.svc.cluster.local:80`
        
5. Click **Save Hostname**.
    

## Step 8: Verification

1. **Verify Pod Status**:
    
    Bash
    
    ```
    kubectl get pods -l app=lanoiapintada
    ```
    
    _Status should read `1/1 Running`._
    
2. **Test End-to-End Traffic**:
    
    Bash
    
    ```
    curl -I https://lanoiapintada.com
    ```
    
    _Expected HTTP response: `200 OK`._