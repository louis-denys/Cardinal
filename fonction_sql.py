import sqlite3
path = 'data.db'

### MEMBRE ###

def add_to_bdd(id, warn, xp):
    """
    On ajoute un nouvelle enregistrement à la BDD
    """
    conn = sqlite3.connect(path, check_same_thread=False) #Vu Logo
    cur = conn.cursor()
    cur.execute(f"INSERT INTO MEMBRE (id, nb_warn, xp) VALUES ({id}, {warn}, {xp})")
    conn.commit()
    cur.close()
    conn.close()
    return

def look_in_bdd(id):
    """
    On effectue une recher d'un contact dans la BDD
    A partir de son nom ou de son prénom précisé dans la variable x
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM MEMBRE WHERE id = {id}")

    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

def bdd_rank():
    """
    On effectue une recherche des plus hauts lvl dans la BDD
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("SELECT id, xp, lvl FROM MEMBRE")

    data = cur.fetchall()

    order = sorted(data, key= lambda data: data[1])
    order = sorted(order, key= lambda data: data[2])
    order.reverse()

    conn.commit()
    cur.close()
    conn.close()
    return order

def maj_warn(id, warn):
    """
    Modifie le nombre de warn. (Ajoute pas ! Modifie.) 
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(f"UPDATE MEMBRE SET nb_warn = {warn} where id = {id}")
    
    conn.commit()
    cur.close()  
    conn.close()

def maj_xp(id, xp):
    """
    Modifie le nombre d'xp. (Ajoute pas ! Modifie.) 
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(f"UPDATE MEMBRE SET xp = {xp} where id = {id}")
    
    conn.commit()
    cur.close()  
    conn.close()
    
def lvl_up(id, lvl):
    """
    Modifie le nombre d'xp. (Ajoute pas ! Modifie.) 
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(f"UPDATE MEMBRE SET xp = 0, lvl = {lvl} where id = {id}")
    
    conn.commit()
    cur.close()  
    conn.close()

### Aventuriers ###

def add_aventurier(prenom, nom, proprietaire):
    """
    Permet d'enregister un nouvel aventurier dans la BDD
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(f"INSERT INTO AVENTURIER (prenom, nom, proprietaire) VALUES ('{prenom}', '{nom}', {proprietaire})")

    conn.commit()
    cur.close()
    conn.close()

def remove_aventurier(prenom = None, nom = None, id = None):
    """
    Permet de retirer un aventurier de la BDD
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()
    if prenom == None and nom == None:
        cur.execute(f"DELETE FROM AVENTURIER WHERE prenom = '{prenom}' AND nom = '{nom}'")
    else:
        try:
            cur.execute(f"DELETE FROM AVENTURIER WHERE id = {id}")
        except:
            pass

    conn.commit()
    cur.close()
    conn.close()

def depot_retrait(prenom, nom, montant):
    """
    Ajouter de l'argent à un aventurier
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(f"UPDATE AVENTURIER SET argent = {montant} where prenom = '{prenom}' AND nom = '{nom}'")

    conn.commit()
    cur.close()
    conn.close()

def look_aventurier(prenom, nom):
    """
    Recuperer les infos depuis la table aventurier
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM AVENTURIER WHERE prenom = '{prenom}' AND nom = '{nom}'")
    data = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return data
