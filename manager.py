from flask_script import Manager

from flask_migrate import Migrate, MigrateCommand

from exts import db

from main import app

import models

manager=Manager(app)

Migrate(app, db)

# 第一次运行项目前，请在终端进入项目的虚拟环境下:
# 运行命令1: python manager.py db init
# 运行命令2: python manager.py db migrate
# 运行命令3: python manager.py db upgrade
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()