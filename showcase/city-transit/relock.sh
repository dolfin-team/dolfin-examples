#!/bin/sh
# Rebuilds the timetable's import lock from ./network, the files an Agrafe
# release + export would give (rust/cli-imports-todos.md, P0 layout):
#   timetable/.dolfin/imports/<slug>/{lock.json,interface.json,turtle.ttl,closure.ttl}
# Run it after any change to network/, from anywhere:
#   RADEAU=target/debug/radeau examples/showcase/city-transit/relock.sh
# radeau has no `imports fetch` yet, so lock.json (and its artifact_hash,
# glossary_ir::locks::artifact_hash) is written here. The lock is for the
# version network/package.dlf has now, as an Agrafe release of it would be.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
radeau=${RADEAU:-radeau}
iri=https://www.dolfin.fr/showcase/city-transit/network
version=$(sed -n 's/^  version "\(.*\)"$/\1/p' "$here/network/package.dlf")
# Same slug as Agrafe's export: IRI-version, other chars than [A-Za-z0-9._-] as _.
slug=$(printf '%s-%s' "$iri" "$version" | sed 's/[^A-Za-z0-9._-]/_/g; s/\.\./__/g')
lock="$here/timetable/.dolfin/imports/$slug"

rm -rf "$here/timetable/.dolfin/imports"
mkdir -p "$lock"
"$radeau" build "$here/network" --no-comments -o "$lock/turtle.ttl"
"$radeau" glossary "$here/network" --json >"$lock/interface.json"
: >"$lock/closure.ttl"

python3 - "$lock" "$iri" "$version" <<'EOF'
import hashlib, json, sys
lock, iri, version = sys.argv[1:]
read = lambda f: open(f"{lock}/{f}", encoding="utf-8").read()
# `radeau glossary --json` prints map keys in hash order: sort them, so that
# relocking an unchanged network gives the same files.
doc = json.loads(read("interface.json"))
open(f"{lock}/interface.json", "w", encoding="utf-8").write(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
h = hashlib.sha256()
def field(s):
    b = s.encode()
    h.update(len(b).to_bytes(8, "big")); h.update(b)
field(iri); field("\u0001"); field(version)
for f in ("turtle.ttl", "interface.json", "closure.ttl"):
    field(read(f))
doc = {"iri": iri, "requested_version": version, "version": version,
       "source": {"url": iri}, "artifact_hash": h.hexdigest()}
open(f"{lock}/lock.json", "w").write(json.dumps(doc) + "\n")
EOF
echo "lock written to $lock"
