import sqlite3
from datetime import datetime

import settings

connection = sqlite3.connect(settings.db_name)

with open(f"dump{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.sql", "w") as f:
    f.write("".join(line + "\n" for line in connection.iterdump()))