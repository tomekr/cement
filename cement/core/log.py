"""Cement methods to setup and configuring logging."""

import logging

from cement import namespaces

def setup_logging(clear_loggers=True, level=None):
    """
    Primary Cement method to setup logging.
    """
    global namespaces
    config = namespaces['global'].config

    # remove any previously setup handlers from other libraries
    if clear_loggers:
        for i in logging.getLogger().handlers:
            logging.getLogger().removeHandler(i)
        for i in logging.getLogger(config['app_module']).handlers:
            logging.getLogger(config['app_module']).removeHandler(i)
        for i in logging.getLogger('cement').handlers:
            logging.getLogger('cement').removeHandler(i)
            
    app_log = logging.getLogger(config['app_module'])
    cement_log = logging.getLogger('cement')
    
    # log level
    if config.has_key('debug') and config['debug']:
        level = 'DEBUG'
    elif level and level.upper() in ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']:
        level = level
    elif config.has_key('log_level'):
        level = config['log_level']
    else:
        level = 'INFO'

    log_level = eval("logging.%s" % level.upper())
    app_log.setLevel(log_level)
    cement_log.setLevel(log_level)
    
    # console formatter    
    console = logging.StreamHandler()
    if log_level == logging.DEBUG:
        console.setFormatter(
            logging.Formatter("%(asctime)s (%(levelname)s) %(name)s : %(message)s")
            )
    else: 
        console.setFormatter(
            logging.Formatter("%(levelname)s: %(message)s")
            )
    console.setLevel(log_level)   
    app_log.addHandler(console)    
    cement_log.addHandler(console)
    
    # file formatter
    if config.has_key('log_file'):
        if config.has_key('log_max_bytes'):
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                config['log_file'], maxBytes=int(config['log_max_bytes']), 
                backupCount=int(config['log_max_files'])
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(config['log_file'])
            
        file_handler.setFormatter( 
            logging.Formatter("%(asctime)s (%(levelname)s) %(name)s : %(message)s")
            )
        file_handler.setLevel(log_level)   
        app_log.addHandler(file_handler)
        cement_log.addHandler(file_handler)
        
def get_logger(name):
    """
    Used throughout the application to get a logger opject with a namespace
    of 'name' (should be passed as __name__).  
    
    Arguments:
    
    name => name of the module calling get_logger (use __name__).
    """
    return logging.getLogger(name)