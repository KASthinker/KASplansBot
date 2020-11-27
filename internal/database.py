import mysql.connector
import copy
from configs import config
from internal import methods

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
class Database(metaclass=MetaSingleton):
    conn = None
    def connect(self):
        if self.conn is None:
            self.conn = mysql.connector.connect(
                            user = config.user,
                            password = config.password,
                            host = config.host,
                            database = config.database,
                            auth_plugin='mysql_native_password'
                        )
        return self.conn.cursor()

    def if_user_exists(self, user_id):
        cursor = self.connect()
        cursor.execute("SHOW TABLES LIKE '{}';".format(user_id))
        tables = cursor.fetchall()
        if len(tables):    
            return True
        else:   
            return False

    def add_new_user(self, user_id, timezone):
        cursor = self.connect()
        add_table = """
            CREATE TABLE `{}` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `type_task` VARCHAR(15) NOT NULL,
                `text` VARCHAR(255) NOT NULL,
                `date` DATE,
                `time` TIME NOT NULL,
                `weekday` VARCHAR(70),
                `priority` VARCHAR(20) NOT NULL,
                PRIMARY KEY (`id`)
            ); 
        """.format(user_id)
        if cursor.execute(add_table):
            return False
        else:
            add_from_users = """
                INSERT INTO `Users` (user_id, timezone) 
                VALUES ({}, {});
            """.format(user_id, str(timezone))
            if cursor.execute(add_from_users):
                return False
            else:
                self.conn.commit()
                return True

    def delete_user_account(self, user_id):
        cursor = self.connect()
        cursor.execute("SET SQL_SAFE_UPDATES=0;")
        del_from_users = """
            DELETE FROM Users WHERE user_id = {};
        """.format(str(user_id))
        if cursor.execute(del_from_users):
            self.delete_user_account(user_id)
        else:
            drop_table = """
                DROP TABLE `{}`;
            """.format(str(user_id))
            if cursor.execute(drop_table):
                self.delete_user_account(user_id)
            else:
                cursor.execute("SET SQL_SAFE_UPDATES=1;")
                self.conn.commit()





"""
CREATE TABLE `Users` (
	`user_id` INT NOT NULL,
	`type_account` VARCHAR(255) NOT NULL DEFAULT 'User',
	`timezone` VARCHAR(255) NOT NULL,
	`group_id` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`user_id`)
);

CREATE TABLE `user_id` (
	`id` BINARY NOT NULL AUTO_INCREMENT,
	`type_task` VARCHAR(255) NOT NULL,
	`text` VARCHAR(255) NOT NULL,
	`date` DATE NOT NULL,
	`time` TIME NOT NULL,
	`weekday` VARCHAR(255) NOT NULL,
	`priority` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `group_name` (
	`user_id` INT NOT NULL,
	`access level` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`user_id`)
);

CREATE TABLE `Groups` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`group_name` VARCHAR(255) NOT NULL,
	`group_timezone` VARCHAR(255) NOT NULL,
	`creator` INT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `gpoup_task_N` (

);


"""