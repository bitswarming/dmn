# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8080
c.JupyterHub.base_url = '/verbook/'+os.environ['TINCIP']+'/'
#c.JupyterHub.port = 80
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']
c.JupyterHub.authenticator_class = 'jwtauthenticator.jwtauthenticator.JSONWebTokenAuthenticator'
c.JSONWebTokenAuthenticator.secret = 'mySigningKey'            # The secrect key used to generate the given token
c.DockerSpawner.default_url = '/lab'
c.Spawner.default_url = '/lab'
#c.JupyterHub.api_tokens = {
#    'c0634a192acc4e80ad36f65b3817ca77': 'admin',
#}
#c.JupyterHub.allow_named_servers = True
c.JupyterHub.tornado_settings = {
       'headers': {
            'Content-Security-Policy': "frame-ancestors * ",
       }
    }
c.JSONWebTokenAuthenticator.username_claim_field = 'name'                           # The claim field contianing the username/sAMAccountNAme/userPrincipalName
c.JSONWebTokenAuthenticator.audience = ''               # This config option should match the aud field of the JSONWebToken, empty string to disable the validation of this field.
c.JSONWebLocalTokenAuthenticator.create_system_users = True                       # This will enable local user creation upon authentication, requires JSONWebTokenLocalAuthenticator
c.JSONWebTokenAuthenticator.header_name = 'Authorization'                         # default valuekjkj


# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

c.NotebookApp.allow_root=True
#c.NotebookApp.nbserver_extensions = {
#    'nbverai': True,
#}
#c.NotebookApp.disable_check_xsrf = True



    # Persist hub data on volume mounted inside container
data_dir  = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir, 'jupyterhub_cookie_secret')

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
                              
#c.JupyterHub.spawner_class = CustomDockerSpawner

# Spawn single-user servers as Docker containers
#CUSTOM
from dockerspawner import DockerSpawner
class CustomDockerSpawner(DockerSpawner):
 def start(self):
    #c = get_config()
    username = self.user.name
    nbk = username.split('!')
    username = username.replace('!', '!')
    self.default_url = '/lab'
    self.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']

    #self.volumes = {  'jupyterhub-user-{username}-home': '/home/jovyan' }

#    self.volumes.update({ 'jupyterhub-user-{username}-cmpid': '/cmpid'})

    #with open("xxxfile5", "w+") as link_file:
    #  link_file.write("Variable =  %s"%(username))
  
    #return super().start()

    #c.JupyterHub.spawner_class = CustomDockerSpawner
    self.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
    #spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
    spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "jupyter labhub")
    self.extra_create_kwargs.update({ 'command': spawn_cmd })
    self.extra_create_kwargs.update({ 'runtime' : 'nvidia' })
 
    self.links = {
      'jupyterhub': 'jupyterhub',
      'daemon1_dev':'daemon1_dev',
    }
    self.environment = {
  	'GRANT_SUDO': 'yes',
  	'runtime': 'nvidia',
  	'VERBOOKSHAREDPATH' :  os.environ['VERBOOKSHAREDPATH'],
  	'VERAI_DAEMON_HOST' : 'tincd',
  	'VERBOOKUSERID' : 'jupyterhub-user-${JUPYTERHUB_USER}-home/_data',
  	'NV_GPU':'0',
  	'CUDA_VISIBLE_DEVICES':'0',
  	'NVIDIA_VISIBLE_DEVICES':'0',
  	'VERBOOKSERVERFOLDER' : '/opt/VerAI/serve',
  	'VERBOOKSERVEFOLDER' : '/home/jovyan',
        'JUPYTER_ENABLE_LAB' : 1,
    }
    network_name = os.environ['DOCKER_NETWORK_NAME']
    self.use_internal_ip = True
    self.network_name = network_name
    self.extra_host_config = { 'network_mode': network_name, 'runtime':'nvidia' }
    notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
    if not os.path.exists( '/var/lib/docker/volumes/jupyterhub-user-'+username+'-home/_data/'+nbk[1] ):
       os.mkdir( '/var/lib/docker/volumes/jupyterhub-user-'+username+'-home/_data/'+nbk[1], 0o777)
       #os.mkdir('/zzz',0o755)
    #os.chmod( '/var/lib/docker/volumes/jupyterhub-user-'+username+'-home/_data/'+nbk[1], 0o777)     
    os.chown( '/var/lib/docker/volumes/jupyterhub-user-'+username+'-home/_data/'+nbk[1], 1000,1000)     
    self.notebook_dir = notebook_dir
    #with open("yyyfile5", "w+") as link_file:
    #  link_file.write("Variable =  %s"%(nbk[0]))
  
    self.volumes = { '/var/lib/docker/volumes/jupyterhub-user-'+username+'-home/_data/'+nbk[1]: notebook_dir }
    self.remove_containers = True
    self.debug = True

    return super().start()

c.JupyterHub.spawner_class = CustomDockerSpawner
#c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'
