import random

# Define word lists
subjects = ["man", "cat", "dog", "elephant", "boy", "girl", "teacher", "child", "rabbit", "lion", "tiger", "mouse", "bird", "monkey", "doctor", "scientist"]
plural_exceptions = {"man": "men", "woman": "women", "mouse":"mice","child":"children"}  # Handle irregular plurals

verbs = {  # Dictionary for correct tense conjugation
    "sit": {"past": "sat", "present_progressive": "sitting"},
    "walk": {"past": "walked", "present_progressive": "walking"},
    "run": {"past": "ran", "present_progressive": "running"},
    "talk": {"past": "talked", "present_progressive": "talking"},
    "move": {"past": "moved", "present_progressive": "moving"},
    "jump": {"past": "jumped", "present_progressive": "jumping"},
    "push": {"past": "pushed", "present_progressive": "pushing"},
    "hold": {"past": "held", "present_progressive": "holding"},
    "kick": {"past": "kicked", "present_progressive": "kicking"},
    "roll": {"past": "rolled", "present_progressive": "rolling"},
    "slide": {"past": "slid", "present_progressive": "sliding"},
    "climb": {"past": "climbed", "present_progressive": "climbing"},
    "crawl": {"past": "crawled", "present_progressive": "crawling"},
    "dance": {"past": "danced", "present_progressive": "dancing"},
    "sing": {"past": "sang", "present_progressive": "singing"},
    "shout": {"past": "shouted", "present_progressive": "shouting"},
    "laugh": {"past": "laughed", "present_progressive": "laughing"},
    "cry": {"past": "cried", "present_progressive": "crying"},
    "think": {"past": "thought", "present_progressive": "thinking"},
    "watch": {"past": "watched", "present_progressive": "watching"}
}

objects = ["house", "ball", "floor", "plate", "chair", "table", "park", "river", "tree", "cloud", "street", "garden", "bench", "beach", "car", "mountain"]
adjectives_subject = ["big", "small","short","tall","red", "blue", "green", "scared", "happy", "sad", "angry", "excited", "sleepy", "energetic", "nervous", "brave", "curious", "playful"]
adjectives_object = ["big", "small","short","tall","red", "blue", "green", "yellow", "heavy", "light", "round", "square", "long", "short", "thick", "thin"]
verb_prepositions = {
    "sit": ["on", "in", "by","under"],
    "walk": ["to", "through", "along"],
    "run": ["to", "through", "along"],
    "talk": ["to", "with", "about"],
    "move": ["to", "from", "through","none"],
    "jump": ["over", "on", "into"],
    "push": ["against", "to", "into","none"],
    "hold": ["none"],
    "paint": ["near","in","on","none"],
    "draw": ["near","in","on","none"],
    "kick": ["at", "to", "against","none"],
    "roll": ["on", "to", "over"],
    "slide": ["on", "to", "under"],
    "climb": ["up", "on", "over","none"],
    "crawl": ["under", "through", "on"],
    "dance": ["on", "with"],
    "sing": ["to", "with", "about"],
    "shout": ["at", "to", "about"],
    "laugh": ["at", "with", "about"],
    "cry": ["about", "for", "over"],
    "think": ["about", "of", "on"],
    "watch": ["over", "for", "none"]
}
numbers = {
    "The": False,
    "A": False,
    "Two": True,
    "Three": True,
    "Four": True,
    "Five": True,
    "Several": True,
    "Many": True,
    "Some": True
    }
times = {
    "past": ["yesterday", "last night", "last week", "last month", "last year", "at 6 o'clock"],
    "present_simple": ["every day", "always", "sometimes"],
    "present_progressive": ["now", "currently","at the moment","presently", "today"],
    "future": ["tomorrow", "soon", "next week", "next month", "next year","at 5 o'clock"]
}
adverbs = ["happily", "carefully", "quickly", "slowly", "silently", "loudly", "gracefully", "clumsily", "eagerly", "sadly", "angrily", "excitedly", "nervously", "bravely", "curiously", "playfully"]

def get_plural(word):
    if word in plural_exceptions:
        return plural_exceptions[word]
    return word + "s"

def generate_sentence():
    number_word, is_plural = random.choice(list(numbers.items()))
    subject = random.choice(subjects)
    
    if is_plural:
        subject = get_plural(subject)
    
    verb = random.choice(list(verbs.keys()))
    tense = random.choice(list(times.keys()))
    
    # Choose correct verb form
    if tense == "past":
        verb_form = verbs[verb]["past"]
    elif tense == "present_simple":
        verb_form = verb
        if not is_plural:
            verb_form += "s"
    elif tense == "present_progressive":
        verb_form = "is " + verbs[verb]["present_progressive"] if not is_plural else "are " + verbs[verb]["present_progressive"]
    elif tense == "future":
        verb_form = "will " + verb
    else:
        raise ValueError("Invalid tense")
    
    adjective_subject = random.choice(adjectives_subject)
    adjective_object = random.choice(adjectives_object)
    object_noun = random.choice(objects)
    
    end_phrase = random.choice(times[tense]) if random.random() > 0.5 else random.choice(adverbs)
    # if probability > 0.5, add an adverb and time phrase
    if random.random() > 0.7:
        end_phrase = random.choice(adverbs)
    elif random.random() > 0.5:
         end_phrase = random.choice(times[tense])
    else :
        end_phrase = ""


    preposition = random.choice(verb_prepositions[verb]) if verb in verb_prepositions else "none"
    article = random.choice(["the", "a"])
    sentence = f"{number_word} {adjective_subject} {subject} {verb_form}"
    if preposition != "none":
        sentence += f" {preposition}"    
    sentence += f" {article} {adjective_object} {object_noun}"
    if end_phrase:
        sentence += f" {end_phrase}"
    #sentence += "."
    return sentence.capitalize()

# Generate and save 500,000 sentences into a file
with open("sentence_pairs.txt", "w") as file:
    for _ in range(50000):
        file.write(generate_sentence() + "\n")
