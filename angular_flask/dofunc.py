import digitalocean
import angular_flask.fabcomm as fab
import angular_flask
"""
    I now realize that this function should exist entirely within a celery task.
    When the entire function is complete we could then find the results based on the task_id

    Pseudo-code:
        API Call: /create_wp_server
            Activate activation script w/Celery

"""


def size_calculator(size):
    size_dict = {
        0.5: "512mb",
        1: "1gb",
        2: "2gb",
        4: "4gb"
    }
    return size_dict[size]

def ssh_key_by_name(name):
    manager = digitalocean.Manager(token="cac1137032098f4d06627bd8744fc0bc1f7cb3102c72e16678146072674f40fd")
    ssh_keys = manager.get_all_sshkeys()

    needed_key_list = [] # needed key is the key that

    for value in ssh_keys:
        if(value.name == name):
            needed_key_list.append(value.id)
        if(value.name == "Thinkpad"):
            needed_key_list.append(value.id)
        if("blanxis_client" in value.name):
            needed_key_list.append(value.id)
        if("blanxis_server" in value.name):
            needed_key_list.append(value.id)
    return needed_key_list


def create_droplet(main_ssh_key_name, name, size=1):

    # Create a new wordpress droplet
    droplet = digitalocean.Droplet(token="cac1137032098f4d06627bd8744fc0bc1f7cb3102c72e16678146072674f40fd",
                                   name=name,
                                   region='nyc2', # New York 2 (cloest to East Coast)
                                   image='wordpress', # Wordpress with Ubuntu 14.04 x64
                                   size_slug=size_calculator(size),
                                   ssh_keys=ssh_key_by_name(main_ssh_key_name),
                                   backups=True)
    droplet.create()
    return droplet


def installation_completion(checkdroplet):
    drop_id = checkdroplet.id
    is_incomplete = True
    isError=False
    current_droplet=None
    while is_incomplete == True:
        d_actions = digitalocean.Droplet(token="cac1137032098f4d06627bd8744fc0bc1f7cb3102c72e16678146072674f40fd",
                            id=drop_id
                            ).get_actions()
        for action in d_actions:
            action.load()
            print action.status
            if(action.status == 'completed' or  action.status == 'errored'):
                is_incomplete = False
                current_droplet = digitalocean.Droplet(
                                    token="cac1137032098f4d06627bd8744fc0bc1f7cb3102c72e16678146072674f40fd",
                                    id=drop_id
                                )
                if(action.status == 'errored'):
                    isError=True

    return {'isError': isError, 'droplet': current_droplet}

# Celery for long running task
def create_wordpress(name, company_name, ssh_key):
    # Mock steps
    # Create droplet -- DONE
    droplet = create_droplet(ssh_key, name)
    # Check for installation completion -- DOING
    try:
        completed_drop = installation_completion(droplet)
    except Exception as e:
        print e.message
    # Add droplet ip address to host list -- DOING

    droplet_obj = completed_drop['droplet'].load()
    # print droplet_obj.ip_address
    # Send fabric commands to host -- DOING -- DONE with
    if completed_drop['isError'] == False:
        fab.run_wordpress_commands(droplet_obj.ip_address, "root")
    # Add database information here -- TODO
    newServer = angular_flask.models.Server(droplet.name, company_name, droplet_obj.ip_address, droplet_obj.id)
    # Must add here
    db = angular_flask.models.db
    angular_flask.models.db.session.add(newServer)
    angular_flask.models.db.session.commit()




# Save the id inside of a variable

# droplet.create()
#
# print droplet.id

# Every 30 seconds check to see of the drop
# actions = droplet.get_actions()
# for action in actions:
#     action.load()
#     # Once it shows complete, droplet is up and running
#     print action.status
