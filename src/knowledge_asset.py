from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class KnowledgeAsset:
    id: int
    category: str
    tags: List[str]
    last_updated: datetime

class KnowledgeAssetSearch:
    def __init__(self, assets: List[KnowledgeAsset]):
        self.assets = assets

    def filter_by_category(self, category: str) -> List[KnowledgeAsset]:
        return [asset for asset in self.assets if asset.category == category]

    def filter_by_tags(self, tags: List[str]) -> List[KnowledgeAsset]:
        return [asset for asset in self.assets if any(tag in asset.tags for tag in tags)]

    def sort_by_relevance(self, query: str) -> List[KnowledgeAsset]:
        return sorted(self.assets, key=lambda asset: len([tag for tag in asset.tags if tag in query]), reverse=True)

    def sort_by_last_updated(self) -> List[KnowledgeAsset]:
        return sorted(self.assets, key=lambda asset: asset.last_updated, reverse=True)

    def sort_by_popularity(self) -> List[KnowledgeAsset]:
        # For simplicity, assume popularity is the number of tags
        return sorted(self.assets, key=lambda asset: len(asset.tags), reverse=True)
