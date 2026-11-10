#!/bin/bash
set -e

if [ ! -f /home/hadoop/.ssh/id_rsa ]; then
  su - hadoop -c "ssh-keygen -t rsa -N '' -f /home/hadoop/.ssh/id_rsa"
  cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys
  chmod 600 /home/hadoop/.ssh/authorized_keys
fi

# Inicia SSH en foreground (CMD lo relanza como -D)
exec "$@"