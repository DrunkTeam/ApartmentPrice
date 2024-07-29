For running
```bash
cd ApartmentPrice/api
```

```bash
docker run --rm -p 5152:8080 my_ml_service
```

If you have error like this:
docker: Error response from daemon: driver failed programming external connectivity on endpoint hungry_spence (b7475c6cd0e0a5ffc5a1ababab7347113688d4b9aefa97f15412aa8769163f27): Bind for 0.0.0.0:5152 failed: port is already allocated.

You need to do:

```bash
sudo lsof -i :5152
```

```bash
sudo kill -9 <PID>
```

```bash
docker ps
```

```bash
docker stop <CONTAINER_ID>
```

If it doesn't help, you need run docker on another port.
```bash
docker run --rm -p 5153:8080 my_ml_service
```
