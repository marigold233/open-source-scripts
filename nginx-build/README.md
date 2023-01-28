
为了兼容centos6系统使用nginx，在centos6系统中进行编译，所以centos6以上的系统都能够使用。

## 使用
```bash
docker build -t nginx-demo:v1 .
docker run --rm --env STDOUT=1 nginx-demo:v1 1.22.1 /data/nginx-bin-1.22.1 > nginx-bin-1.22.1.tar.gz
```

## DEBUG
```bash
docker run --rm --env STDOUT=1 --env TRACE=true nginx-demo:v1 1.22.1 /data/nginx-bin-1.22.1 > nginx-bin-1.22.1.tar.gz
```
