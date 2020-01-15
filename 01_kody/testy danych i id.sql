select count(*) from sp2 where author is null;


select id_, count(*), count(distinct author) autor from sp2 group by id_ order by autor desc

select * from sp2 where id_='8_342'

select * from speech_data where id_ not in (select id_ from portraits)

select * from sp2 where autor_by_id<>author

select id_, autor_by_id, author, count(*) from sp2 group by id_, autor_by_id, author
select * from sp2 where date_='08-06-2011' and number_='19 i 20'

select distinct id_, autor_by_id, author from sp2 
select * from portraits where id_='(13, ''86630af3c418a6c0c125793e0039870e'')'	or full_name like '%Babalski'


select * from sp2 where id_ ='(10, ''7c644b3853fc19d1c125793e00398700'')' order by date_