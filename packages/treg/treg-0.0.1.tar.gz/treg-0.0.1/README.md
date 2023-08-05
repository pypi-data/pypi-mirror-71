# tregex

Tregex utilizes trie structured regex patterns to search texts for a potientially large number of words and phrases.

## Documentation
Documentation is available at https://tregex.readthedocs.io/

## Getting started

```python
from treg import Tregex, Phrase, Match

# Initialize a new pattern
trex = Tregex()
# Add some phrases
trex.add_phrases([
    Phrase(phrase='afternoon tea', meta={'fun': 1}),
    Phrase(phrase='tea party', meta={'fun': 3}),
    # ...
])
# Compile the pattern
trex.compile()
# Happy searching!
for match in trex.find_iter(
        "A long collection of afternoon tea party recipes ...",
        overlapped=True):
    print(match)

# Output
Match(phrases=[Phrase(phrase='afternoon tea', meta={'fun': 1})], start=16, end=29)
Match(phrases=[Phrase(phrase='tea party', meta={'fun': 3})], start=26, end=35)
```