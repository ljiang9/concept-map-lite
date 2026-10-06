"""从文本抽取高频术语与共现关系，输出概念图 JSON。"""
from __future__ import annotations
import json, re
from collections import Counter
from dataclasses import dataclass

STOPWORDS = set("的 了 和 是 在 也 就 都 而 及 与 这 那 你 我 他 她 它 们 之 或 一个 没有 我们 你们 他们 但是 因为 所以 如果 虽然 不过 以及 进行 可以 这个 那个".split())


@dataclass
class ConceptMap:
    nodes: list
    edges: list
    def to_json(self) -> str:
        return json.dumps({"nodes": self.nodes, "edges": self.edges}, ensure_ascii=False, indent=2)


def _split_sentences(text):
    return [s.strip() for s in re.split(r"[。！？!?\n；;]", text) if s.strip()]


def _candidate_terms(sentence, min_len=2):
    words = re.findall(r"[一-龥]{2,}", sentence)
    out = []
    for w in words:
        if w in STOPWORDS: continue
        if len(w) >= min_len: out.append(w)
    return out


def extract_concept_map(text, top_n=10, cooccur_window=5):
    sentences = _split_sentences(text)
    node_counter = Counter(); edge_counter = Counter()
    for sent in sentences:
        terms = _candidate_terms(sent)
        seen = set()
        for t in terms:
            if t not in seen: node_counter[t] += 1; seen.add(t)
        for i, a in enumerate(terms):
            for b in terms[i+1:i+1+cooccur_window]:
                if a == b: continue
                edge_counter[tuple(sorted((a, b)))] += 1
    nodes = [{"id": w, "weight": c} for w, c in node_counter.most_common(top_n)]
    top_ids = {n["id"] for n in nodes}
    edges = [{"source": a, "target": b, "weight": w}
             for (a, b), w in edge_counter.most_common(30)
             if a in top_ids and b in top_ids]
    return ConceptMap(nodes=nodes, edges=edges)
