import pandas as pd
import unicodedata
import simplejson

df = pd.read_excel("Lexique4.xlsx")

# enlever accents
def enlever_accents(texte):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texte))
        if unicodedata.category(c) != 'Mn'
    )

# colonne des mots
df["mot"] = (
    df["1_Mot"]
    .astype(str)
    .str.lower()
    .apply(enlever_accents)
)

# garder uniquement lettres
df = df[df["mot"].str.fullmatch(r"[a-z]+")]

# mots de 5 lettres
df = df[df["mot"].str.len() == 5]

# supprimer doublons
df = df.drop_duplicates(subset="mot")

# dictionnaire mot -> fréquence
dico_freq = dict(zip(df["mot"], df["11_FreqOrtho"]))


s=0
freq_mot3={}
for e in list(dico_freq):
    s=s+dico_freq[e]
for e in list(dico_freq):
    freq_mot3[e]=dico_freq[e]/s

print(freq_mot3)
with open("list_lexique4.json", "w", encoding="utf-8") as f:
    simplejson.dump(list(freq_mot3), f, ensure_ascii=False)


