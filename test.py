import unittest
import pandas as pd
from src.tutas.grouping import *
from src.tutas.graph_builder import build_similarity_graph
from src.tutas.louvain.louvain import louvain
from src.tutas.grouping import make_subgroups
from src.tutas.config import INPUT_CSV, OUTPUT_CSV, THRESHOLD, MAX_CIRCLE_SZ

class TestLouvainCircleClustering(unittest.TestCase):
    def setUp(self):
        # Buat dataframe dummy untuk test
        data = "data/dummy/dummy_circle_2.csv"
        self.df = pd.read_csv(data)

        # Expected output (circle ID bisa berbeda urutan, tapi pasangan anggota komunitas harus cocok)
        self.expected_communities = [
            {'Nama': 'a_tutor', 'Circle ID': 0, 'Tutor/Murid': 'Tutor', 'No WA': 81234567890},
            {'Nama': 'b_murid', 'Circle ID': 0, 'Tutor/Murid': 'Murid', 'No WA': 81234567891},
            {'Nama': 'c_murid', 'Circle ID': 1, 'Tutor/Murid': 'Murid', 'No WA': 81234567892},
            {'Nama': 'd_murid', 'Circle ID': 2, 'Tutor/Murid': 'Murid', 'No WA': 81234567893},
            {'Nama': 'e_tutor', 'Circle ID': 2, 'Tutor/Murid': 'Tutor', 'No WA': 81234567894},
        ]

    def normalize_result(self, result):
        # Mengubah no WA ke int dan urutkan berdasarkan nama untuk perbandingan
        return sorted([
            {
                'Nama': x['Nama'],
                'Circle ID': x['Circle ID'],
                'Tutor/Murid': x['Tutor/Murid'],
                'No WA': int(str(x['No WA']).replace('+62', '62').lstrip("0").lstrip("62"))  # normalisasi
            } for x in result
        ], key=lambda x: x['Nama'])

    def test_louvain_output(self):
        df = self.df
        G  = build_similarity_graph(df, THRESHOLD)
        partition = louvain(G)
        rows = make_subgroups(df, partition, max_size=MAX_CIRCLE_SZ)
        actual_output = rows
        normalized_actual = self.normalize_result(actual_output)
        normalized_expected = sorted(self.expected_communities, key=lambda x: x['Nama'])

        # Cek jumlah anggota
        self.assertEqual(len(normalized_actual), len(normalized_expected))

        # Cek tiap entri
        for actual, expected in zip(normalized_actual, normalized_expected):
            self.assertEqual(actual['Nama'], expected['Nama'])
            self.assertEqual(actual['Tutor/Murid'], expected['Tutor/Murid'])
            self.assertEqual(actual['No WA'], expected['No WA'])

            # Circle ID bisa acak, tapi kita cek via mapping komunitas
        # Cek struktur komunitas
        community_map_actual = {}
        for x in normalized_actual:
            community_map_actual.setdefault(x['Circle ID'], []).append(x['Nama'])

        community_map_expected = {}
        for x in normalized_expected:
            community_map_expected.setdefault(x['Circle ID'], []).append(x['Nama'])

        # Cek semua anggota komunitas ada dan lengkap (urutan tidak penting)
        actual_sets = [set(v) for v in community_map_actual.values()]
        expected_sets = [set(v) for v in community_map_expected.values()]

        self.assertCountEqual(actual_sets, expected_sets)

if __name__ == '__main__':
    unittest.main()