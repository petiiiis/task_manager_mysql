from db import pripojeni_db, vytvoreni_tabulky, zobrazit_ukoly_db, odstranit_ukol_db

def main():
    conn = pripojeni_db()
    vytvoreni_tabulky(conn)

    ukoly = zobrazit_ukoly_db(conn)
    print("ÚKOLY:")
    if not ukoly:
        print("Žádné úkoly.")
        conn.close()
        return

    for u in ukoly:
        print(f"[{u['id']}] {u['nazev']} – {u['stav']}")

    ukol_id = int(input("\nZadej ID úkolu ke smazání: ").strip())
    potvrzeni = input("Opravdu smazat? (a/n): ").strip().lower()

    if potvrzeni != "a":
        print("Mazání zrušeno.")
        conn.close()
        return

    ok = odstranit_ukol_db(conn, ukol_id)
    if ok:
        print("Úkol smazán.")
    else:
        print("Takové ID neexistuje.")

    conn.close()

if __name__ == "__main__":
    main()
    