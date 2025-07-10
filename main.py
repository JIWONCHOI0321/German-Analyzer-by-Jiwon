from flask import Flask, render_template, request
import spacy
import de_core_news_sm


app = Flask(__name__)
nlp = de_core_news_sm.load()  

# POS와 Dep 설명 딕셔너리 정의
pos_expl = {
    "NOUN": "Noun (명사)",
    "VERB": "Verb (동사)",
    "DET": "Determiner (관형사)",
    "ADJ": "Adjective (형용사)",
    "ADV": "Adverb (부사)",
    "PRON": "Pronoun (대명사)",
    "ADP": "Adposition (전치사 등)",
    "AUX": "Auxiliary verb (조동사)",
    "CCONJ": "Coordinating conjunction (등위 접속사)",
    "SCONJ": "Subordinating conjunction (종속 접속사)",
    "PART": "Particle (조사 등)",
    "PUNCT": "Punctuation (구두점)",
    "INTJ": "Interjection (감탄사)",
    "NUM": "Number (수사)"
}

dep_expl = {
    "nk": "noun kernel modifier (핵심 명사 수식어)",
    "sb": "subject (주어)",
    "oa": "accusative object (직접 목적어)",
    "da": "dative object (간접 목적어)",
    "mo": "modifier (수식어)",
    "oc": "object complement (목적 보어)",
    "cj": "conjunct (병렬 요소)",
    "punct": "punctuation (구두점)",
    "root": "root (문장의 중심 동사)",
    "avz": "adverbial phrase (부사구)"
}

@app.route("/", methods=["GET", "POST"])
def index():
        result = []
        if request.method == "POST":
            text = request.form["sentence"]  
            doc = nlp(text)
            for token in doc:
                result.append({
                    "text": token.text,
                    "pos": token.pos_,
                    "pos_expl": pos_expl.get(token.pos_, "unknown"),
                    "dep": token.dep_,
                    "dep_expl": dep_expl.get(token.dep_, "unknown"),
                    "head": token.head.text
                })
        return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)