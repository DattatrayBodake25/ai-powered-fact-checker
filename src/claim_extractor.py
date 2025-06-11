import spacy

class ClaimExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_claim(self, text):
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return sentences  # For now, return full sentences as claims

if __name__ == "__main__":
    extractor = ClaimExtractor()
    text = "India conducted Operation Sindoor as a counter-terror mission in Jammu & Kashmir."
    claims = extractor.extract_claim(text)
    print("Extracted Claims:")
    print(claims)