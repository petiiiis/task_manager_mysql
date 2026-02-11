import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def pripojeni_db(db_name=DB_NAME):
    """
    Vytvoří a vrátí připojení k MySQL databázi
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=db_name
        )
        return connection
    except Error as e:
        raise RuntimeError(f"Chyba připojení k DB: {e}")
import mysql.connector
from mysql.connector import Error

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def pripojeni_db(db_name=DB_NAME):
    """Vytvoří a vrátí připojení k MySQL databázi."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=db_name
        )
        return connection
    except Error as e:
        raise RuntimeError(f"Chyba připojení k DB: {e}")


def vytvoreni_tabulky(conn):
    """Vytvoří tabulku ukoly, pokud neexistuje."""
    sql = """
    CREATE TABLE IF NOT EXISTS ukoly (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nazev VARCHAR(255) NOT NULL,
      popis TEXT NOT NULL,
      stav ENUM('Nezahájeno','Probíhá','Hotovo') NOT NULL DEFAULT 'Nezahájeno',
      datum_vytvoreni TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()

def pridat_ukol_db(conn, nazev: str, popis: str) -> int:
    nazev = (nazev or "").strip()
    popis = (popis or "").strip()

    if not nazev:
        raise ValueError("Název je povinný.")
    if not popis:
        raise ValueError("Popis je povinný.")

    sql = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
    cur = conn.cursor()
    cur.execute(sql, (nazev, popis))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    return int(new_id)

def zobrazit_ukoly_db(conn):
    sql = """
    SELECT id, nazev, popis, stav
    FROM ukoly
    WHERE stav IN ('Nezahájeno', 'Probíhá')
    ORDER BY datum_vytvoreni DESC, id DESC
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return rows

def aktualizovat_stav_ukolu_db(conn, ukol_id: int, novy_stav: str) -> bool:
    povolene = {"Probíhá", "Hotovo"}
    if novy_stav not in povolene:
        raise ValueError("Neplatný stav. Povolené: Probíhá / Hotovo.")

    cur = conn.cursor()
    cur.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
    exists = cur.fetchone()
    if not exists:
        cur.close()
        return False

    cur.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, ukol_id))
    conn.commit()
    cur.close()
    return True

def odstranit_ukol_db(conn, ukol_id: int) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
    exists = cur.fetchone()
    if not exists:
        cur.close()
        return False

    cur.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
    conn.commit()
    cur.close()
    return True
