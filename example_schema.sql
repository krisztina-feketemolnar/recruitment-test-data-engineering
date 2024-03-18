
-- drop table ef if exists commands

drop table if exists codetest.`people`;


drop table if exists codetest.`places`;

-- create table commands
create table codetest.`places` (
  `city` varchar(80) not null,
  `county` varchar(80) default null,
  `country` varchar(80) not null,
  primary key (`city`,`country`)
);

create table codetest.`people` (
  `id` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `place_of_birth` varchar(80) not null, 
  primary key (`id`),
  foreign key (`place_of_birth`) references `places`(`city`)
);


select count(*) from codetest.places;

select count(*) from codetest.people;

-- It should consist of a list of the countries, and a count of how many people were born in that country. 
select p2.country, count(p.place_of_birth)
from codetest.people p 
inner join codetest.places p2 on p.place_of_birth  = p2.city 
group by p2.country
