``` bash
curl -u "USERNAME:PASSWORD" \
  -X POST \
  -H "Content-Type: application/json" \
  http://localhost:5000/api/v2.0/projects/lanoiapintada/webhook/policies \
  -d '{
    "name": "trigger-k3s-rollout",
    "enabled": true,
    "targets": [{
      "type": "http",
      "address": "http://192.168.1.131:30090/webhook",
      "auth_header": "Bearer SECRET",
      "skip_cert_verify": true
    }],
    "event_types": ["PUSH_ARTIFACT"]
  }'
```