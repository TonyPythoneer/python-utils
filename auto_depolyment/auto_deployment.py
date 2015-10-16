import os
import commands
import sys
from string import Template


# Global variables: repo
REPO_FILENAME = os.path.dirname(os.path.abspath(__name__)) # Example: /../p-pjname
REPO_DIR = os.path.dirname(REPO_FILENAME)  # Example: /../
REPO_NAME = os.path.basename(REPO_FILENAME) # Example: p-pjname

# Global variables: pj
PJ_NAME = REPO_NAME.split('-')[-1]  # Example: pjname
PJ_NGINX = '{PJ_NAME}_nginx.conf'.format(PJ_NAME=PJ_NAME)
PJ_UWSGI = '{PJ_NAME}_uwsgi.ini'.format(PJ_NAME=PJ_NAME)

# Global variables: deployment
DEPLOYMENT_TEMPLATE_DIR = os.path.join(REPO_FILENAME, 'deployment_template')  # Example: /../p-pjname/deployment_template
DEPLOYMENT_DIR = os.path.join(REPO_FILENAME, 'deployment')  # Example: /../p-pjname/deployment

# Global variables: service
INSTALL_BASE_DIR = '/backend_service/'
SERVICE_FILENAME = os.path.join(INSTALL_BASE_DIR, REPO_NAME)  # Example: /backend_service/p-pjname
SERVICE_DEPLOYMENT_FILENAME = os.path.join(SERVICE_FILENAME, 'deployment')  # Example: /backend_service/p-pjname/deployment


def establish_config_for_service():
    def establish_config_file(read_file, write_file, tmpl_kwargs=None):
        content = ''
        with open(os.path.join(DEPLOYMENT_TEMPLATE_DIR, read_file), 'r') as f:
            content = Template(f.read()).substitute(**tmpl_kwargs) if tmpl_kwargs else f.read()
        with open(os.path.join(DEPLOYMENT_DIR, write_file), 'w') as f:
            f.write(content)

    # Local variables
    nginx_kwargs = {"repo_name": REPO_NAME,
                    "service_deployment_filename": SERVICE_DEPLOYMENT_FILENAME}
    uwsgi_kwargs = {"web_filename": os.path.join(SERVICE_FILENAME, PJ_NAME),
                    "service_deployment_filename": SERVICE_DEPLOYMENT_FILENAME}
    files = {'nginx': ['nginx.conf', PJ_NGINX, nginx_kwargs],
             'uwsgi': ['uwsgi.ini', PJ_UWSGI, uwsgi_kwargs],
             'other': ['nginx_access.log', 'nginx_error.log',
                       'uwsgi_params', 'websock.sock']}

    # Action: Build DEPLOYMENT_DIR
    if not os.path.isdir(DEPLOYMENT_DIR):
        commands.getstatusoutput("mkdir {}".format(DEPLOYMENT_DIR))

    # Action: Build deployment files
    for filetype, filelist in files.items():
        if filetype != 'other':
            tmpl, new_file, config_kwargs = filelist
            establish_config_file(read_file=tmpl, write_file=new_file,
                                  tmpl_kwargs=config_kwargs)
        else:
            for each_file in filelist:
                establish_config_file(read_file=each_file, write_file=each_file)


def install_web_service():
    """Copied the project to install destination"""
    # Actions: Build folder
    # Action: Build INSTALL_BASE_DIR
    if not os.path.isdir(INSTALL_BASE_DIR):
        commands.getstatusoutput("mkdir {}".format(INSTALL_BASE_DIR))
    # Action: Build SERVICE_FILENAME
    if not os.path.isdir(SERVICE_FILENAME):
        commands.getstatusoutput("cp -r {} {}".format(REPO_FILENAME, INSTALL_BASE_DIR))
    # Action: Build SERVICE_DEPLOYMENT_FILENAME
    if not os.path.isdir(SERVICE_DEPLOYMENT_FILENAME):
        commands.getstatusoutput("mkdir {}".format(SERVICE_DEPLOYMENT_FILENAME))

    # Actions: Build nginx and uwsgi
    # Action: Link uwsgi to vassals
    service_uwsgi = os.path.join(SERVICE_DEPLOYMENT_FILENAME, PJ_UWSGI)
    vassal_uwsgi = os.path.join('/etc/uwsgi/vassals/', PJ_UWSGI)
    if not os.path.islink(vassal_uwsgi):
        commands.getstatusoutput("ln -s {} {}".format(service_uwsgi, vassal_uwsgi))
    # Action: Link nginx to sites-enabled
    service_nginx = os.path.join(SERVICE_DEPLOYMENT_FILENAME, PJ_NGINX)
    site_enable_nginx = os.path.join('/etc/nginx/sites-enabled/', PJ_NGINX)
    if not os.path.islink(site_enable_nginx):
        commands.getstatusoutput("ln -s {} {}".format(service_nginx, site_enable_nginx))

def change_owner_and_mod():
    commands.getstatusoutput("chown -R www-data {}".format(INSTALL_BASE_DIR))
    commands.getstatusoutput("chmod -R 777 {}".format(INSTALL_BASE_DIR))


if __name__ == '__main__':
    # Action: Show installing message
    print "#########################################################"
    print "#Start to establish depolyment and install web service!!#"
    print "#########################################################"
    print "\n\n\n"

    # Verification: Has system installed nginx and uwsgi?
    check_list = {"nginx": "nginx -v",
                  "uwsgi": "uwsgi --version"}
    print "Start to check has system installed nginx and uwsgi?"
    for service, cmd in check_list.items():
        err_code, _ = commands.getstatusoutput(cmd)  # Ideal output: (0, 'nginx version: nginx/1.1.19')
        if err_code != 0:
            sys.exit("You haven't installed {}!!".format(service))
    print "OK! You have installed both!\n"

    # Actions: Strart to establish depolyment and install web service
    # Step 1: Copied the project to install destination
    establish_config_for_service()
    # Step 2: Copied the project to install destination
    install_web_service()
    # Step 3: change_owner_and_mod
    change_owner_and_mod()

    print "Congratulations! You have installed!"
