#!/bin/bash

# ENOUGH_API_TOKEN=abc tests/run-tests.sh tox -e openvpn -- --enough-no-create --enough-no-tests playbooks/openvpn/tests

set -ex

function prepare_environment() {
    if test $(id -u) != 0 ; then
        SUDO=sudo
    fi
    $SUDO apt-get update
    $SUDO apt-get install -y git
}

function prepare_inventory() {
    if ! test -f inventory/group_vars/all/clouds.yml ; then
        cat > tests/clouds.yml <<EOF
---
clouds:
  ovh:
    auth:
      auth_url: "$OS_AUTH_URL"
      project_name: "$OS_PROJECT_NAME"
      project_id: "$OS_PROJECT_ID"
      user_domain_name: "$OS_USER_DOMAIN_NAME"
      username: "$OS_USERNAME"
      password: "$OS_PASSWORD"
    region_name: "$OS_REGION_NAME"
EOF
    else
        cat inventory/group_vars/all/clouds.yml > tests/clouds.yml
    fi

    if ! test -f inventory/group_vars/all/domain.yml ; then
        cat > tests/domain.yml <<EOF
---
domain: enough.community
EOF
    else
        cat inventory/group_vars/all/domain.yml > tests/domain.yml
    fi
}

function image_name() {
    if test "$GITLAB_CI" ; then
        echo enough-tox-$(date +%s)
        trap "docker rm -f $name >& /dev/null || true ; docker rmi --no-prune $name >& /dev/null || true"  EXIT
    else
        echo enough-tox
    fi
}

function build_image() {
    local name="$1"

    (
        cat enough/common/data/base.dockerfile
        cat tests/tox.dockerfile
    ) | docker build --build-arg=USER_ID="$(id -u)" --build-arg=DOCKER_GID="$(getent group docker | cut -d: -f3)" --build-arg=USER_NAME="${USER:-root}" --tag $name -f - .
}

function run_tests_on_ref() {
    local ref="$1"
    local name="$2"
    local toplevel="$3"
    local service="$4"

    local basedir=$(dirname $toplevel)
    local refdir="$basedir/infrastructure-versions/$ref"
    mkdir -p $refdir
    if ! test -d $refdir/infrastructure ; then
        git clone --reference . . $refdir/infrastructure
        cp -a bootstrap dev-links.sh $refdir/infrastructure
        (
            cd $refdir/infrastructure

            bootstrap
            ./dev-links.sh
        )
    fi

    (
        cd $refdir/infrastructure

        source ../virtualenv/bin/activate

        run_tests $name $refdir/infrastructure tox -e $service -- --enough-no-destroy playbooks/$service/tests

        local c=.tox/$service/.pytest_cache
        mkdir -p $toplevel/$c
        rsync -av --delete $c/ $toplevel/$c/
    )
}

function run_tests() {
    local name="$1"
    shift
    local d="$1"
    shift

    find $d \( -name '*.pyc' -o -name '*.pyo' -o -name __pycache__ \) -delete
    if test "$SKIP_OPENSTACK_INTEGRATION_TESTS" ; then
        skip="-e SKIP_OPENSTACK_INTEGRATION_TESTS=true"
    fi
    if test "$GITLAB_CI" ; then
        args="--workdir /opt"
    else
        args="--volume ${d}:${d} --workdir ${d} --volume $HOME/.enough:$HOME/.enough"
    fi
    docker run --rm --device=/dev/net/tun --name $name --user "${USER:-root}" -e ENOUGH_API_TOKEN=$ENOUGH_API_TOKEN $skip --cap-add=NET_ADMIN $args --volume /var/run/docker.sock:/var/run/docker.sock $name "${@:-tox}"
}

function main() {
    prepare_environment
    prepare_inventory
    local name=$(image_name "$@")
    build_image $name
    local toplevel=$(git rev-parse --show-toplevel)
    if test "$1" = "--upgrade" ; then
        shift
        local ref="$1"
        local service="$2"
        run_tests_on_ref $ref $name $toplevel $service
        run_tests $name $toplevel tox -e $service
    else
        run_tests $name $toplevel "$@"
    fi
}

main "$@"
