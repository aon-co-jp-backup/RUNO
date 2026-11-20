#!/bin/bash
# VPS(AlmaLinux 10.2, glibc 2.39)向けの Linux バイナリを作る。
# 使い方(PowerShell から): wsl -d Ubuntu-24.04 -- bash /mnt/f/runo/vps-build.sh <crate dir> <cargo build の引数...>
#   例: wsl -d Ubuntu-24.04 -- bash /mnt/f/runo/vps-build.sh /mnt/f/open-web-server -p open-web-server-gateway --bin open-web-server --features admin-2fa,domain-watchdog,fastcgi-client,ddns,sftp
# 既定の WSL(Ubuntu 26.04)は glibc 2.43 なので、そこで作ると VPS で動かないことがある。
# このスクリプトは Ubuntu-24.04(glibc 2.39)で作り、出来た実行ファイルを check-glibc.sh で検査する。
set -euo pipefail
DIR=$1; shift
export PATH=$HOME/.cargo/bin:$PATH
NAME=$(basename "$DIR")
export CARGO_TARGET_DIR=$HOME/vps-target/$NAME
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$DIR"
echo "rustc: $(rustc --version)  glibc: $(ldd --version | head -1)"
cargo build --release "$@" 2>&1 | tee /tmp/vps-build.log | grep -E '^error|Finished|could not compile' || true
BINS=$(find "$CARGO_TARGET_DIR/release" -maxdepth 1 -type f -perm -u+x ! -name '*.d')
grep -q '^error' /tmp/vps-build.log && { echo 'build failed (see /tmp/vps-build.log)'; exit 1; }
bash "$HERE/check-glibc.sh" $BINS
