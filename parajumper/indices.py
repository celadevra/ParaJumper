"""Work with locally generated indices."""
import jieba
import parajumper.db

def _get_freq(word_list):
    """Get number of occurrence of word in a list."""
    word_set = set(word_list)
    results = []
    for word in word_set:
        results.append((word_list.count(word), word))
    results.sort()
    return results

def gen_index(identity, text):
    """Generate a content index for item with id = identity."""
    words = [w for w in jieba.cut_for_search(text.lower()) if w != " "]
    word_freq = _get_freq(words)
    result = []
    for (_, word) in word_freq:
        result.append(word)
    parajumper.db.INDEX_T.update_one({"identity": identity},
                                     {"$set": {"words": result}},
                                     upsert=True)
