"""
fake_environment.py
───────────────────
Part of an AI-powered honeypot system.

Generates realistic fake system environments dynamically so that
attackers interacting with the honeypot cannot easily detect that
it is fake.  Everything is self-contained — no external APIs required.

Usage:
    python fake_environment.py
"""

import random
import string
import json
from datetime import datetime, timedelta


# ──────────────────────────────────────────────
# Helper utilities
# ──────────────────────────────────────────────

def _random_ip():
    """Return a random private-ish IPv4 address."""
    return f"{random.choice([10, 172, 192])}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def _random_timestamp(days_back=90):
    """Return a random ISO-8601 timestamp within the last `days_back` days."""
    now = datetime.now()
    delta = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return (now - delta).strftime("%Y-%m-%dT%H:%M:%S")


def _random_mac():
    """Return a random MAC address."""
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))


# ──────────────────────────────────────────────
# 1. Generate a fake OS / system profile
# ──────────────────────────────────────────────

def generate_os_profile():
    """
    Build a realistic-looking operating system profile.

    Returns a dict with keys like 'os_name', 'os_version',
    'hostname', 'kernel', 'architecture', etc.
    """

    # Pool of realistic OS options with matching kernel patterns
    os_options = [
        {
            "os_name": "Ubuntu",
            "versions": ["18.04.6 LTS", "20.04.5 LTS", "22.04.3 LTS", "24.04.1 LTS"],
            "kernel_prefix": "5.",
            "kernel_range": (4, 19),
        },
        {
            "os_name": "CentOS",
            "versions": ["7.9.2009", "8.5.2111", "Stream 9"],
            "kernel_prefix": "4.",
            "kernel_range": (18, 18),
        },
        {
            "os_name": "Debian",
            "versions": ["10.13 (Buster)", "11.8 (Bullseye)", "12.4 (Bookworm)"],
            "kernel_prefix": "5.",
            "kernel_range": (10, 15),
        },
        {
            "os_name": "Red Hat Enterprise Linux",
            "versions": ["8.9", "9.3"],
            "kernel_prefix": "5.",
            "kernel_range": (14, 14),
        },
        {
            "os_name": "Windows Server",
            "versions": ["2016 Standard", "2019 Datacenter", "2022 Standard"],
            "kernel_prefix": None,   # Windows doesn't expose a Linux kernel
            "kernel_range": None,
        },
    ]

    chosen = random.choice(os_options)
    is_linux = chosen["kernel_prefix"] is not None

    # Build a realistic hostname  (e.g.  "prod-web-03", "srv-db-17")
    prefixes = ["prod", "stg", "dev", "srv", "node", "app", "infra"]
    roles    = ["web", "db", "api", "cache", "worker", "proxy", "mail", "mon"]
    hostname = f"{random.choice(prefixes)}-{random.choice(roles)}-{random.randint(1, 99):02d}"

    # Kernel version (Linux only)
    kernel = None
    if is_linux and chosen["kernel_range"] is not None and chosen["kernel_prefix"] is not None:
        minor = random.randint(*chosen["kernel_range"])
        patch = random.randint(0, 250)
        suffix = random.choice(["-generic", "-cloud-amd64", ".el8.x86_64", ".el9.x86_64", ""])
        kernel = f"{chosen['kernel_prefix']}{minor}.{patch}{suffix}"

    profile = {
        "os_name": chosen["os_name"],
        "os_version": random.choice(chosen["versions"]),
        "hostname": hostname,
        "kernel": kernel if kernel else "N/A (Windows)",
        "architecture": random.choice(["x86_64", "amd64"]),
        "uptime_days": random.randint(1, 365),
        "ip_address": _random_ip(),
        "mac_address": _random_mac(),
    }

    return profile


# ──────────────────────────────────────────────
# 2. Generate fake running services
# ──────────────────────────────────────────────

def generate_services():
    """
    Produce a list of fake network services, each with a port,
    name, version, and current state.
    """

    # Realistic service pool — port, name, and plausible version strings
    service_pool = [
        {"port": 22,   "name": "OpenSSH",          "versions": ["7.6p1", "8.2p1", "8.9p1", "9.3p1"]},
        {"port": 80,   "name": "Apache httpd",      "versions": ["2.4.41", "2.4.52", "2.4.57"]},
        {"port": 443,  "name": "nginx",             "versions": ["1.18.0", "1.22.1", "1.25.3"]},
        {"port": 3306, "name": "MySQL",             "versions": ["5.7.42", "8.0.35", "8.2.0"]},
        {"port": 5432, "name": "PostgreSQL",        "versions": ["13.13", "14.10", "15.5", "16.1"]},
        {"port": 21,   "name": "vsftpd",            "versions": ["3.0.3", "3.0.5"]},
        {"port": 25,   "name": "Postfix smtpd",     "versions": ["3.4.13", "3.6.4", "3.8.3"]},
        {"port": 6379, "name": "Redis",             "versions": ["6.2.14", "7.0.14", "7.2.3"]},
        {"port": 8080, "name": "Apache Tomcat",     "versions": ["9.0.82", "10.1.16"]},
        {"port": 27017,"name": "MongoDB",           "versions": ["5.0.22", "6.0.12", "7.0.4"]},
        {"port": 53,   "name": "BIND",              "versions": ["9.16.44", "9.18.21"]},
        {"port": 8443, "name": "Jetty",             "versions": ["11.0.18", "12.0.3"]},
        {"port": 111,  "name": "rpcbind",           "versions": ["0.2.3", "1.2.6"]},
        {"port": 2049, "name": "NFS",               "versions": ["4.1", "4.2"]},
        {"port": 9200, "name": "Elasticsearch",     "versions": ["7.17.15", "8.11.3"]},
    ]

    # Pick a random subset (5-9 services) to look realistic
    count = random.randint(5, 9)
    chosen = random.sample(service_pool, k=min(count, len(service_pool)))

    services = []
    for svc in chosen:
        services.append({
            "port": svc["port"],
            "protocol": "tcp",
            "service": svc["name"],
            "version": random.choice(svc["versions"]),
            "state": random.choices(["running", "listening", "active"], weights=[5, 3, 2])[0],
        })

    # Sort by port for a tidy look
    services.sort(key=lambda s: s["port"])
    return services


# ──────────────────────────────────────────────
# 3. Generate fake users
# ──────────────────────────────────────────────

def generate_users():
    """
    Create a list of fake system users with home directories,
    shells, UIDs, and permission levels.
    """

    # System / privileged accounts
    base_users = [
        {"username": "root",   "uid": 0,    "privilege": "superuser", "shell": "/bin/bash"},
        {"username": "admin",  "uid": 1000, "privilege": "admin",     "shell": "/bin/bash"},
    ]

    # Pool of normal-looking usernames an attacker might expect
    extra_names = [
        "user1", "devops", "deploy", "jenkins", "ansible",
        "ubuntu", "centos", "ftpuser", "backup", "svc_monitor",
        "developer", "webadmin", "dbadmin", "appuser", "testuser",
        "git", "ci-runner", "nagios", "prometheus", "kafka",
    ]

    shells = ["/bin/bash", "/bin/sh", "/usr/sbin/nologin", "/bin/zsh"]

    # Pick 3-7 extra users on top of root & admin
    sample_size = random.randint(3, 7)
    chosen_names = random.sample(extra_names, k=sample_size)

    users = list(base_users)  # copy
    for idx, name in enumerate(chosen_names, start=1001):
        privilege = random.choice(["standard", "standard", "limited", "service"])
        shell = random.choice(shells)
        # Service accounts typically have nologin
        if privilege == "service":
            shell = "/usr/sbin/nologin"

        users.append({
            "username": name,
            "uid": idx,
            "privilege": privilege,
            "shell": shell,
            "home": f"/home/{name}",
            "last_login": _random_timestamp(days_back=30),
        })

    return users


# ──────────────────────────────────────────────
# 4. Generate a fake file system structure
# ──────────────────────────────────────────────

def generate_filesystem():
    """
    Build a dictionary representing a realistic directory tree
    with fake files that include names, sizes, and timestamps.
    """

    def _fake_file(name):
        """Helper — create metadata for a single fake file."""
        return {
            "name": name,
            "size_bytes": random.randint(64, 5_000_000),
            "modified": _random_timestamp(days_back=60),
            "permissions": random.choice([
                "-rw-r--r--",
                "-rw-------",
                "-rwxr-xr-x",
                "-rw-rw-r--",
            ]),
        }

    filesystem = {
        "/etc": [
            _fake_file("passwd"),
            _fake_file("shadow"),
            _fake_file("hosts"),
            _fake_file("resolv.conf"),
            _fake_file("ssh/sshd_config"),
            _fake_file("nginx/nginx.conf"),
            _fake_file("crontab"),
            _fake_file("fstab"),
        ],
        "/home/admin": [
            _fake_file(".bash_history"),
            _fake_file(".ssh/authorized_keys"),
            _fake_file("notes.txt"),
            _fake_file("config.yaml"),
        ],
        "/var/log": [
            _fake_file("syslog"),
            _fake_file("auth.log"),
            _fake_file("kern.log"),
            _fake_file("nginx/access.log"),
            _fake_file("nginx/error.log"),
            _fake_file("mysql/error.log"),
            _fake_file("cron.log"),
        ],
        "/tmp": [
            _fake_file("backup.sql"),
            _fake_file("deploy_20240301.tar.gz"),
            _fake_file("passwords.txt"),
            _fake_file("session_token.tmp"),
        ],
        "/opt": [
            _fake_file("app/server.jar"),
            _fake_file("app/config.yaml"),
            _fake_file("scripts/cleanup.sh"),
        ],
        "/var/www/html": [
            _fake_file("index.html"),
            _fake_file("login.php"),
            _fake_file(".env"),
            _fake_file("uploads/.htaccess"),
        ],
        "/root": [
            _fake_file(".bash_history"),
            _fake_file(".ssh/id_rsa"),
            _fake_file(".ssh/id_rsa.pub"),
            _fake_file("emergency_access.key"),
        ],
    }

    return filesystem


# ──────────────────────────────────────────────
# 5. Generate fake logs
# ──────────────────────────────────────────────

def generate_logs(count=15):
    """
    Create a list of fake log entries: SSH attempts,
    system events, and application messages.

    Args:
        count: total number of log lines to generate.
    """

    logs = []

    # --- SSH login attempts ---
    ssh_users   = ["root", "admin", "ubuntu", "deploy", "test", "guest", "oracle", "postgres"]
    ssh_results = ["Accepted", "Failed", "Failed", "Failed"]  # bias toward failures

    for _ in range(count // 3 + 1):
        user   = random.choice(ssh_users)
        result = random.choice(ssh_results)
        ip     = _random_ip()
        port   = random.randint(40000, 65535)
        logs.append({
            "type": "ssh",
            "timestamp": _random_timestamp(days_back=7),
            "message": (
                f"{result} password for {user} from {ip} port {port} ssh2"
            ),
        })

    # --- System / kernel logs ---
    sys_messages = [
        "systemd[1]: Started Session {sid} of user {user}.",
        "kernel: [UFW BLOCK] IN=eth0 OUT= SRC={src} DST={dst} PROTO=TCP DPT={dpt}",
        "CRON[{pid}]: (root) CMD (/usr/local/bin/cleanup.sh)",
        "systemd[1]: Reloading nginx.service.",
        "kernel: Out of memory: Kill process {pid} (java) score {score}",
        "systemd-logind[{pid}]: New session {sid} of user {user}.",
        "dhclient: DHCPREQUEST on eth0 to {dst} port 67",
    ]

    for _ in range(count // 3 + 1):
        template = random.choice(sys_messages)
        message = template.format(
            sid=random.randint(100, 9999),
            user=random.choice(["root", "admin", "deploy"]),
            src=_random_ip(),
            dst=_random_ip(),
            dpt=random.choice([22, 80, 443, 3306, 8080]),
            pid=random.randint(1000, 65535),
            score=random.randint(100, 999),
        )
        logs.append({
            "type": "system",
            "timestamp": _random_timestamp(days_back=7),
            "message": message,
        })

    # --- Application logs ---
    http_methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
    http_paths   = ["/", "/login", "/api/v1/users", "/admin", "/wp-admin",
                    "/phpmyadmin", "/.env", "/robots.txt", "/api/health"]
    status_codes = [200, 200, 200, 301, 403, 404, 404, 500]

    for _ in range(count // 3 + 1):
        method = random.choice(http_methods)
        path   = random.choice(http_paths)
        status = random.choice(status_codes)
        size   = random.randint(128, 52000)
        ip     = _random_ip()
        logs.append({
            "type": "application",
            "timestamp": _random_timestamp(days_back=7),
            "message": f'{ip} - - "{method} {path} HTTP/1.1" {status} {size}',
        })

    # Sort all logs chronologically so they look real
    logs.sort(key=lambda l: l["timestamp"])
    return logs


# ──────────────────────────────────────────────
# 6. Build the complete environment
# ──────────────────────────────────────────────

def build_environment():
    """
    Assemble every fake component into a single structured
    dictionary that represents the full honeypot environment.
    """

    environment = {
        "os": generate_os_profile(),
        "services": generate_services(),
        "users": generate_users(),
        "filesystem": generate_filesystem(),
        "logs": generate_logs(),
    }

    return environment


# ──────────────────────────────────────────────
# 7. Main entry point
# ──────────────────────────────────────────────

def main():
    """Generate and display the fake environment as pretty JSON."""
    env = build_environment()
    print(json.dumps(env, indent=2))


if __name__ == "__main__":
    main()
