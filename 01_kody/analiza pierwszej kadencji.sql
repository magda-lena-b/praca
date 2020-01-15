create table term1 as
select *
from speeches
where term=1;

--informacje podstawowe
select 
	count(*) as row_cnt,
	count(distinct id_) as id_cnt,
	count(distinct date_) as date_cnt,
	count(distinct session_number) as sesion_cnt,
	count(distinct speech_title) as speech_cnt
from 
	term1

create table term1_names as	
select id_, autor_by_id, author, count(*) as ile
from term1
group by id_	

select autor_by_id, count(*) from term1_names group by autor_by_id 
having count(*)>1