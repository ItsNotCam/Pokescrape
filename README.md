# Pokescrape

Pokescrape is a web scraper that pulls pokemon data from [Pokemon DB](https://pokemondb.net) and stores it in a mysql database.
The entity relationship diagram and the tables' schema are shown at the bottom of this README

## Setup
1. Add the database 'pokemon' to your mysql database
2. Set up your credentials and input them into the .env file
3. Clone the repsitory `git clone https://github.com/ItsNotCam/Pokescrape.git`
4. Run `pip3 install -r requirements.txt` from the root directory
5. Run `python3 pokescrape.py` with the arguments that you want

## Command Line Arguments
`--init`: initializes the database tables and indices \
`-v` or `--verbose`: Shows a more detailed view of each pokemon added \
`-p` or `--pokemon`: Pulls all pokemon from the website \
`-ps` or `--pstart`: Tells the script which pokemon number to start with (to be included with `-p`, but is optional) \
`-pe` or `--pend`: Tells the script which pokemon number to end at (to be included with `-p`, but is optional) \
`-m` or `--moves`: Pulls all moves from the website \
`-a` or `--abilities`: Pulls all abilities from the website \
`-d` or `--damage`: Pulls the element damage effectiveness matrix from the site \
`--icons`: Downloads all of the pokemon thumbnails from the website \
`--images`: Downloads all of the detailed pokemon images

## Example Queries
### If you are viewing from my [website](https://cameronayoung.dev), the syntax highlighting will be very off. It is recommended to click the GitHub button on this card to view this readme.
Get all water-type Pokemon:
```sql
SELECT * 
FROM pokemon
INNER JOIN pokemon_element
  ON number = pokemon_number
  AND name = pokemon_name
  AND sub_name = pokemon_sub_name
WHERE element_name = 'Water'
```

Get a Pokemon's move set:
```sql
SELECT m.* 
FROM pokemon AS p
INNER JOIN pokemon_move AS pm
  ON p.number = pm.pokemon_number
  AND p.name = pm.pokemon_name
  AND p.sub_name = pm.pokemon_sub_name
INNER JOIN move AS m
  ON m.name = pm.move_name
WHERE p.name = 'Mudkip';
```

Get all data for each Pokemon and include all of its elements
```sql
SELECT 
  p.*,
  GROUP_CONCAT(pe.element_name) AS elements
FROM pokemon AS p
INNER JOIN pokemon_element AS pe 
  ON pe.pokemon_number = p.number
  AND pe.pokemon_name = p.name
  AND pe.pokemon_sub_name = p.sub_name
GROUP BY p.number, p.name, p.sub_name;
```

Get all moves from one Pokemon and determine their effectiveness on a target Pokemon. \
In this case, Onix is attacking Charizard:
```sql
SELECT
  defender.name AS defender_name,
  defender.sub_name AS defender_sub_name,
  GROUP_CONCAT(DISTINCT defender_element.element_name) AS defender_elements,
  m.name AS move_name,
  me.dmg_source,
  CASE
    WHEN me.effectiveness = 0 THEN 'no effectiveness'
    WHEN me.effectiveness = 0.5 THEN 'not very effective'
    WHEN me.effectiveness = 1 THEN 'normal'
    WHEN me.effectiveness = 2 THEN 'super-effective'
  END AS friendly_effectiveness,
  GROUP_CONCAT(DISTINCT me.effectiveness) AS effectiveness
FROM pokemon_move AS pm
INNER JOIN pokemon AS defender
  ON defender.name = 'Charizard'
INNER JOIN move AS m
  ON m.name = pm.move_name
INNER JOIN move_effectiveness AS me
  ON me.dmg_dest IN (
    SELECT element_name
    FROM pokemon_element
    WHERE pokemon_name = 'Charizard'
  )
  AND me.dmg_source = m.element_name
INNER JOIN pokemon_element AS defender_element
  ON defender_element.pokemon_number = defender.number
  AND defender_element.pokemon_name = defender.name
  AND defender_element.pokemon_sub_name = defender.sub_name
WHERE pm.pokemon_name = 'Onix'
GROUP BY pm.move_name, me.dmg_dest, defender.name, defender.sub_name
ORDER BY effectiveness DESC;
```

## Entity Relationship Diagram
![pokescrape](https://github.com/ItsNotCam/Pokescrape/assets/46014191/93925f73-5048-46a3-a37a-c239d9e5c6b2)
