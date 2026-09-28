"""Chapter 13 notebook: language models and LLMs (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def length(a):
    return math.sqrt(dot(a, a))


def cosine(a, b):
    return dot(a, b) / (length(a) * length(b))


print("1. embeddings: meaning as coordinates")
risk = (3, 1)
score = (3, 2)
sandwich = (0, 5)
print("cosine(risk, score) =",
      round(cosine(risk, score), 3), "(about 0.965)")
print("cosine(risk, sandwich) =",
      round(cosine(risk, sandwich), 3), "(about 0.316)")
print("similar usage lands nearby")

print()
print("2. the QKV spotlight (plain weights)")
scores = [2, 5, 1]
total = sum(scores)
weights = [round(s / total, 4) for s in scores]
names = ["login failed", "new country", "night hour"]
for name, w in zip(names, weights):
    print(f"  {name}: {w}")
print("weights:", weights, " sum:", round(sum(weights), 3))
print("the reading leans on:", names[weights.index(max(weights))])
print("score 4, 1, 3 would give:",
      [round(s / 8, 3) for s in [4, 1, 3]])

print()
print("3. RAG: retrieve, then read")
stopwords = {"the", "when", "does", "at", "is", "on"}


def tokens(text):
    pieces = text.replace(":", " ").lower().split()
    return {p for p in pieces if p not in stopwords}


question = tokens("when does the firewall drop port 22")
chunks = {
    "A": "the firewall drops port 22 at night",
    "B": "the office printer is idle on weekends",
    "C": "backup jobs run at 22:00",
}
print("small words dropped; 22:00 splits into 22 and 00")
for name, text in sorted(chunks.items()):
    hits = sorted(question & tokens(text))
    print(f"  chunk {name}: {len(hits)} matches {hits}")
print("retrieved top 2: A (3), C (1); the answer reads from A:")
print("  the firewall drops port 22 at night (source: chunk A)")

print()
print("fluency is not knowledge; check every citation")
