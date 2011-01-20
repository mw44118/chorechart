begin;

create table Parent
(

    parent_id serial primary key,
    title text
);

create table Chart
(
    chart_id serial primary key,
    parent_id integer references Parent (parent_id),
    title text,

    number_of_stars integer not null
    check (number_of_stars > 0),

    stars_filled_in integer not null default 0
    check (stars_filled_in <= number_of_stars),

    created timestamp with time zone not null default now()

);

commit;
