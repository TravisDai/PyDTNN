#!/bin/bash

export ENABLE_CONV_GEMM=False

SCRIPT_PATH="$(cd "$(dirname "$0")" >/dev/null 2>&1 || exit 1; pwd -P)"
exec "${SCRIPT_PATH}"/run_alexnet_cifar10_conv_gemm.sh
