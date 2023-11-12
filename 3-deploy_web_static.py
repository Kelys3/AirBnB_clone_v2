#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py)"""
from fabric.api import local, put, run, env
from os import path

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'your_username'

def do_pack():
    """Function to generate a compressed archive from the web_static folder"""
    local("mkdir -p versions")
    archive_name = "versions/web_static_$(date '+%Y%m%d%H%M%S').tgz"
    result = local("tar -cvzf {} web_static".format(archive_name))
    if result.failed:
        return None
    return archive_name

def do_deploy(archive_path):
    """Function to distribute an archive to web servers"""
    if not path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the /data/web_static/releases/ directory
        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]
        remote_path = "/data/web_static/releases/{}".format(folder_name)
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, remote_path))

        # Create a symbolic link /data/web_static/current linked to the new version
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))

        # Move the contents of the extracted folder to its parent directory
        run("mv {}/web_static/* {}".format(remote_path, remote_path))

        # Clean up by deleting the temporary archive
        run("rm /tmp/{}".format(archive_name))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False

def deploy():
    """Function to deploy the web_static content to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)

if __name__ == '__main__':
    deploy()
