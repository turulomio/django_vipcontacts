 SELECT 
    distinct(id,  search)
 FROM (
    select 
        persons.id, 
        persons.name || ' ' || 
        persons.surname || ' ' || 
        persons.surname2 || ' '|| 
        mails.mail  || ' '|| 
        phones.phone  || ' '|| 
        adresses.address || ' '|| 
        adresses.city  || ' '|| 
        adresses.code 
        
        as search
    from
        persons,  
        mails,  
        phones, 
        adresses
    WHERE
    
    persons.id = mails.person_id AND
    persons.id=adresses.person_id AND
    persons.id=phones.person_id 
 ) as s
  WHERE 
    search ilike '%Mariano%'
;
