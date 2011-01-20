begin;

create table parent
(

    parent_id serial primary key,
    title text
);

create table theme
(
    theme_id serial primary key,
    title text,
    embedded_video text
);

create table chart
(
    chart_id serial primary key,
    parent_id integer references Parent (parent_id),
    title text,
    theme_id integer references theme (theme_id),

    number_of_stars integer not null
    check (number_of_stars > 0),

    stars_filled_in integer not null default 0
    check (stars_filled_in <= number_of_stars),

    created timestamp with time zone not null default now()

);

create unique index on chart (parent_id, title);

commit;
