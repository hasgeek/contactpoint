from os import environ

'''
    environ['CONTACTPOINT_ENV']
    Possible values:
        - 'development'
        - 'production'
    
    In development environment, the app will run in debug mode.

    environ['PEOPLEFLOW_HOSTNAME']
    The hostname that is available from the network.
    If left empty, host2ip will not run.

    environ['REMOTE_SERVERS']
    Array containing hostnames to be controlled in the /etc/hosts
    file. If left empty, host2ip will not run.

    environ['HOST2IP_PERIOD']
    Time period(in seconds) between two host2ip calls.
    
'''
environ['CONTACTPOINT_ENV'] = 'production'
environ['PEOPLEFLOW_HOSTNAME'] = ''
environ['REMOTE_SERVERS'] = pickle.dumps([])
environ['HOST2IP_PERIOD'] = '60'