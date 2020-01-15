---- zestawienie wszystkich opcji
drop table ids_dict;

create table ids_dict as	
select 
	id_, 
	author_by_idor_by_id, 
	author_by_text, 
	count(*) as ile,
	null as author_final
from speeches
group by id_,author_by_idor_by_id, 
	author_by_text;

----- ile jest bez przypisania z tekstu
select count(*)
from ids_dict
where author_by_text is null;

---- 1853 pustych na 19689

update ids_dict 
SET	author_final = NULL

/*
1. Tam gdzie chociaz raz przypisanie z tekstu jest takie samo jak z id, przypisuje te wartosc
*/

update ids_dict 
SET	author_final = (select distinct author_by_id from ids_dict as tab1
					where author_by_text=author_by_id
					and tab1.id_ = ids_dict.id_) updt;

					
--- ile brakuje
select count(*), count(distinct id_)
from ids_dict
where author_final is null;

--19698	3828
--9613	3095



/*
2. Po najwiekszej liczbie przypisan z tekstu
*/

-- dla prejrzystosci tworze tabele pomocnicza, 
-- w ktorej dla kazdego id znajduje najczesciej wystepujace
-- imie i nazwisko autora odczytane z tekstu

DROP TABLE help_top_names;

CREATE TABLE help_top_names as	
SELECT * FROM (
				select id_, author_by_text, ile, row_number() over (partition by id_ order by ile desc) as row_n
				from ids_dict
				where author_final is null ) top_name
WHERE row_n=1
	and author_by_text is not null;

-- przypisanie wartosci z tabeli pomocniczej
update ids_dict
SET	
	author_final = (select author_by_text from help_top_names as h
					where h.id_ = ids_dict.id_)
WHERE
	author_final is NULL;
			
					
/*
3. Wynikajace z przeglądania danych lub innej recznej weryfikacji
*/

---- ponizej niektóre z update'ow

update ids_dict 
SET	author_final = 'Elżbieta Kruk'
where id_='(188, ''b2f24151a54a5f74c125793e00398bb1'')';

update ids_dict 
SET	author_final = 'Adam Abramowicz'
where id_='(1, ''6b52c1248097033ec125793e003986c4'')';

update ids_dict 
SET	author_final = 'Eugeniusz Kłopotek'
where id_='(160, ''19f0d97036d9fbaac125793e00398b07'')';

update ids_dict 
SET	author_final = 'Andrzej Adamczyk'
where id_ in ('8_002','(2, ''b317b7f7e16435e0c125793e003986ca'')');

update ids_dict 
SET	author_final = 'Jerzy Gosiewski'
where id_ in ('(100, ''a9c46e19f8290961c125793e00398961'')');

update ids_dict 
SET	author_final = 'Jerzy Gosiewski'
where id_ in ('(100, ''a9c46e19f8290961c125793e00398961'')');

update ids_dict 
SET	author_final = 'Elżbieta Streker-Dembińska'
where id_ in ('(362, ''319e8177d8002eecc125793e00398fc6'')');




--- ile brakuje
select count(*), count(distinct id_)
from ids_dict
where author_final is null;

--19698	3828
-- 5558	 795

/*
przypisnie do tabeli z tekstami
*/

alter table speeches add author_final TEXT;

update speeches 
SET	
	author_final = (select author_final from ids_dict where ids_dict.id_ = speeches.id_)
where 
	author_final is null;
	
	
select count(*), count(distinct id_)
from speeches
where author_final is not null;



--272221	3828
--225388	3033

select id_, count(*) as ile from speeches
where author_final is NULL
group by id_
order by count(*) desc	

