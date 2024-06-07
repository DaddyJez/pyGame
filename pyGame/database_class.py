import sqlite3


class DatabaseManager:
    def __init__(self, database):
        self.db = sqlite3.connect(database)
        self.logger = self.Logger()

    class Logger:
        def log(self, message):
            print(message)

    def write_score(self, nick, score_to_insert):
        cur = self.db.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS users
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nickname TEXT,
                        score INTEGER)''')

        cur.execute('SELECT score FROM users WHERE nickname = ?', (nick,))
        previous_score = cur.fetchone()

        if previous_score is None:
            cur.execute('INSERT INTO users (nickname, score) VALUES (?, ?)', (nick, score_to_insert))
        elif score_to_insert > previous_score[0]:
            cur.execute('UPDATE users SET score = ? WHERE nickname = ?', (score_to_insert, nick))

        self.db.commit()

    def get_top_players(self):
        cur = self.db.cursor()

        query = 'SELECT nickname, score FROM users ORDER BY score DESC LIMIT 5'

        cur.execute(query)
        top_players_list = cur.fetchall()

        self.logger.log("Retrieved top players from the database.")
        self.logger.log(top_players_list)

        self.db.commit()

        return top_players_list

    def close(self):
        self.db.commit()
        self.db.close()
        self.logger.log("Closed the database connection.")
