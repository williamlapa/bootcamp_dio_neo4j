LOAD CSV WITH HEADERS FROM 'file:///music_info.csv' AS row
WITH row,
     toInteger(row.user_id) AS user_id,
     toInteger(row.track_id) AS track_id,
     toInteger(row.artist_id) AS artist_id,
     toInteger(row.nota) AS nota,
     toInteger(row.duracao) AS duracao

MERGE (u:Usuario {user_id: user_id})
  ON CREATE SET u.nome = row.nome_usuario, u.pais = row.pais

MERGE (m:Musica {track_id: track_id})
  ON CREATE SET m.titulo = row.titulo, m.duracao = duracao

MERGE (a:Artista {artist_id: artist_id})
  ON CREATE SET a.nome = row.nome_artista

MERGE (g:Genero {nome: row.genero})

MERGE (u)-[r1:OUVIU_A]->(m)
  ON CREATE SET r1.nota = nota

FOREACH (_ IN CASE WHEN row.date IS NOT NULL AND row.date <> "" THEN [1] ELSE [] END |
  MERGE (u)-[r2:CURTIU_A {date: row.date}]->(m)
)

MERGE (m)-[:E_DE_UM]->(a)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a)-[:IN_GENRE]->(g)

FOREACH (_ IN CASE WHEN row.user_followed IS NOT NULL AND row.user_followed <> "" THEN [1] ELSE [] END |
  MERGE (u2:Usuario {user_id: toInteger(row.user_followed)})
  MERGE (u)-[r3:SEGUE_O {since: row.since}]->(u2)
);

RETURN 'Importação concluída com sucesso!' AS status;
