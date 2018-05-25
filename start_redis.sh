docker stop some-redis || true
docker rm some-redis || true
docker run --name some-redis -p 6379:6379 -d redis
