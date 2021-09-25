
import os
import subprocess
import go

class Run(go.BaseRunner):
    def __init__(self):
        self.process = None

    def description(self):
        return [
            "Docker base image"
        ]

    def config(self):
        os.makedirs("/config/data", mode=0o777, exist_ok=True)
        os.makedirs("/config/logs", mode=0o777, exist_ok=True)
        os.makedirs("/config/run", mode=0o777, exist_ok=True)
        
        if not os.path.isdir("/usr/lib/unifi/data") and not os.path.islink("/usr/lib/unifi/data"):
            os.symlink("/config/data", "/usr/lib/unifi/data")
        if not os.path.isdir("/usr/lib/unifi/logs") and not os.path.islink("/usr/lib/unifi/logs"):
            os.symlink("/config/logs", "/usr/lib/unifi/logs")
        if not os.path.isdir("/usr/lib/unifi/run") and not os.path.islink("/usr/lib/unifi/run"):
            os.symlink("/config/run", "/usr/lib/unifi/run")

    def run(self):
        self.process = subprocess.Popen(
            args = [
                "java",
                "-jar", "/usr/lib/unifi/lib/ace.jar",
                "start",
                "-pidfile /var/run/unifi.pid",
                "-Dfile.encoding=UTF-8",
                "-Djava.awt.headless=true",
                "-Dapple.awt.UIElement=true",
                "-Dunifi.core.enabled=false",
                "-Xmx1024M",
                "-XX:+ExitOnOutOfMemoryError",
                "-XX:+CrashOnOutOfMemoryError",
                "-XX:ErrorFile=/usr/lib/unifi/logs/hs_err_pid%p.log",
                "-Dunifi.datadir=/usr/lib/unifi/data",
                "-Dunifi.logdir=/usr/lib/unifi/logs",
                "-Dunifi.rundir=/var/run/unifi",
                "-Dunifi.core.enabled=false",
                "-procname unif",
                "-outfile SYSLOG",
                "-errfile SYSLOG"
            ],
            cwd = "/config"
        )
        return self.process.wait()

    def stop(self):
        self.process.kill()

    def check(self):
        return self.process.poll() is None

