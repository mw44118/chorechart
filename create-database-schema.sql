begin;

create table theme
(
    theme_id serial primary key,
    title text,
    empty_star_html text,
    filled_in_star_html text,
    embedded_video text
);

create table chart
(
    chart_id serial primary key,
    facebook_uid text not null,
    title text,
    theme_id integer references theme (theme_id),

    number_of_stars integer not null
    check (number_of_stars > 0),

    stars_filled_in integer not null default 0
    check (stars_filled_in <= number_of_stars),

    created timestamp with time zone not null default now()

);

create unique index on chart (facebook_uid, title);

commit;
