# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import pathlib


# Instantiates a client

text = """Decent flight
Great flight out of a small airport (Long Beach, CA). Departed on time and arrived early. Decent amount of entertainment options--I like that DirecTV is available, a bunch of people were watching a game at the same time so you could hear cheering/sighing throughout the cabin, haha. Decent variety of snacks. The fly-fi (online wi-fi) was spotty but worked well once we were at cruising altitude, and I love that it's free. Attendants were okay, just going through the motions I guess. Would definitely fly again, especially from this airport."""

def sentiment_value(text):
    client = language.LanguageServiceClient()
    # The text to analyze
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document)
    return sentiment.document_sentiment.score

textfile = "TripAdvisorReview.txt"

def sort_data(textfile):
    print("breki")
    with open(textfile) as fp:
        for line in fp:
            x = sentiment_value(line)
            if 0.25 < x:
                filename = "Good.txt"
            elif  -0.25 < x:
                filename = "Ok.txt"
            else:
                filename = "Bad.txt"
            #i want to put (line)(the variable) as a new line in the texfile (filename)
            print(filename)

sort_data(textfile)
