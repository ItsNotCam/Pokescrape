-- SQLite
SELECT p.name || " " || p.sub_name AS name, 
	GROUP_CONCAT(DISTINCT e.name) AS elements, 
	GROUP_CONCAT(DISTINCT a.name) AS abilities, 
	GROUP_CONCAT( DISTINCT "Generation " || a.generation || ": " || a.description),
	GROUP_CONCAT(DISTINCT pevs.ev_amount || " " || evs.name) AS 'evs',
	p.attack,
	p.special_attack AS 'Sp. Att.',
	p.defense,
	p.special_defense AS 'Sp. Def.'

FROM pokemon AS p

INNER JOIN pokemon_elements AS pe 
	ON pe.pokemon_number = p.number 
	AND pe.pokemon_name = p.name 
	AND pe.pokemon_sub_name = p.sub_name

INNER JOIN elements AS e 
	ON pe.element_name = e.name

INNER JOIN pokemon_abilities AS pa 
	ON pe.pokemon_number = pe.pokemon_number 
	AND pe.pokemon_name = pa.pokemon_name 
	AND pe.pokemon_sub_name = pa.pokemon_sub_name

INNER JOIN pokemon_evs AS pevs
	ON pevs.pokemon_number = p.number 
	AND pevs.pokemon_name = p.name 
	AND pevs.pokemon_sub_name = p.sub_name

INNER JOIN evs
	ON evs.name = pevs.ev_name

INNER JOIN abilities AS a 
	ON pa.ability_name = a.name

GROUP BY pe.pokemon_number, pe.pokemon_name, pe.pokemon_sub_name;