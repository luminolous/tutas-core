import pandas as pd

from config import INPUT_CSV, OUTPUT_CSV, THRESHOLD, MAX_CIRCLE_SZ
from data_loader import load_data
from graph_builder import build_similarity_graph
from louvain.louvain import louvain
from grouping import make_subgroups
from scoring import matriks
from hungarian.matching import match_tutors

def main():
    # —————————————
    # 1) BIKIN CIRCLE
    # —————————————
    df = load_data(INPUT_CSV)
    G  = build_similarity_graph(df, THRESHOLD)
    partition = louvain(G)
    rows = make_subgroups(df, partition, max_size=MAX_CIRCLE_SZ)

    pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False)
    print(f"➡️  Circles saved to {OUTPUT_CSV}")

    # —————————————————
    # 2) MATCHING TUTOR
    # —————————————————
    # pakai scoring + Hungarian dari package
    score_df = matriks()
    match_tutors(score_df)


if __name__ == "__main__":
    main()
