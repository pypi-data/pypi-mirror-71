#!/bin/bash

LIBRDKAFKA_VERSION=0.11.4
OPENSSL_VER=1.0.2o

if [[ ! -e /usr/local/lib/librdkafka.so ]]; then
  echo "librdkafka.so does not exist, installing libs"

  yum install -y zlib-devel unzip

  for i in /usr/local/lib /usr/local/lib64; do
    echo $i
  done > /etc/ld.so.conf.d/usrlocal.conf

  mkdir /tmp/openssl && cd $_ && \
    curl -L https://www.openssl.org/source/openssl-$OPENSSL_VER.tar.gz | \
    tar xz --strip-components=1 && \
    ./config --prefix=/usr/local zlib no-krb5 zlib shared && \
    make && make install && ldconfig && \
    rm -rf /tmp/openssl

  mkdir /tmp/librdkafka && cd $_ && \
    curl -L https://github.com/edenhill/librdkafka/archive/v$LIBRDKAFKA_VERSION.tar.gz | \
    tar xz --strip-components=1 && \
    ./configure && make && make install && ldconfig && \
    rm -rf /tmp/librdkafka
else
  echo "librdkafka.so exists, skipping library install"
fi
