import sqlite3

verbindung = sqlite3.connect("campaign_wiki.db")
verbindung.execute("PRAGMA foreign_keys = ON")
cursor = verbindung.cursor()


#Tabellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS factions (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    faction_type TEXT,
    description TEXT,
    notes TEXT
);
""")
verbindung.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS NPCs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    faction_id INTEGER,
    description TEXT,
    notes TEXT,
    FOREIGN KEY (faction_id) REFERENCES factions(id) ON DELETE SET NULL
);
""")
verbindung.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS PCs(
    id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    race TEXT,
    backstory TEXT,
    equipment TEXT,
    notes TEXT
);
""")
verbindung.commit()



cursor.execute("""
CREATE TABLE IF NOT EXISTS Quests (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    description TEXT,
    notes TEXT
);
""")
verbindung.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Locations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    description TEXT,
    notes TEXT
);
""")
verbindung.commit()

#beziehungs - Tabelle quests + locations
cursor.execute("""
CREATE TABLE IF NOT EXISTS quest_location (
    quest_id INTEGER,
    location_id INTEGER,

    PRIMARY KEY (quest_id, location_id),

    FOREIGN KEY (quest_id)
        REFERENCES quests(id)
        ON DELETE CASCADE,

    FOREIGN KEY (location_id)
        REFERENCES locations(id)
        ON DELETE CASCADE
);
""")

verbindung.commit()



def show_database():
    cursor.execute("""
    SELECT *
    FROM NPCs
    """)

    npcs = cursor.fetchall()

    for npc in npcs:
        print(npc)


#NPCs Funktionen
def add_npc():
    name = input("What is the NPC called?")
    role = input("What is the NPCs profession?")
    faction_name = input("What faction does the NPC belong to? (leave empty for none)")

    if faction_name == "":
        faction_id = None

    else:
        cursor.execute("""
          SELECT id
          FROM factions
          WHERE name = ?
          """, (faction_name,))

        faction = cursor.fetchone()

        if faction:
            faction_id = faction[0]

        else:
            print("Faction not found.")
            create_faction = input("Would you like to create it? (y/n) ")

            if create_faction == "y":
                faction_id = add_faction()
            else:
                print("NPC creation cancelled.")
                return

    description = input("What is the NPCs description?")
    notes = input("What notes do you have?")

    cursor.execute("""
    INSERT INTO NPCs
    (name, role, faction_id, description, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (name, role, faction_id, description, notes))

    verbindung.commit()
    print("npc added.")

def show_npc(npc):
    faction_id = npc[3]

    if faction_id:
        cursor.execute("""
           SELECT name
           FROM factions
           WHERE id = ?
           """, (faction_id,))

        faction = cursor.fetchone()
        faction_name = faction[0]
    else:
        faction_name = "None"


    print("ID:", npc[0])
    print("name:", npc[1])
    print("role:", npc[2])
    print("faction:", faction_name)
    print("description:", npc[4])
    print("notes:", npc[5])

def show_npcs():
    cursor.execute("""
    SELECT *
    FROM NPCs
    """)

    npcs = cursor.fetchall()

    for npc in npcs:
        show_npc(npc)

def search_npc():
    npc_name_from_user = input("Which NPC are you looking for?")
    search_npcs_by_name(npc_name_from_user)


def search_npcs_by_name(name_to_search):
    cursor.execute("""
    SELECT *
    FROM NPCs
    WHERE name = ?
    """, (name_to_search,))

    npcs = cursor.fetchall()

    if npcs:
        for npc in npcs:
            show_npc(npc)
        return npcs  #WHYYY
    else:
        print("NPC not found.")
        return None


def delete_npc():
    search_name = input("Which NPC do you want to delete?")
    found_npcs = search_npcs_by_name(search_name)

    if found_npcs:
        npc_id = int(input("Which NPC ID do you want to delete? "))
        confirm = input("Are you sure? (y/n)")

        if confirm == "y":

            cursor.execute("""
                DELETE FROM NPCs
                WHERE id = ?
                """, (npc_id,))

            verbindung.commit()

            if cursor.rowcount > 0:
                print("NPC deleted.")
            else:
                print("NPC not found.") #WHY


        elif confirm  == "n":
            print("Deletion cancelled.")

        else:
            print("Invalid input.")

    else:
        return


def update_npc():
    search_name = input("Which NPC do you want to update?")
    found_npcs = search_npcs_by_name(search_name)

    if found_npcs:
        npc_id = int(input("Which NPC ID do you want to update? "))

        print("1. name")
        print("2. role")
        print("3. faction")
        print("4. description")
        print("5. notes")

        choice = input("What would you like to update? ")


        if choice == "1":
            new_name = input("What is the NPCs new name?")
            cursor.execute("""
            UPDATE NPCs
            SET name = ?
            WHERE id = ?
            """, (new_name, npc_id))


        elif choice == "2":
            new_role = input("What is the NPCs new role?")
            cursor.execute("""
            UPDATE NPCs
            SET role = ?
            WHERE id = ?
            """, (new_role, npc_id))



        elif choice == "3":
            faction_name = input("What faction does the NPC belong to? (leave empty for none) ")

            if faction_name == "":
                faction_id = None

            else:
                cursor.execute("""
                SELECT id
                FROM factions
                WHERE name = ?
                """, (faction_name,))

                faction = cursor.fetchone()

                if faction:
                    faction_id = faction[0]

                else:
                    print("Faction not found.")
                    create_faction = input("Would you like to create it? (y/n) ")

                    if create_faction == "y":
                        faction_id = add_faction()

                        if faction_id is None:
                            print("Faction update cancelled.")
                            return

                    else:
                        print("Faction update cancelled.")
                        return

            cursor.execute("""
            UPDATE NPCs
            SET faction_id = ?
            WHERE id = ?
            """, (faction_id, npc_id))


        elif choice == "4":
            new_description = input("What is the NPCs new description?")
            cursor.execute("""
            UPDATE NPCs
            SET description = ?
            WHERE id = ?
            """, (new_description, npc_id))


        elif choice == "5":
            new_notes = input("What are the NPCs new notes?")
            cursor.execute("""
            UPDATE NPCs
            SET notes = ?
            WHERE id = ?
            """, (new_notes, npc_id))

        else:
            print("Invalid input.")
            return

        verbindung.commit()

        if cursor.rowcount > 0:
            print("NPC updated successfully.")

    else:
        return #WHYYY


def add_pc():
    name = input("What is the PCs called?")
    role = input("What is the PCs role(class)?")
    race = input("What is the PCs race?")
    backstory = input("What is the PCs backstory?")
    equipment = input("What is the PCs equipment?")
    notes = input("What notes do you have?")

    cursor.execute("""
    INSERT INTO PCs
    (name, role, race, backstory, equipment, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, role, race, backstory, equipment, notes))

    verbindung.commit()


def show_pc(pc):
    print("ID:", pc[0])
    print("name:", pc[1])
    print("role:", pc[2])
    print("race:", pc[3])
    print("backstory:", pc[4])
    print("equipment:", pc[5])
    print("notes:", pc[6])

def show_pcs():
    cursor.execute("""
    SELECT *
    FROM PCs
    """)
    pcs = cursor.fetchall()

    for pc in pcs:
        show_pc(pc)


def search_pc():
    pc_name_from_user = input("Which PC are you looking for?")
    search_pcs_by_name(pc_name_from_user)

def search_pcs_by_name(name_to_search):
    cursor.execute("""
    SELECT *
    FROM PCs
    WHERE name = ?
    """, (name_to_search,))

    pcs = cursor.fetchall()

    if pcs:
        for pc in pcs:
            show_pc(pc)
        return pcs
    else:
        print("PC not found.")
        return None


def delete_pc():
    search_name = input("Which PC do you want to delete?")
    found_pcs = search_pcs_by_name(search_name)

    if found_pcs:
        pc_id = int(input("Which PC ID do you want to delete?"))
        confirm = input("Are you sure? (y/n)")

        if confirm == "y":

            cursor.execute("""
                DELETE FROM PCs
                WHERE id = ?
                """, (pc_id,))

            verbindung.commit()

            if cursor.rowcount > 0:
                print("PC deleted.")
            else:
                print("PC not found.")

        elif confirm == "n":
            print("Deletion cancelled.")

        else:
            print("Invalid input.")

    else:
        return


#PCs Funktionen
def update_pc():
    search_name = input("Which PC do you want to update?")
    found_pcs = search_pcs_by_name(search_name)

    if found_pcs:
        pc_id = int(input("Which PC ID do you want to update?"))

        print("1. name")
        print("2. role")
        print("3. race")
        print("4. backstory")
        print("5. equipment")
        print("6. notes")

        choice = input("What would you like to update?")

        if choice == "1":
            new_name = input("What is the PCs new name?")
            cursor.execute("""
            UPDATE PCs
            SET name = ?
            WHERE id = ?
            """, (new_name, pc_id))

        elif choice == "2":
            new_role = input("What is the PCs new role?")
            cursor.execute("""
            UPDATE PCs
            SET role = ?
            WHERE id = ?
            """, (new_role, pc_id))

        elif choice == "3":
            new_race = input("What is the PCs new race?")
            cursor.execute("""
            UPDATE PCs
            SET race = ?
            WHERE id = ?
            """, (new_race, pc_id))

        elif choice == "4":
            new_backstory = input("What is the PCs new backstory?")
            cursor.execute("""
            UPDATE PCs
            SET backstory = ?
            WHERE id = ?
            """, (new_backstory, pc_id))

        elif choice == "5":
            new_equipment = input("What is the PCs new equipment?")
            cursor.execute("""
            UPDATE PCs
            SET equipment = ?
            WHERE id = ?
            """, (new_equipment, pc_id))

        elif choice == "6":
            new_notes = input("What are the new notes?")
            cursor.execute("""
            UPDATE PCs
            SET notes = ?
            WHERE id = ?
            """, (new_notes, pc_id))

        else:
            print("Invalid input.")
            return

        verbindung.commit()

        if cursor.rowcount > 0:
            print("PC updated successfully.")

        else:
            return


#Factions Funktionen
def add_faction():
    name = input("What is the faction's name? ")

    cursor.execute("""
    SELECT id
    FROM factions
    WHERE name = ?
    """, (name,))

    existing_faction = cursor.fetchone()

    if existing_faction:
        print("A faction with this name already exists, please choose another one.")
        return

    faction_type = input("What is the faction type? ")
    description = input("What is the faction's description? ")
    notes = input("What are the faction's notes? ")

    cursor.execute("""
    INSERT INTO factions
    (name, faction_type, description, notes)
    VALUES (?, ?, ?, ?)
    """, (name, faction_type, description, notes))

    verbindung.commit()

    return cursor.lastrowid

print("faction added.")

def show_faction(faction):
    print("ID:", faction[0])
    print("name:", faction[1])
    print("type:", faction[2])
    print("description:", faction[3])
    print("notes:", faction[4])

def show_factions():
    cursor.execute("""
    SELECT *
    FROM factions
    """)

    factions = cursor.fetchall()

    for faction in factions:
        show_faction(faction)


def search_faction():
    search_name = input("What faction are you looking for?")
    search_factions_by_name(search_name)

def search_factions_by_name(search_name):
    cursor.execute("""
    SELECT *
    FROM factions
    WHERE name = ?
    """, (search_name,))

    factions = cursor.fetchall()

    if factions:
        for faction in factions:
            show_faction(faction)
        return factions
    else:
        print("Faction not found.")
        return None

def delete_faction():
    search_name = input("Which faction do you want to delete?")
    found_factions = search_factions_by_name(search_name)


    if found_factions:
        faction_id = int(input("Which faction ID do you want to delete?"))
        confirm = input("Are you sure? (y/n)")

        if confirm == "y":
            cursor.execute("""
                DELETE FROM factions
                WHERE id = ?
                """, (faction_id,))

            verbindung.commit()

            if cursor.rowcount > 0:
                print("Faction deleted.")
            else:
                print("Faction not found.")

        elif confirm == "n":
            print("Deletion cancelled.")

        else:
            print("Invalid input.")

    else:
        return


def update_faction():
    search_name = input("Which faction do you want to update?")
    found_factions = search_factions_by_name(search_name)

    if found_factions:
        faction_id = int(input("Which faction ID do you want to update?"))

        print("1. name")
        print("2. type")
        print("3. description")
        print("4. notes")

        choice = input("What would you like to edit?")

        if choice == "1":
            new_name = input("What is the new name?")
            cursor.execute("""
            UPDATE factions
            SET name = ?
            WHERE id = ?
            """, (new_name, faction_id))

        elif choice == "2":
            new_type = input("What is the factions new role?")
            cursor.execute("""
                UPDATE factions
                SET faction_type = ?
                WHERE id = ?
                """, (new_type, faction_id))


        elif choice == "3":
            new_description = input("What is the factions new descriptiom?")
            cursor.execute("""
                UPDATE factions
                SET description = ?
                WHERE id = ?
                """, (new_description, faction_id))


        elif choice == "4":
            new_notes = input("What is the NPCs new description?")
            cursor.execute("""
                UPDATE factions
                SET notes = ?
                WHERE id = ?
                """, (new_notes, faction_id))


        else:
            print("Invalid input.")
            return

        verbindung.commit()

        if cursor.rowcount > 0:
            print("faction updated successfully.")

    else:
        return

#Quests Funktionen
def add_quest():
    name = input("What is the quests name?")
    type = input("What is the quests type? (e.g. mainquest, sidequest)")
    description = input("What is the quests description?")
    notes = input("What are the quests notes?")

    cursor.execute("""
    INSERT INTO Quests
    (name, type, description, notes)
    VALUES (?, ?, ?, ?)
    """, (name, type, description, notes))
    verbindung.commit()

def show_quest(quest):
    print("ID:", quest[0])
    print("name:", quest[1])
    print("type:", quest[2])
    print("description:", quest[3])
    print("notes:", quest[4])

def show_quests():
    cursor.execute("""
    SELECT *
    FROM Quests
    """)

    quests = cursor.fetchall()
    for quest in quests:
        show_quest(quest)

def search_quest():
    quest_name_from_user = input("Which quest are your searching for?")
    search_quests_by_name(quest_name_from_user)

def search_quests_by_name(name_to_search):
    cursor.execute("""
    SELECT *
    FROM Quests
    WHERE name = ?
    """, (name_to_search,))

    quests = cursor.fetchall()

    if quests:
        for quest in quests:
            show_quest(quest)
        return quests
    else:
        print("Quest not found.")
        return None

def delete_quest():
    search_quest = input("Which quest do you want to delete?")
    found_quests = search_quests_by_name(search_quest)

    if found_quests:
        quest_id = int(input("Which quest ID do you want to delete?"))
        confirm = input("Are you sure? (y/n)")

        if confirm == "y":
            cursor.execute("""
            DELETE FROM Quests
            WHERE id = ?
            """, (quest_id,))

            verbindung.commit()

            if cursor.rowcount > 0:
                print("Quest deleted.")
            else:
                print("Quest not found.")

        elif confirm == "n":
            print("Deletion cancelled.")

        else:
            print("Invalid input.")

    else:
        return

def update_quest():
    search_quest = input("Which quest do you want to update?")
    found_quests = search_quests_by_name(search_quest)

    if found_quests:
        quest_id = int(input("Which quest ID do you want to edit"))

        print("1. name")
        print("2. type")
        print("3. description")
        print("4. notes")

        choice = input("What would you like to edit?")

        if choice == "1":
            new_name = input("What is the new quest name?")
            cursor.execute("""
            UPDATE Quests
            SET name = ?
            WHERE id = ?
            """, (new_name, quest_id))

        elif choice == "2":
            new_type = input("What is the new quest type?")
            cursor.execute("""
            UPDATE Quests
            SET type = ?
            WHERE id = ?
            """, (new_type, quest_id))

        elif choice == "3":
            new_description = input("What is the new quest description?")
            cursor.execute("""
            UPDATE Quests
            SET description = ?
            WHERE id = ?
            """, (new_description, quest_id))

        elif choice == "4":
            new_notes = input("What are the new quest notes?")
            cursor.execute("""
            UPDATE Quests
            SET notes = ?
            WHERE id = ?
            """, (new_notes, quest_id))

        else:
            print("Invalid input.")
            return

        verbindung.commit()

        if cursor.rowcount > 0:
            print("Quest updated successfully.")

    else:
        return


def add_location():
    name = input("What is the location called?")
    type = input("What is the type of location?")
    description = input("What is the description?")
    notes = input("What are the notes?")

    cursor.execute("""
    INSERT INTO Locations
    (name, type, description, notes)
    VALUES (?,?,?,?)
    """, (name, type, description, notes))

    verbindung.commit()

#Locations Funktionen
def show_location(location):
    print("ID:", location[0])
    print("Name:", location[1])
    print("Type:", location[2])
    print("Description:", location[3])
    print("Notes:", location[4])


def show_locations():
    cursor.execute("""
    SELECT *
    FROM Locations
    """)

    locations = cursor.fetchall()

    for location in locations:
        show_location(location)


def search_location():
    search_name = input("What location are you searching for?")
    search_locations_by_name(search_name)


def search_locations_by_name(search_name):
    cursor.execute("""
    SELECT *
    FROM Locations 
    WHERE name = ?
    """, (search_name,))

    locations = cursor.fetchall()

    if locations:
        for location in locations:
            show_location(location)
        return locations

    else:
        print("Location not found.")
        return None


def delete_location():
    search_name = input("What location do you want to delete?")
    found_locations = search_locations_by_name(search_name)

    if found_locations:
        location_id = int(input("Which location ID do you want to delete?"))
        confirm = input("Are you sure? (y/n)")

        if confirm == "y":

            cursor.execute("""
            DELETE FROM Locations
            WHERE id = ?
            """, (location_id,))

            verbindung.commit()

            if cursor.rowcount > 0:
                print("Location deleted.")
            else:
                print("Location not found.")


        elif confirm == "n":
            print("Deletion cancelled.")

        else:
            print("Invalid input.")

    else:
        return


def update_location():
    search_name = input("What location do you want to update?")
    found_locations = search_locations_by_name(search_name)

    if found_locations:
        location_id = int(input("Which location ID do you want to edit?"))

        print("1. Name")
        print("2. Type")
        print("3. Description")
        print("4. Notes")

        choice = input("What would you like to edit?")

        if choice == "1":
            new_name = input("What is the locations new name?")
            cursor.execute("""
            UPDATE Locations
            SET name = ?
            WHERE id = ?
            """, (new_name, location_id))

        elif choice == "2":
            new_type = input("What is the locations new type?")
            cursor.execute("""
            UPDATE Locations
            SET type = ?
            WHERE id = ?
            """, (new_type, location_id))

        elif choice == "3":
            new_description = input("What is the locations new description?")
            cursor.execute("""
            UPDATE Locations
            SET description = ?
            WHERE id = ?
            """, (new_description, location_id))

        elif choice == "4":
            new_notes = input("What are the locations new notes?")
            cursor.execute("""
            UPDATE Locations
            SET notes = ?
            WHERE id = ?
            """, (new_notes, location_id))

        else:
            print("Invalid input.")
            return

        verbindung.commit()

        if cursor.rowcount > 0:
            print("Location updated successfully.")

    else:
        return


#Untermenüs Funktionen
def npc_menu():
    while True:
        print("\n=== NPC menu ===")
        print("1. Add NPC")
        print("2. Show NPCs")
        print("3. Search for NPCs")
        print("4. Update NPC")
        print("5. Delete NPC")
        print("6. Return to main menu")

        choice = input("What would you like to do? ")

        if choice == "1":
            add_npc()

        elif choice == "2":
            show_npcs()

        elif choice == "3":
            search_npc()

        elif choice == "4":
            update_npc()

        elif choice == "5":
            delete_npc()

        elif choice == "6":
            break

        else:
            print("invalid input.")

def pc_menu():
    while True:
        print("\n=== PC menu ===")
        print("1. add PC")
        print("2. show PCs")
        print("3. search for PCs")
        print("4. update PC")
        print("5. delete PC")
        print("6. Return to main menu")

        choice = input("What would you like to do?")

        if choice == "1":
            add_pc()

        elif choice == "2":
            show_pcs()

        elif choice == "3":
            search_pc()

        elif choice == "4":
            update_pc()

        elif choice == "5":
            delete_pc()

        elif choice == "6":
            break

        else:
            print("Invalid input.")

def faction_menu():
    while True:
        print("\n=== Faction menu ===")
        print("1. Add faction")
        print("2. Show factions")
        print("3. Search for factions")
        print("4. Update faction")
        print("5. Delete faction")
        print("6. Return to main menu")

        choice = input("What would you like to do? ")

        if choice == "1":
            add_faction()

        elif choice == "2":
            show_factions()

        elif choice == "3":
            search_faction()

        elif choice == "4":
            update_faction()

        elif choice == "5":
            delete_faction()

        elif choice == "6":
            break

        else:
            print("invalid input!")

def quest_menu():
    while True:
        print("\n=== Quest menu ===")
        print("1. Add Quest")
        print("2. Show Quests")
        print("3. Search for Quests")
        print("4. Update Quest")
        print("5. Delete Quest")
        print("6. Return to main menu")

        choice = input("What would you like to do?")

        if choice == "1":
            add_quest()

        elif choice == "2":
            show_quests()

        elif choice == "3":
            search_quest()

        elif choice == "4":
            update_quest()

        elif choice == "5":
            delete_quest()

        elif choice == "6":
            break

        else:
            print("Invalid input.")


def location_menu():
    while True:
        print("\n=== Locations menu ===")
        print("1. Add location")
        print("2. Show locations")
        print("3. Search for locations")
        print("4. Update locations")
        print("5. Delete locations")
        print("6. Return to main menu")

        choice = input("What would you like to do? ")

        if choice == "1":
            add_location()

        elif choice == "2":
            show_locations()

        elif choice == "3":
            search_location()

        elif choice == "4":
            update_location()

        elif choice == "5":
            delete_location()

        elif choice == "6":
            break

        else:
            print("invalid input!")


#Hauptmenü
while True:
    print("\n=== Main menu ===")
    print("1.NPC menu")
    print("2.PC menu")
    print("3.Factions menu")
    print("4.Quest menu")
    print("5.Location menu")
    print("6.Exit")

    choice = input("Which menu would you like to open? ")

    if choice == "1":
        npc_menu()

    elif choice == "2":
        pc_menu()

    elif choice == "3":
        faction_menu()

    elif choice == "4":
        quest_menu()

    elif choice == "5":
        location_menu()

    elif choice == "6":
        break

    else:
        print("invalid input.")

verbindung.close()







