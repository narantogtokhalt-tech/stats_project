try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # pymysql байхгүй (жишээ нь Render дээр) үед алдаа гаргахгүй алгасана
    pass