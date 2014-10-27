#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import subprocess
import threading
import os
import signal

# The utility is run in a fake environment, do no apply any operation that may
# change your system configuration
FAKE_EXEC = False


def run(cmd, timeout=-1):
    if 'FAKE_EXEC' in globals() and FAKE_EXEC:
        print cmd, timeout
        return None
    else:
        return EzShell(cmd, timeout)


class EzShell(object):
    """An easy way to execute shell commands.

    Attributes:
        cmd: Executing commands.
        proc: A process object in executing.
        timeout: Set timeout to stop the process.
            -1 for don't wait the process stop,
            0 for waiting process stop forever,
            >0: timeout in seconds, force the process to stop
                if process is still running
        ret: Return data, including return value and output.
    """

    def __init__(self, cmd, timeout=-1):
        self.cmd = cmd
        self.timeout = timeout
        self.proc = None
        self.ret = None

        if self.timeout > 0:
            self.countdown()
        else:
            self.run()

    def run(self):
        self.proc = subprocess.Popen(
            self.cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        if 0 <= self.timeout:
            self.ret = self.proc.communicate()

    def output(self):
        if not self.ret:
            self.ret = self.proc.communicate()
        return self.ret[0].strip() if self.ret[0] else self.ret[0]

    def err(self):
        if not self.ret:
            self.ret = self.proc.communicate()
        return self.ret[1]

    def returncode(self):
        return self.proc.returncode

    def terminate(self):
        try:
            self.proc.terminate()
            os.killpg(self.proc.pid, signal.SIGKILL)
        except OSError:
            pass

    def countdown(self):
        try:
            thread = threading.Thread(target=self.run)
            thread.daemon = True
            thread.start()
            thread.join(self.timeout)
        except:
            self.terminate()
            raise RuntimeError('Execute error: %s.' % self.cmd)

        self.terminate()

        if thread.is_alive():
            raise RuntimeError('Execute timeout: %s.' % self.cmd)


if __name__ == '__main__':
    cmd = 'ip a show | grep inet'
    cmd = './sleep.sh'
    ret = EzShell.run(cmd, 3)
    print ret.output()
    print ret.returncode()
    print ret.err()
