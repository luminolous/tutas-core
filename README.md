# tutas-core

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)  ![License](https://img.shields.io/badge/license-MIT-green)  ![Build](https://img.shields.io/badge/build-passing-brightgreen)

A full‑stack web app that **pairs tutors and students optimally (1‑on‑1)** using the Hungarian algorithm and **forms balanced study circles** using Louvain community detection.

---

## Features

* **Optimal 1‑on‑1 matching** – Hungarian algorithm maximises total compatibility score.
* **Tutas Circle auto‑grouping** – Builds similarity graph (TF‑IDF + cosine) → Louvain partition → sub‑groups ≤ `MAX_CIRCLE_SZ`.
* **Flexible schedule handling** – If either party is flexible, date/time mismatch is ignored in scoring.
* **Dark‑mode React UI** – Built with Next.js + Tailwind, live refresh for new pairs/groups.
* **Plain‑JSON storage** – Easy export to Google Sheets / CSV.
* **REST API** – Simple endpoints: `/submit`, `/available`, `/tutas-circle`.

---

## Workflow

![Workflow](assets/tutas%20(1).png)

---

## Screenshots & Demo

|         Register Form        |       Matched 1‑on‑1       |         Tutas Circle         |
| :--------------------------: | :------------------------: | :--------------------------: |
| ![Form](assets/Screenshot%202025-06-23%20022828.png) | ![Pairs](assets/Screenshot%202025-06-22%20221319.png) | ![Circle](assets/Screenshot%202025-06-22%20221325.png) |

---

## Tech Stack

| Layer                 | Tools / Libraries                                                                  |
| --------------------- | ---------------------------------------------------------------------------------- |
| **Frontend**          | Next.js 14, Tailwind CSS, Framer‑Motion                                            |
| **Backend API**       | Flask 3, Flask‑CORS                                                                |
| **Algorithms / Data** | pandas, numpy, scikit‑learn, **python‑louvain**, **networkx**, munkres (Hungarian) |
| **Storage**           | JSON files                                                                         |

---

## Algorithms Explained

### Hungarian (1‑on‑1)

* Finds minimum‑cost perfect matching in bipartite graph (O(n³)).
* We negate compatibility score to turn it into cost.
* Guarantees globally optimal tutor↔student assignment.

### Louvain (Method) + Sub‑Grouping (Circle)

* Maximises modularity Q to detect communities in similarity graph.
* Each community is further split into blocks ≤ `MAX_CIRCLE_SZ` (greedy fill) ensuring exactly **one tutor** per subgroup.

### Compatibility Score

| Attribute     | Weight | Compatible rule                    |
| ------------- | :----: | ---------------------------------- |
| courseName    |  **4** | exact match                        |
| topicSubtopic |  **5** | exact match                        |
| learningStyle |    3   | exact match                        |
| learningMode  |    2   | exact match                        |
| preferredDate |    1   | same date OR at least one flexible |
| preferredTime |    1   | same time OR at least one flexible |

---

## Installation

```bash
# Clone repo
$ git clone https://github.com/tutas-its/tutas-core.git

# Backend
$ cd src/tutas
$ python -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt
$ python main.py

# Frontend (new terminal)
$ cd web
$ npm install
$ npm run dev
```

---

## API Reference

| Endpoint        | Method | Body / Query        | Description                    |
| --------------- | ------ | ------------------- | ------------------------------ |
| `/submit`       | POST   | one JSON submission | Add entry & auto‑match         |
| `/available`    | GET    | –                   | Return matched 1‑on‑1 pairs    |
| `/tutas-circle` | GET    | –                   | Return study groups            |
| `/match/1on1`   | POST   | –                   | Manual trigger 1‑on‑1 matching |
| `/match/circle` | POST   | –                   | Manual trigger circle matching |

---

## Performance

| Dataset Size              | Hungarian time | Louvain time | Notes     |
| ------------------------- | -------------: | -----------: | --------- |
| 20 tutors + 50 students   |         0.04 s |       0.02 s | laptop M1 |
| 100 tutors + 300 students |          0.6 s |       0.15 s |           |

> Louvain scales \~O(E); Hungarian O(n³) but manageable for ≤ 200×200.

---

## License

Licensed under the **MIT License** – see [`LICENSE`](LICENSE).

---

> ⭐️ If you find this useful, please star the repo!
