# PyHavamal

The [Hávamál](https://en.wikipedia.org/wiki/H%C3%A1vam%C3%A1l) is an Old Norse poem in which each stanza is a saying. The topics range from proper feast decorum to dealing with sorcerers. PyHavamal provides easy access to the text of a [translation by Henry Adams Bellows](https://en.wikisource.org/wiki/Poetic_Edda/H%C3%A1vam%C3%A1l).

# Installation

Use `pip install pyhavamal`.

# Use

There are 165 stanzas in the Bellows translation numbered 1-165.

- `all()` returns a list of all stanzas. Pass `numbered=True` to return a dict of numbered stanzas.
- `find_by_number(n)` returns stanza n (where n is the stanza number and not zero-based).
- `random()` returns a random stanza.
- `range_by_number(a, b)` returns a list of stanzas from a to b inclusive (where a and b are stanza numbers and not zero-based).

# License

[MIT License](LICENSE)