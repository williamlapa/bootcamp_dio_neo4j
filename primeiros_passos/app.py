import pandas as pd
import uuid

# === 1️⃣ Leitura do arquivo ===
arquivo = "MUSICAS.xlsx"
df = pd.read_excel(arquivo, sheet_name="Music_Info")

# === 2️⃣ Criação da tabela de ARTISTAS ===
artistas = (
    df[['artist']]
    .drop_duplicates()
    .reset_index(drop=True)
    .rename(columns={'artist': 'nome'})
)
# Gera uma chave única por artista
artistas['artist_id'] = [str(uuid.uuid4()) for _ in range(len(artistas))]

# === 3️⃣ Criação da tabela de MÚSICAS ===
musicas = df.copy()

# Faz o join para associar o artist_id
musicas = musicas.merge(artistas, left_on='artist', right_on='nome', how='left')

# Seleciona apenas colunas relevantes + artist_id
musicas = musicas[[
    'track_id', 'name', 'spotify_id', 'genre', 'year', 'duration_ms',
    'danceability', 'energy', 'speechiness', 'acousticness', 'valence',
    'tempo', 'artist_id'
]].rename(columns={'name': 'titulo'})

# === 4️⃣ Criação da tabela de USUÁRIOS (simulada) ===
# Como o dataset original não contém usuários, criamos um conjunto exemplo.
usuarios = pd.DataFrame({
    "user_id": [str(uuid.uuid4()) for _ in range(5)],
    "nome": ["Alice", "Bruno", "Carla", "Diego", "Eva"],
    "pais": ["Brasil", "EUA", "Reino Unido", "Alemanha", "Japão"]
})

# === 5️⃣ Exportação dos arquivos ===
artistas.to_csv("artistas.csv", index=False, encoding="utf-8")
musicas.to_csv("musicas.csv", index=False, encoding="utf-8")
usuarios.to_csv("usuarios.csv", index=False, encoding="utf-8")

print("✅ Arquivos gerados com sucesso:")
print("- artistas.csv")
print("- musicas.csv")
print("- usuarios.csv")
