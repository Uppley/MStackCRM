from fabric.api import *


def update_upgrade():
    """
        Update the default OS installation's
        basic default tools.
    """
    run("aptitude    update")
    run("aptitude -y upgrade")


def add_swap():
    run("fallocate -l 4G /swapfile")
    run("chmod 600 /swapfile")
    run("mkswap /swapfile")
    run("swapon /swapfile")
    run("swapon -s")
    add_to_swap_files='echo "/swapfile none swap sw 0 0" >> /etc/fstab'
    add_swappiness='echo "vm.swappiness=10" >> /etc/sysctl.conf'
    add_cache_pressure='echo "vm.vfs_cache_pressure=50" >> /etc/sysctl.conf'
    run(add_to_swap_files)
    run(add_swappiness)
    run(add_cache_pressure)

def block_xmlrpc():
    run("a2enconf block-xmlrpc")
    run("service apache2 restart")

def wordpress_cli_add():
    with cd("/tmp"):
        run("curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar")
        run("chmod +x wp-cli.phar")
        run("mv wp-cli.phar /usr/local/bin/wp")

    with cd("/var/www/html"):
        run("ls -l")

def create_user_alfred():
    run("useradd -m -p theRealBM! -s /bin/bash alfred")
    run("usermod -aG sudo alfred")


def wordpress_and_add():
    update_upgrade()
    add_swap()
    block_xmlrpc()
    wordpress_cli_add()
    create_user_alfred()


# Change the type as well either cli or main
# be able to change key name
def run_wordpress_commands(hostip, host_username):
    host = "{0}@{1}".format(host_username,hostip)
    print "{0}".format(host)
    execute(wordpress_and_add, hosts=[host]) # -- for sudo commands send in env.password = '****'


def run_wordpress_cli(plugin_set_name):
    if isinstance(plugin_set_name, str):
        print "This is a string"
    else:
        print "It's not a string, don't return a success"



def get_set(name):
    return {
        'normal': ["List of programs go here"]
    }.get(name, )
