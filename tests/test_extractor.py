import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from concept_map_lite.extractor import extract_concept_map


class TestConceptMap(unittest.TestCase):
    def test_basic_nodes(self):
        cm = extract_concept_map("苹果 公司 发布 新 手机。苹果 手机 销量 很好。三星 也 发布 新 手机。", top_n=5)
        self.assertIn("手机", {n["id"] for n in cm.nodes})
    def test_edges_between_cooccur(self):
        cm = extract_concept_map("苹果 发布 新手机。华为 发布 新手机。小米 发布 新手机。", top_n=10)
        pairs = {(e["source"], e["target"]) for e in cm.edges}
        self.assertTrue(any("发布" in p for p in pairs))
    def test_json_valid(self):
        import json
        d = json.loads(extract_concept_map("测试 文本 文本 测试。").to_json())
        self.assertIn("nodes", d); self.assertIn("edges", d)
    def test_empty_text(self):
        cm = extract_concept_map("")
        self.assertEqual(cm.nodes, []); self.assertEqual(cm.edges, [])


if __name__ == "__main__": unittest.main()
