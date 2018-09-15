# isucon8-infra
## Requirements
- Python >= 2.7, < 3

## How to setup
```
$ pip install 'fabric<2' cuisine
```

## About config files
CentOS7.5のデフォルトの設定もコピーしてあるので、適当に `scp` して `/etc` 以下に全部上書きすればええんじゃね(適当)

### nginx
* `/etc/nginx/nginx.conf`
  - nginxのすべての設定
  - `conf.d` 以下の設定はすべて消して、上記に移した
  - よくある設定はある程度書いておいた

### php-fpm
* `/etc/php.ini`
  - php全般の設定
  - とりあえず `timezone` とか `memory_limit` とか設定済み
* `/etc/php-fpm.conf`
  - fpmのglobal設定
  - 軽く設定済み
* `/etc/php-fpm.d/www.conf`
  - fpmのpoolの設定
  - 実行権限とかプロセス数はここ
  - アプリケーションに合わせて設定必要

### Percona
* `/etc/percona-server.conf.d/percona-server.cnf`
  - Percona Server の主な設定
  - その他は無視してよいが、元からゴミが置いてあった場合は念の為新たなものを置き直した方がよい

## 付録
### memcached
```bash
$ sudo yum install memcached

# vendor preset: disabled なので
$ sudo systemctl enable memcached

# 設定はsystemd経由なので以下
$ cat /etc/sysconfig/memcached
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
```

過去に使ったらしきオプション
```bash
# socket生やす場合は権限が必要
#-u root -> USERで指定すれば良さそう

# socketを生やす場合のオプション
-s /run/memcached.sock
-a 666

# UDPを使わないなら切る
-U 0

# thread数, default=4
-t 4

# でかいキャッシュぶち込みたい場合はこれ, default=1m
-I 3m
```