from configs import config
from internal import database


def create_table():
    cursor = database.Database().connect()
    db = "ALTER DATABASE {} charset=utf8;".format(config.database)
    cursor.execute(db)

    create_table = """
        CREATE TABLE `Users` (
            `user_id` INT NOT NULL,
            `type_account` VARCHAR(6) NOT NULL DEFAULT 'User',
            `timezone` VARCHAR(3) NOT NULL,
            `group_id` VARCHAR(255),
            PRIMARY KEY (`user_id`)
        );
    """
    if cursor.execute(create_table):
        print('Table creation error "Users", try again!')
        return
    else:
        print('ОК')
        create_table = """
            CREATE TABLE `Groups` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `group_name` VARCHAR(255) NOT NULL,
                `group_timezone` VARCHAR(3) NOT NULL,
                `creator` INT NOT NULL,
                PRIMARY KEY (`id`)
            );
        """
        if cursor.execute(create_table):
            print('Table creation error "Groups", try again!')
            return
        else:
            print('OK')
            database.Database().conn.commit()

if __name__ == "__main__":
    create_table()