# concept-map-lite

文本 → 概念图：抽取高频实体/术语与共现，输出节点+边 JSON。

## 快速开始
```python
from concept_map_lite import extract_concept_map
print(extract_concept_map("苹果 发布 新手机。华为 发布 新手机。").to_json())
```

## 运行测试
```bash
python -m unittest discover -s tests -v
```

## License
MIT © ljiang9
