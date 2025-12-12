#!/bin/sh

case "$(uname -s)" in
  Darwin)
    url="https://api.adoptium.net/v3/binary/latest/17/ga/mac/x64/jdk/hotspot/normal/adoptium?project=jdk"
    ;;
  Linux*)
    url="https://www.sql-workbench.eu/jre/jre_linux64.tar.gz"
    ;;
  *)
    echo "Unknown system: $(uname)"
    exit 1
    ;;
esac

curl --insecure -L "${url}" -o jre17.tar.gz

rm -Rf jre
mkdir jre

tar xf jre17.tar.gz --strip-components=1 --directory jre
