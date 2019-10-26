# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = """Decent flight
Great flight out of a small airport (Long Beach, CA). Departed on time and arrived early. Decent amount of entertainment options--I like that DirecTV is available, a bunch of people were watching a game at the same time so you could hear cheering/sighing throughout the cabin, haha. Decent variety of snacks. The fly-fi (online wi-fi) was spotty but worked well once we were at cruising altitude, and I love that it's free. Attendants were okay, just going through the motions I guess. Would definitely fly again, especially from this airport."""
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document)

print('Text: {}'.format(text))
print(sentiment)
