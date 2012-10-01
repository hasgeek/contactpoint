'''
    env
    Possible values:
        - 'development'
        - 'production'
    
    In development environment, the app will run in debug mode.
    
'''
env = 'production'

if env is 'development':
    shud_i_debug = True
elif env is 'production':
    shud_i_debug = False
