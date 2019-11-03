

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'db_handler': {
            'level': 'INFO',
            'class': 'app.log_handler.LogDBHandler',
        }
    },
    'loggers': {
        'RequestLogger': {
            'handlers': ['db_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
