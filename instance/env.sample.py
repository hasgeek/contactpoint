from os import environ

'''
    environ['CONTACTPOINT_ENV']
    Possible values:
        - 'development'
        - 'production'
    
    In development environment, the app will run in debug mode.
    
'''
environ['CONTACTPOINT_ENV'] = 'production'