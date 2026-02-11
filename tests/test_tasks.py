import pytest
from config import TEST_DB_NAME
from db import (
    pripojeni_db,
    vytvoreni_tabulky,
    pridat_ukol_db,
    aktualizovat_stav_ukolu_db,
    odstranit_ukol_db,
)


@pytest.fixture
def conn():
    connection = pripojeni_db(db_name=TEST_DB_NAME)
    vytvoreni_tabulky(connection)
    yield connection
    connection.close()


def _create_task(conn, nazev="Test úkol", popis="Test popis"):
    ukol_id = pridat_ukol_db(conn, nazev, popis)
    assert ukol_id is not None
    return ukol_id


def _delete_task_direct(conn, ukol_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
    conn.commit()
    cur.close()


#         PRIDAT UKOL

def test_pridat_ukol_pozitivni(conn):
    ukol_id = pridat_ukol_db(conn, "Test úkol", "Testovací popis")
    assert ukol_id is not None
    _delete_task_direct(conn, ukol_id)


def test_pridat_ukol_negativni_prazdny_nazev(conn):
    try:
        result = pridat_ukol_db(conn, "", "nějaký popis")
        assert not result
    except ValueError:
        assert True


#       AKTUALIZOVAT STAV 

def test_aktualizovat_stav_pozitivni(conn):
    ukol_id = _create_task(conn, "Update test", "popis")

    ok = aktualizovat_stav_ukolu_db(conn, ukol_id, "Probíhá")
    assert ok is True or ok == 1

    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    row = cur.fetchone()
    cur.close()

    assert row is not None
    assert row["stav"] == "Probíhá"

    _delete_task_direct(conn, ukol_id)


def test_aktualizovat_stav_negativni_neexistujici_id(conn):
    ok = aktualizovat_stav_ukolu_db(conn, 999999999, "Hotovo")
    assert not ok


#      ODSTRANIT UKOL 

def test_odstranit_ukol_pozitivni(conn):
    ukol_id = _create_task(conn, "Delete test", "popis")

    ok = odstranit_ukol_db(conn, ukol_id)
    assert ok is True or ok == 1

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM ukoly WHERE id = %s", (ukol_id,))
    count = cur.fetchone()[0]
    cur.close()

    assert count == 0


def test_odstranit_ukol_negativni_neexistujici_id(conn):
    ok = odstranit_ukol_db(conn, 999999999)
    assert not ok