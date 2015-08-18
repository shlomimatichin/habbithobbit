import subprocess
import logging

_logger = logging.getLogger('run')


def run(command, cwd=None):
    with open("/dev/null") as devNull:
        try:
            output = subprocess.check_output(
                command, cwd=cwd, stderr=subprocess.STDOUT,
                stdin=devNull, close_fds=True)
        except subprocess.CalledProcessError as e:
            _logger.error("Failed command '%(command)s' output:\n%(output)s", dict(
                command=command, output=e.output))
            raise
    return output


def interactive(command, cwd=None):
    with open("/dev/null") as devNull:
        try:
            subprocess.check_call(command, cwd=cwd, close_fds=True)
        except subprocess.CalledProcessError as e:
            _logger.error("Failed command '%(command)s'", dict(command=command))
            raise
