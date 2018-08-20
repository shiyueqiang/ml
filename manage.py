# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: manage.py
@time: 2017/11/12 下午1:20
@desc:
"""

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if os.path.exists('.env'):
    print ('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from flask_script import Manager, Shell
from flask import url_for

app = create_app(os.getenv('FLASK_CONFIG') or 'default.cfg')
manager = Manager(app)



def make_shell_context():

    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def deploy():
    """Run deployment tasks."""
    pass


@manager.command
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        # line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        # output.append(line)
        output.append(url)

    for line in sorted(output):
        print (line)


if __name__ == '__main__':
    manager.run()
