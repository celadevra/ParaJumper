"""Work with locally generated indices."""
import jieba
import parajumper.db

def _get_freq(word_list):
    """Get number of occurrence of word in a list."""
    counts = dict()
    for word in word_list:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    results = []
    for word in counts:
        results.append((counts[word], word))
    results.sort()
    return results

def gen_index(identity, text):
    """Generate a content index for item with id = identity."""
    words = [w for w in jieba.lcut_for_search(text.lower()) if w != " "]
    word_freq = _get_freq(words)
    result = []
    for (_, word) in word_freq:
        result.append(word)
    parajumper.db.INDEX_T.update_one({"identity": identity},
                                     {"$set": {"words": result}},
                                     upsert=True)
