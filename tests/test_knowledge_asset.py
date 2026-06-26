from datetime import datetime
from knowledge_asset import KnowledgeAsset, KnowledgeAssetSearch

def test_filter_by_category():
    assets = [
        KnowledgeAsset(1, "category1", ["tag1", "tag2"], datetime(2022, 1, 1)),
        KnowledgeAsset(2, "category2", ["tag3", "tag4"], datetime(2022, 1, 2)),
        KnowledgeAsset(3, "category1", ["tag5", "tag6"], datetime(2022, 1, 3)),
    ]
    search = KnowledgeAssetSearch(assets)
    filtered_assets = search.filter_by_category("category1")
    assert len(filtered_assets) == 2
    assert filtered_assets[0].id == 1
    assert filtered_assets[1].id == 3

def test_filter_by_tags():
    assets = [
        KnowledgeAsset(1, "category1", ["tag1", "tag2"], datetime(2022, 1, 1)),
        KnowledgeAsset(2, "category2", ["tag3", "tag4"], datetime(2022, 1, 2)),
        KnowledgeAsset(3, "category1", ["tag5", "tag6"], datetime(2022, 1, 3)),
    ]
    search = KnowledgeAssetSearch(assets)
    filtered_assets = search.filter_by_tags(["tag1", "tag5"])
    assert len(filtered_assets) == 2
    assert filtered_assets[0].id == 1
    assert filtered_assets[1].id == 3

def test_sort_by_relevance():
    assets = [
        KnowledgeAsset(1, "category1", ["tag1", "tag2"], datetime(2022, 1, 1)),
        KnowledgeAsset(2, "category2", ["tag3", "tag4"], datetime(2022, 1, 2)),
        KnowledgeAsset(3, "category1", ["tag5", "tag6"], datetime(2022, 1, 3)),
    ]
    search = KnowledgeAssetSearch(assets)
    sorted_assets = search.sort_by_relevance("tag1 tag2")
    assert len(sorted_assets) == 3
    assert sorted_assets[0].id == 1

def test_sort_by_last_updated():
    assets = [
        KnowledgeAsset(1, "category1", ["tag1", "tag2"], datetime(2022, 1, 1)),
        KnowledgeAsset(2, "category2", ["tag3", "tag4"], datetime(2022, 1, 2)),
        KnowledgeAsset(3, "category1", ["tag5", "tag6"], datetime(2022, 1, 3)),
    ]
    search = KnowledgeAssetSearch(assets)
    sorted_assets = search.sort_by_last_updated()
    assert len(sorted_assets) == 3
    assert sorted_assets[0].id == 3

def test_sort_by_popularity():
    assets = [
        KnowledgeAsset(1, "category1", ["tag1", "tag2"], datetime(2022, 1, 1)),
        KnowledgeAsset(2, "category2", ["tag3", "tag4", "tag5"], datetime(2022, 1, 2)),
        KnowledgeAsset(3, "category1", ["tag6"], datetime(2022, 1, 3)),
    ]
    search = KnowledgeAssetSearch(assets)
    sorted_assets = search.sort_by_popularity()
    assert len(sorted_assets) == 3
    assert sorted_assets[0].id == 2
