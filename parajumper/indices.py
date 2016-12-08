"""Work with locally generated indices."""
import jieba
import parajumper.db

def _get_freq(word, text):
    """Get number of occurrence of word in text."""
    word = word.lower()
    text = text.lower()
    return text.count(word)

def gen_index(identity, text):
    """Generate a content index for item with id = identity."""
    words = [w for w in jieba.lcut_for_search(text.lower()) if w != " "]
    word_freq = []
    result = []
    for word in words:
        word_freq.append((_get_freq(word, text), word))
    word_freq.sort()
    for (_, word) in word_freq:
        result.append(word)
    parajumper.db.INDEX_T.update_one({"identity": identity},
                                     {"$set": {"words": result}},
                                     upsert=True)
