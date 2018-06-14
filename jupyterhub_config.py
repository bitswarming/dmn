# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
###
c.DockerSpawner.mem_limit = '800M'
c.Spawner.mem_limit = '800M'
#c.DockerSpawner.read_only_volumes = {"nvidia_driver":"/usr/local/nvidia"}
#c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'nvidia-docker' })
#c.DockerSpawner.extra_create_kwargs = {"volume_driver":"nvidia-docker"}
#c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'nvidia-docker' })
#c.DockerSpawner.extra_host_config = { "devices":["/dev/nvidiactl","/dev/nvidia-uvm","/dev/nvidia-uvm-tools","/dev/nvidia0"] }
###
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
c.NotebookApp.allow_root=True
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd ,  'runtime': 'nvidia'})
#c.DockerSpawner.extra_create_kwargs.update({ 'command': ' jupyter notebook --allow-root' ,  'runtime': 'nvidia'})
#c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd})
#c.DockerSpawner.extra_create_kwargs = {
#    'runtime': 'nvidia',
#}
#c.DockerSpawner.extra_create_kwargs = {'user' : '0'}
#c.DockerSpawner.environment = {['VERBOOKSHAREDPATH' : os.environ['VERBOOKSHAREDPATH'],'VERBOOKUSERID' : 'youare{username}']}
#c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
  #'GRANT_SUDO': '1',
  #'UID': '0', 
#usr = f'{username}'
#print("blalbla %s" % (usr))
#c.DockerSpawner.use_docker_links = True
c.DockerSpawner.links = {
   'jupyterhub': 'jupyterhub',
   'daemon1_dev':'daemon1_dev',
}
  #'USER':'root',
c.DockerSpawner.environment = {
  'GRANT_SUDO': 'yes',
  'VERBOOKSHAREDPATH' :  os.environ['VERBOOKSHAREDPATH'],
  'VERAI_DAEMON_HOST' : 'tincd',
  'VERBOOKUSERID' : 'jupyterhub-user-${JUPYTERHUB_USER}/_data',

}
#c.DockerSpawner.extra_create_kwargs.update({ 'runtime': 'nvidia' })
#c.DockerSpawner.extra_host_config = {'mem_limit': '300m'}
#c.DockerSpawner.environment = {'VERBOOKUSERID' : 'youare{username}'}
#c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd }{, 'environment': {'XXX':"yyy"} })
#/bin/bash -c "export VAR1=VAL1 && export VAR2=VAL2 && your_cmd"
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
#c.DockerSpawner.extra_host_config = { 'network_mode': 'service_tincd' }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
#notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir, 'sokol':'/opt/VerAI/serve' }
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
c.DockerSpawner.volumes = {  'jupyterhub-user-{username}-home': notebook_dir, 'jupyterhub-user-{username}': '/opt/VerAI/serve' }
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
#c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8080
#c.JupyterHub.base_url = '/verbook/10.0.1.10/'
#c.JupyterHub.base_url = '/verbook/169.254.1.2/'
c.JupyterHub.base_url = '/verbook/'+os.environ['TINCIP']+'/'
#c.JupyterHub.bind_url = 'http://127.0.0.1:8000'

# TLS config
#c.JupyterHub.port = 80
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Authenticate users with GitHub OAuth
#c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
#c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
#c.Spawner.default_url = '/lab'
#c.DockerSpawner.default_url = '/lab'
#c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
#c.DummyAuthenticator.password = "181818"
#c.JupyterHub.authenticator_class = 'jwtauthenticator.jwtauthenticator.JSONWebTokenLocalAuthenticator'
c.JupyterHub.authenticator_class = 'jwtauthenticator.jwtauthenticator.JSONWebTokenAuthenticator'
# one of "secret" or "signing_certificate" must be given.  If both, then "secret" will be the signing method used.
c.JSONWebTokenAuthenticator.secret = 'mySigningKey'            # The secrect key used to generate the given token
c.JupyterHub.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors * ",
    }
}
#c.JupyterHub.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors 'self' https://10.0.1.24:443/"} }
#c.JupyterHub.tornado_settings = { 'headers': { 'Content-Security-Policy': "frame-ancestors https://deploy.ver.ai:80/form-1/ ; " } }
#c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors '*' "}
# -OR-
#c.JSONWebTokenAuthenticator.signing_certificate = '/foo/bar/adfs-signature.crt'    # The certificate used to sign the incoming JSONWebToken, must be in PEM Format
c.JSONWebTokenAuthenticator.username_claim_field = 'name'                           # The claim field contianing the username/sAMAccountNAme/userPrincipalName
c.JSONWebTokenAuthenticator.audience = ''               # This config option should match the aud field of the JSONWebToken, empty string to disable the validation of this field.
c.JSONWebLocalTokenAuthenticator.create_system_users = True                       # This will enable local user creation upon authentication, requires JSONWebTokenLocalAuthenticator
c.JSONWebTokenAuthenticator.header_name = 'Authorization'                         # default valuekjkj

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

# Whitlelist users and admins
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True
pwd = os.path.dirname(__file__)
with open(os.path.join(pwd, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
