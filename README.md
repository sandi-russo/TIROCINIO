# Tecniche di Analisi Avanzata dei Dati tramite Graph Data Science ed Intelligenza Artificiale

## Informazioni Generali
* **Studente:** Sandi Russo
* **Docenti Tutor:** Antonio Celesti, Rosario Napoli
* **ID Tirocinio:** PTI_Celesti Antonio_20/03/2025 17.27.44
* **Istituzione:** Università degli Studi di Messina, dipartimento MIFT

---

## Abstract del Progetto
L’obiettivo di questo progetto di tirocinio è l’utilizzo di **Knowledge Graphs**, un'area emergente nell'analisi dei Big Data, per affrontare complessi problemi di Deep Learning tramite l’utilizzo della **Graph Data Science (GDS)**. 

In particolare, il lavoro si concentra sullo sviluppo, l'implementazione e il confronto di strumenti e algoritmi di Machine Learning su grafi per:
* **Classificazione dei nodi** (Node Classification)
* **Clustering** e rilevamento di comunità
* **Predizione dei collegamenti** (Link Prediction)
* **Identificazione di pattern nascosti** all’interno di dati massivi.

Il progetto prevede un'infrastruttura di test comparativa che vede contrapposti due ecosistemi di gestione dati differenti: **Neo4j** (motore a grafo nativo) e **Oracle Database** (motore relazionale esteso a grafo). L'obiettivo è analizzare le performance, la tolleranza ai dati sporchi e l'efficienza nell'addestramento di Graph Neural Networks (GNN).

---

## Il Dataset: PharMeBINet
Il dataset scelto per condurre gli esperimenti è **PharMeBINet** (Pharmacological and Medical Biomedical Informatics Network), un massiccio grafo della conoscenza biologica, medica e farmacologica. Integra decine di database open-source (come DrugBank, DisGeNET, e clincaltrials.gov) in un'unica topologia interconnessa.

* **Tipologia di Dati:** Relazioni tra Geni, Malattie, Farmaci, Proteine e Vie metaboliche.
* **Volume Infrastrutturale:**
  * **Nodi (Entità):** 5.831.471
  * **Archi (Relazioni):** 22.783.080
* **Perché PharMeBINet?** L'alta eterogeneità e la densità di questo dataset lo rendono il candidato perfetto (e sfidante) per testare i limiti architetturali dei DBMS e l'accuratezza degli algoritmi di intelligenza artificiale applicata ai grafi.

---

## Architettura a Confronto: Nativo vs Relazionale
Il cuore ingegneristico di questo progetto è il benchmark tra due paradigmi architetturali di storage e analisi. Al fine di garantire un test scientificamente inattaccabile, i due database sono stati sottoposti a un processo di pulizia e allineamento (Data Forensics) per raggiungere un benchmark **"Zero-Difference"** (stesso identico numero di nodi e archi validi).

### 1. Neo4j (Il DBMS a Grafo Nativo)
Neo4j utilizza la *Index-Free Adjacency*, il che significa che ogni nodo contiene fisicamente i puntatori in memoria ai nodi adiacenti. 
* **Importazione:** I dati sono stati strutturati e caricati massivamente tramite la libreria APOC, risolvendo problemi complessi di concorrenza e deadlock (`parallel: false` sui caricamenti ad alta densità).
* **Comportamento logico:** Essendo nativo, Neo4j filtra intrinsecamente il rumore, scartando i "dangling edges" (archi che puntano a nodi inesistenti) già in fase di importazione.
* **ML Engine:** `Neo4j Graph Data Science (GDS)`.

### 2. Oracle DB (Il DBMS Relazionale con Graph Extension)
Oracle Database rappresenta l'approccio ibrido. I dati sono immagazzinati fisicamente su disco in tradizionali tabelle relazionali a righe e colonne (`pharme_nodes` e `pharme_edges`).
* **Importazione:** È stata utilizzata la tecnica del *Direct Path Load* e delle *External Tables* per caricare decine di Gigabyte ignorando il costoso overhead delle Foreign Keys durante la fase bulk.
* **Comportamento logico:** Sebbene il livello fisico (SQL) accetti topologie "sporche", la proiezione in RAM tramite l'istruzione `CREATE PROPERTY GRAPH` (SQL/PGQ) applica un rigoroso controllo topologico, allineando matematicamente i dati logici a quelli di Neo4j.
* **ML Engine:** `Oracle PGX (Parallel Graph AnalytiX)` e `OML4Py`.

---

## Struttura Modulare del Codice
Seguendo le *best practices* del Software Engineering, il progetto Python è stato strutturato in moduli indipendenti e "pluggabili", orchestrati da un unico punto di ingresso centrale. Questo permette di eseguire esperimenti isolati passando dinamicamente da un backend all'altro.

```text
TIROCINIO/
├── main.py
├── requirements.txt
├── .gitignore
├── .env
│
├── database/
│   ├── __init__.py
│   ├── oracle_manager.py
│   └── neo4j_manager.py
│
└── ml_models/
    ├── __init__.py
    ├── oracle_pgx_ml.py
    └── neo4j_gds_ml.py
```

---

## Setup & Requisiti
Per replicare l'ambiente di test:

1. Clonare la repository:
```bash
git clone [https://github.com/sandi-russo/TIROCINIO.git](https://github.com/sandi-russo/TIROCINIO.git)
cd TIROCINIO
```

2. Creare e attivare un Virtual Environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Installare le dipendenze:
```bash
pip install -r requirements.txt
```

4. Creare un file testuale `.env` nella root del progetto per le credenziali (es. `ORACLE_USER=...`).

5. Eseguire la pipeline principale:
```bash
python main.py
```

---
*Progetto sviluppato come attività di Tirocinio Curriculare presso l'Università degli Studi di Messina.*
