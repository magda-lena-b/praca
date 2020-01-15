----- czyszczenie danych

-- 01 usuniecie pustych rekordow (bez tresci przemowienia)
delete from speeches where speech_raw='None'

--------->	100 rows affected