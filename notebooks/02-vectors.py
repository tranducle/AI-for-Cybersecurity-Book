# Companion notebook 02: the vector toolbox on fictional emails.
# All values fictional; standard library only.
import math

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(a):
    return math.sqrt(dot(a, a))

def cosine(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def distance(a, b):
    return norm(tuple(x - y for x, y in zip(a, b)))

a = (40, 1)
b = (120, 3)
c = (150, 10)
print("a = (40, 1)  b = (120, 3)")
print("dot(a,b) = %d | |a| = %.3f | |b| = %.3f"
      % (dot(a, b), norm(a), norm(b)))
print("cos(a,b) = %.3f | angle = %.1f deg | dist(a,b) = %.2f"
      % (cosine(a, b), math.degrees(math.acos(cosine(a, b))),
         distance(a, b)))
print("a = (40, 1)  c = (150, 10)")
print("dot(a,c) = %d | |c| = %.3f"
      % (dot(a, c), norm(c)))
print("cos(a,c) = %.3f | angle = %.1f deg | dist(a,c) = %.1f"
      % (cosine(a, c), math.degrees(math.acos(cosine(a, c))),
         distance(a, c)))
print("score is an observation, not a verdict")
