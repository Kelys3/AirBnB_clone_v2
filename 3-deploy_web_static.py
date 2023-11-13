#!/usr/bin/python3
# Sets up a web server for deployment of web_static
"""
    Fabric script that creates and distributes an archive
    on my web servers, using deploy function
"""
from fabric.api import *
from fabric.operations import run, put, sudo, local
from datetime import datetime
import os

env.hosts = ['100.25.197.148', '54.158.210.206']
created_path = None


def do_pack():
    """
        generates a .tgz archive from contents of web_static
    """
    file_name = "versions/web_static_$(date '+%Y%m%d%H%M%S').tgz"
    try:
        local("mkdir -p ./versions")
        local("tar -cvzf{} ./web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
        using fabric to distribute archive
    """
    if not os.path.exists(archive_path):
        return False
    try:
        archive = os.path.basename(archive_path)
        path = "/data/web_static/releases"
        put(archive_path, "/tmp/{}".format(archive))
        folder = archive.split(".")
        run("mkdir -p {}/{}/".format(path, folder[0]))
        new_archive = '.'.join(folder)
        run("tar -xzf /tmp/{} -C {}/{}/"
            .format(new_archive, path, folder[0]))
        run("rm /tmp/{}".format(archive))
        run("mv {}/{}/web_static/* {}/{}/"
            .format(path, folder[0], path, folder[0]))
        run("rm -rf {}/{}/web_static".format(path, folder[0]))
        run("rm -rf /data/web_static/current")
        run("ln -sf {}/{} /data/web_static/current"
            .format(path, folder[0]))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
        deploy function that creates/distributes an archive
    """
    global created_path
    if created_path is None:
        created_path = do_pack()
    if created_path is None:
        return False
    return do_deploy(created_path)
