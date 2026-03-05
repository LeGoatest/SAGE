#!/usr/bin/env python3
import os, json, time, socket, subprocess, pathlib

OUT = pathlib.Path(".jules_runtime")
OUT.mkdir(parents=True, exist_ok=True)

def sh(cmd):
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
        return p.stdout
    except Exception as e:
        return f"ERROR running {cmd}: {e}\n"

def read_text(path):
    try:
        return pathlib.Path(path).read_text(errors="replace")
    except Exception as e:
        return f"ERROR reading {path}: {e}\n"

def parse_proc():
    procs = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        p = f"/proc/{pid}"
        try:
            stat = read_text(f"{p}/stat").split()
            if len(stat) < 5:
                continue
            comm = stat[1].strip("()")
            ppid = int(stat[3])
            cmdline = read_text(f"{p}/cmdline").replace("\x00", " ").strip()
            if not cmdline:
                cmdline = comm
            environ_raw = b""
            try:
                environ_raw = open(f"{p}/environ", "rb").read()
            except:
                pass
            env_keys = []
            if environ_raw:
                # store keys only (avoid secrets)
                env_keys = [kv.split(b"=",1)[0].decode(errors="replace") for kv in environ_raw.split(b"\x00") if kv]
            cgroup = read_text(f"{p}/cgroup").strip()
            exe = ""
            try:
                exe = os.readlink(f"{p}/exe")
            except:
                pass
            procs.append({
                "pid": int(pid),
                "ppid": ppid,
                "comm": comm,
                "cmdline": cmdline,
                "exe": exe,
                "cgroup": cgroup,
                "env_keys": env_keys,
            })
        except:
            continue
    return sorted(procs, key=lambda x: (x["ppid"], x["pid"]))

report = {
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "hostname": socket.gethostname(),
    "pwd": os.getcwd(),
    "uid": os.getuid(),
    "gid": os.getgid(),
    "whoami": sh(["whoami"]).strip(),
    "uname": sh(["uname","-a"]).strip(),
    "os_release": read_text("/etc/os-release"),
    "proc_count": 0,
    "notes": "env_keys only; no env values captured to avoid leaking secrets",
}

procs = parse_proc()
report["proc_count"] = len(procs)

(OUT / "processes.json").write_text(json.dumps(procs, indent=2), encoding="utf-8")
(OUT / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

# Helpful system snapshots
(OUT / "ps_ef.txt").write_text(sh(["ps","-ef"]), encoding="utf-8")
(OUT / "ps_forest.txt").write_text(sh(["ps","-eo","pid,ppid,user,etime,%cpu,%mem,cmd","--forest"]), encoding="utf-8")
(OUT / "ss_ltnp.txt").write_text(sh(["ss","-ltnp"]), encoding="utf-8")
(OUT / "ss_lunp.txt").write_text(sh(["ss","-lunp"]), encoding="utf-8")
(OUT / "mount.txt").write_text(sh(["mount"]), encoding="utf-8")
(OUT / "df_h.txt").write_text(sh(["df","-h"]), encoding="utf-8")
(OUT / "env_keys.txt").write_text("\n".join(sorted(set(os.environ.keys()))), encoding="utf-8")

# systemd info (if present)
(OUT / "systemctl_running_services.txt").write_text(sh(["bash","-lc","systemctl list-units --type=service --state=running --no-pager 2>/dev/null || true"]), encoding="utf-8")
(OUT / "journal_boot.txt").write_text(sh(["bash","-lc","sudo journalctl -b --no-pager 2>/dev/null | tail -n 2000 || true"]), encoding="utf-8")

print(f"Wrote VM diagnostics to: {OUT.resolve()}")
