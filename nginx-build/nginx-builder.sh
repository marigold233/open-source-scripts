#!/usr/bin/env bash
set -eo pipefail; [[ "$TRACE" ]] && set -x

DEFAULT_NGINX_VERSION="1.22.0"
DEFAULT_NGINX_PREFIX="/usr/local/nginx-bin-${DEFAULT_NGINX_VERSION}"
DEFAULT_OPENSSL_VERSION="1.1.1p"
DEFAULT_PCRE_VERSION="8.01"


zlib_download() {
    wget -qO- -t1 -T2 "https://api.github.com/repos/madler/zlib/releases/latest" | 
        grep download_url | 
        sed -rn "s/\"browser_download_url\": \"(.*)\"/\1/p" |
        head -1 | xargs -n 1 -i wget --no-check-certificate -qO-  https://ghproxy.com/{} |  tar zxf -
    ZLIB_VERSION=`wget -qO- -t1 -T2 "https://api.github.com/repos/madler/zlib/releases/latest"  | 
        grep tag_name | 
        sed -rn "s/\"tag_name\": \"(.*)\",/\1/p" | tr -d v," "`
}

mian() {
    nginx_version="${1:-$DEFAULT_NGINX_VERSION}"
    nginx_prefix="${2:-$DEFAULT_NGINX_PREFIX}"
    # : "${nginx_version:?}" "${nginx_prefix:?}"
    {
        wget --no-check-certificate -qO- "https://nginx.org/download/nginx-${nginx_version}.tar.gz" |
            tar zxf -
        wget --no-check-certificate -qO- "https://www.openssl.org/source/old/1.1.1/openssl-${DEFAULT_OPENSSL_VERSION}.tar.gz" |
            tar zxf -
        wget --no-check-certificate -qO- "https://nchc.dl.sourceforge.net/project/pcre/pcre/${DEFAULT_PCRE_VERSION}/pcre-${DEFAULT_PCRE_VERSION}.tar.gz" |
            tar zxf -
        # wget --no-check-certificate -qO- "http://www.zlib.net/zlib-${DEFAULT_ZLIB_VERSION}.tar.gz" |
        #     tar zxf -
        zlib_download
        cd nginx-${nginx_version}
        ./configure \
            --prefix=${nginx_prefix} \
            --with-pcre=../pcre-${DEFAULT_PCRE_VERSION} \
            --with-zlib=../zlib-${ZLIB_VERSION} \
            --with-openssl=../openssl-${DEFAULT_OPENSSL_VERSION} \
            --with-http_ssl_module \
            --with-http_stub_status_module \
            --with-http_gzip_static_module \
            --with-http_realip_module \
            --with-http_sub_module \
            --with-stream
        cores=$((`grep -c ^processor /proc/cpuinfo` - 1))
        make -j${cores}
        make install
        tar -zcf "/nginx-bin-${nginx_version}.tar.gz" -C "$(dirname $nginx_prefix)" "$(basename $nginx_prefix)"
    } >&2
    [[ $STDOUT ]] && cat "/nginx-bin-${nginx_version}.tar.gz"
}

mian "$@"

