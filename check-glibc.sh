#!/bin/bash
# 実行ファイルが VPS の glibc(既定 2.39)より新しい版を必要としていないか確かめる。
# 使い方: check-glibc.sh <実行ファイル...>   (環境変数 VPS_GLIBC で上限を変えられる)
# 1つでも上限を超えたら終了コード1。VPS へ送る前に必ず通すこと。
set -u
MAX=${VPS_GLIBC:-2.39}
rc=0
for f in "$@"; do
  need=$(objdump -T "$f" 2>/dev/null | grep -oE 'GLIBC_[0-9]+\.[0-9]+(\.[0-9]+)?' | sed 's/GLIBC_//' | sort -uV | tail -1)
  [ -n "$need" ] || need=none
  if [ "$need" != none ] && [ "$(printf '%s\n%s\n' "$need" "$MAX" | sort -V | tail -1)" != "$MAX" ]; then
    echo "NG  $f  needs glibc $need (> $MAX)"; rc=1
  else
    echo "OK  $f  needs glibc $need (<= $MAX)"
  fi
done
exit $rc
