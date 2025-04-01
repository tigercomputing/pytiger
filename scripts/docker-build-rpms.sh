#!/bin/bash
#
# This script can be used to build a source RPM locally, using Docker. It will
# build using all the variants we support, that is a mixture of CentOS 6 and 7
# with or without various SCL Python versions. Results are output into the
# build/ directory.
#
set -eu -o pipefail

src_rpm="${1:-}"
if [ -z "$src_rpm" ]; then
  echo "usage: $0 <source>" >&2
  exit 1
fi

builds=(
  "centos:7"
  "centos:7&rh-python35"
  "centos:7&rh-python36"
  "centos:6"
  "centos:6&python27"
  "centos:6&rh-python36"
)

for build in "${builds[@]}"; do
  IFS='&' read -r image rpm_scl <<< "${build}"

  cid="$(docker run --rm -d -i "${image}" sh -c "while sleep 1; do :; done")"

  docker cp "${src_rpm}" "${cid}:/"

  docker exec -i $cid bash <<EOF
set -euxo pipefail

yum -y install \
  epel-release \
  ${rpm_scl:+centos-release-scl}

yum -y install \
  epel-rpm-macros \
  rpm-build \
  ${rpm_scl:+${rpm_scl}-build}

yum -y install \
  \$(rpmbuild --rebuild "$(basename "${src_rpm}")" 2>&1 | \
    awk '/is needed by/ { print \$1 }')

rpmbuild --rebuild "$(basename "${src_rpm}")"
EOF

  docker cp "${cid}:/root/rpmbuild/RPMS/." ./build/

  docker stop "${cid}"
done

# vim: ai ts=2 sw=2 et sts=2 ft=sh
