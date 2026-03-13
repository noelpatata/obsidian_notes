
``` bash
if [ -z "$1" ]; then
  echo "Usage: $0 <MARIADB_VM_ID>"
  exit 1
fi

MARIADB_VM_ID="$1"
JENKINS_VM_ID="100"

rm -r /mnt/mariadb_wallettracker
pct shutdown "$MARIADB_VM_ID" && pct destroy "$MARIADB_VM_ID"
pct exec "$JENKINS_VM_ID" -- rm -r /var/lib/jenkins/workspace/wallettracker_cd/terraform/

echo "✅ MariaDB VM $MARIADB_VM_ID reset and Terraform state cleared."

```