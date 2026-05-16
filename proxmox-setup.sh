#!/bin/bash
# ==============================================================
# Cobblemon DeepAgent — Proxmox LXC Setup
# Ejecutar en el HOST de Proxmox (no en el container)
# ==============================================================
# Esto crea un LXC container (NO una VM) con Docker listo.

set -e

CONTAINER_ID=200
CONTAINER_NAME="cobblemon-agent"
MEMORY_MB=2048
DISK_GB=20
STORAGE="local-lvm"       # Cambiar si usas otro storage
TEMPLATE="ubuntu-24.04"   # O debian-12

echo "=== Creando LXC container para Cobblemon DeepAgent ==="

# 1. Bajar template si no existe
pveam update 2>/dev/null || true

# 2. Crear el LXC container (privilegiado=no, nesting=yes para Docker)
pct create $CONTAINER_ID \
    $TEMPLATE \
    --hostname $CONTAINER_NAME \
    --memory $MEMORY_MB \
    --swap 1024 \
    --rootfs ${STORAGE}:${DISK_GB} \
    --cores 2 \
    --net0 name=eth0,bridge=vmbr0,ip=dhcp \
    --unprivileged 1 \
    --features nesting=1 \
    --start 1

echo "Esperando a que el container inicie..."
sleep 10

# 3. Instalar Docker dentro del LXC
pct exec $CONTAINER_ID -- bash -c '
set -e
apt-get update -y
apt-get install -y curl git

# Docker
curl -fsSL https://get.docker.com | sh

# docker-compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "=== Docker instalado en LXC ==="
docker --version
docker-compose --version
'

echo ""
echo "=== LXC container listo ==="
echo "IP del container:"
pct exec $CONTAINER_ID -- ip -4 addr show eth0 | grep inet | awk '{print $2}'
echo ""
echo "Para entrar: pct enter $CONTAINER_ID"
echo "Para copiar el proyecto:"
echo "  rsync -av --exclude frontend/node_modules --exclude backend/.venv \\"
echo "    /ruta/local/AgentePokemon/ root@<IP>:/opt/cobblemon-agent/"
echo ""
echo "Luego dentro del LXC:"
echo "  cd /opt/cobblemon-agent"
echo "  nano backend/.env   # Poner tus API keys"
echo "  docker-compose up -d"
