# Define prior probabilities
p_spam = 0.3  # Prior probability of an email being spam
p_not_spam = 0.7  # Prior probability of an email not being spam

# Define likelihoods
p_word_given_spam = 0.5  # Probability of seeing a specific word in a spam email
p_word_given_not_spam = 0.1  # Probability of seeing the same word in a non-spam email

# Assume we observe a word in an email
word_observed = "offer"

# Calculate evidence (probability of observing the word)
p_word = (p_word_given_spam * p_spam) + (p_word_given_not_spam * p_not_spam)

# Calculate posterior probabilities
p_spam_given_word = (p_word_given_spam * p_spam) / p_word  # Posterior probability of the email being spam given the word
p_not_spam_given_word = (p_word_given_not_spam * p_not_spam) / p_word  # Posterior probability of the email not being spam given the word

# Make a decision based on posterior probabilities
decision = "Spam" if p_spam_given_word > p_not_spam_given_word else "Not Spam"

# Print results
print("Posterior probability of spam given the word:", p_spam_given_word)
print("Posterior probability of not spam given the word:", p_not_spam_given_word)
print("Decision based on posterior probabilities:", decision)
