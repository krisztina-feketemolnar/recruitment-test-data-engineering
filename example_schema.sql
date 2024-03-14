drop table if people examples;

create table `people` (
  `id` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `place_of_birth` int default null, --there can be places with same name but in different countriey, so I use id 
  primary key (`id`)
);

--people
--given_name,family_name,date_of_birth,place_of_birth

--places
--city,county,country