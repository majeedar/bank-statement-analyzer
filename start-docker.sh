#!/bin/bash
docker compose -f docker-compose.dev.yml up -d
sleep 3
docker compose -f docker-compose.dev.yml ps
