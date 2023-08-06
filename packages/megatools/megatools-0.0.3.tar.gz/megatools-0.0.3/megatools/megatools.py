import logging
import subprocess
import os

logger = logging.getLogger("megatools")


class Megatools:
    megatools_path = ""

    def __init__(self, executable="megatools"):
        self.executable = executable

    def dl(
        self,
        link,
        path=None,
        no_progress=False,
        print_names=False,
        disable_resume=False,
        username=None,
        password=None,
        reload=False,
        limit_speed=0,
        proxy=None,
        netif=None,
        ip_proto=None,
        config=None,
        ignore_config_file=False,
        display_output=False,
        debug=None,
        version=None,
    ):
        """
        Usage:
          megatools dl [OPTION?] - download exported files from mega.nz

        Help Options:
          -h, --help                  Show help options

        Application Options:
          --path=PATH                 Local directory or file name, to save data to
          --no-progress               Disable progress bar
          --print-names               Print names of downloaded files
          --choose-files              Choose which files to download when downloading folders (interactive)
          --disable-resume            Disable resume when downloading file
          -u, --username=USERNAME     Account username (email)
          -p, --password=PASSWORD     Account password
          --no-ask-password           Never ask interactively for a password
          --reload                    Reload filesystem cache
          --limit-speed=SPEED         Limit transfer speed (KiB/s)
          --proxy=PROXY               Proxy setup string
          --netif=NAME                Network interface or local IP address used for outgoing connections
          --ip-proto=PROTO            Which protocol to prefer when connecting to mega.nz (v4, v6, or any)
          --config=PATH               Load configuration from a file
          --ignore-config-file        Disable loading mega.ini
          --debug=OPTS                Enable debugging output
          --version                   Show version information
        """

        command = f"{self.executable} dl {link} --no-ask-password"

        if path:
            command += "--path="
            command += path
            command += " "

        if no_progress:
            command += "--no-progress"
            command += " "

        if print_names:
            command += "--print-names"
            command += " "

        if disable_resume:
            command += "--disable-resume"
            command += " "

        if username:
            command += "--username="
            command += username
            command += " "

        if password:
            command += "--password="
            command += password
            command += " "

        if reload:
            command += "--reload"
            command += " "

        if limit_speed:
            command += "----limit-speed="
            command += limit_speed
            command += " "

        if proxy:
            command += "--proxy="
            command += proxy
            command += " "

        if netif:
            command += "--netif="
            command += netif
            command += " "

        if ip_proto:
            command += "--ip_proto="
            command += ip_proto
            command += " "

        if config:
            command += "--config="
            command += config
            command += " "

        if ignore_config_file:
            command += "--ignore-config-file"
            command += " "

        if debug:
            command += "--debug="
            command += debug
            command += " "

        if version:
            command += "--version"
            command += " "

        logger.debug(command)

        exit_code = execute_command(command, display_output)

        logger.debug(exit_code)

        return exit_code


def execute_command(command, display_output=False):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if display_output:
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.strip())
        return process.poll()
    else:
        return process.wait()


if __name__ == "__main__":
    """
    formatter = logging.Formatter(
        "%(asctime)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(stream_handler)
    """
    megatools = Megatools(executable="C:\megatools\megatools.exe")
    """
    exit_code = megatools.dl(
        "https://mega.nz/file/PpVB0CTZ#bwa51HbeKaVjuCff_lzbH4nQnV27uBxmcF89PnnACvY"
    )
    """
    exit_code = megatools.dl(
        "https://mega.nz/#!PpVB0CTZ!bwa51HbeKaVjuCff_lzbH4nQnV27uBxmcF89PnnACvY",
        path=None,
        no_progress=False,
        print_names=False,
        disable_resume=False,
        username=None,
        password=None,
        reload=False,
        limit_speed=0,
        proxy=None,
        netif=None,
        ip_proto=None,
        config=None,
        ignore_config_file=False,
        display_output=False,
        debug=None,
        version=None,
    )
    print(exit_code)
