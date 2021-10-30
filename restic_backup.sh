#!/bin/bash

set -e

#(see docs for necessary restic env vars)
#(Currently using RESTIC_REPOSITORY , RESTIC_PASSWORD and HEALTHCHECKS_URL)
source .env

#Ignore pihole containers because my home network shouldn't crash because backups crashed
pihole_containerid=$(docker ps -aqf "name=pihole")
dhcphelper_containerid=$(docker ps -aqf "name=dhcphelper")

diun_containerid=$(docker ps -aqf "name=diun")

#Manually backup Pi-hole to /opt/restic/pihole-backups
docker exec pihole /bin/bash -c 'cd /etc/pihole/backups && pihole -a -t '

#Stop all docker containers
docker stop $(docker ps -q | rg -v $pihole_containerid | rg -v $dhcphelper_containerid | rg -v $diun_containerid)

# for the first run uncomment
#restic init

# --quiet - should speed up backup process see: https://github.com/restic/restic/pull/1676
# read --quiet flag
restic backup \
  --exclude-caches \
  --exclude "/opt/library" \
  --exclude "/opt/amd" \
  --exclude "/opt/jellyfin/config/cache" \
  --exclude "/opt/jellyfin/config/data/metadata" \
  --exclude "/opt/radarr/config/MediaCover" \
  --exclude "/opt/sonarr/config/MediaCover" \
  --exclude "/opt/pihole" \
  --exclude "**logs.*" \
  --tag files \
  /opt/

#mysqldump --single-transaction --all-databases | restic backup \
#  --quiet \
#  --stdin \
#  --stdin-filename dump.sql \
#  --tag mysql

# remove outdated snapshots
# --keep-last 20 - there won't be probably more hourly snapshots in last two days than 20
# --prune - delete repositories which should be forgotten
#restic forget --keep-last 20 \
#  --keep-daily 7 \
#  --keep-weekly 4 \
#  --keep-monthly 6 \
#  --keep-yearly 3 \
#  --limit-upload 500 \
#  --prune

restic check --with-cache

#Start all docker containers
docker start $(docker ps -a -q)

curl -m 10 --retry 5 $HEALTHCHECKS_URL
