#!/usr/bin/python3
"""A script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers,
using the function do_deploy
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ['54.144.154.247', '54.89.27.191']
env.user = "ubuntu"


def do_pack():
    """generating a .tzg archive"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    arc_path = "version/web_static_{}.tzg".format(date)
    create_archive = local("tar -cvzf {} web_static".format(arc_path))
    if create_archive.succeeded:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """distributing the archives"""
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        version_dir = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(version_dir))
        run("tar -xzf {} -C {}/".format(archived_file, version_dir))
        run("rm {}".format(archived_file))
        run("mv {}/web_static/* {}".format(version_dir, version_dir))
        run("rm -rf {}/web_static".format(version_dir))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(version_dir))

        print("New version deployed!")
        return True

    return False
