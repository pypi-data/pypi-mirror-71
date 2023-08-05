# treg 0.0.2

treg utilizes trie structured regex patterns to search texts for a potientially large number of words and phrases.

## Experimental state

This project is in an early and experimental state and might be subject substantial changes in the future.

## Documentation
Documentation is available at https://treg.readthedocs.io

## Getting started

```python
from treg import Treg, Phrase, Match

# Initialize a new pattern
treg = Treg()
# Add some phrases
treg.add_phrases([
    Phrase(phrase='afternoon tea', meta={'fun': 1}),
    Phrase(phrase='tea party', meta={'fun': 3}),
    # ...
])
# Compile the pattern
treg.compile()
# Happy searching!
for match in treg.find_iter(
        "A long collection of afternoon tea party recipes ...",
        overlapped=True):
    print(match)

# Output
Match(phrases=[Phrase(phrase='afternoon tea', meta={'fun': 1})], start=16, end=29)
Match(phrases=[Phrase(phrase='tea party', meta={'fun': 3})], start=26, end=35)
```