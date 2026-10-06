"""concept_map_lite: 文本 → 概念图（实体共现 → 节点+边 JSON）。"""
from .extractor import extract_concept_map, ConceptMap

__all__ = ["extract_concept_map", "ConceptMap"]
__version__ = "0.1.0"
