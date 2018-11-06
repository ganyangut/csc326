#static variables
class StaticVar():
    database_file = 'persistent_storage.db'
    SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
    REDIRECT_URI = 'http://localhost:8081/redirect'
    sessions_opts = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './data',
        'session.auto': True
    }
