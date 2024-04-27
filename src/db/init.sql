create table if not exists users (
    id integer primary key,
    username text not null unique,
    password text not null
);

create table if not exists groups (
    id integer primary key,
    name text not null
);

create table if not exists groups_users (
    group_id integer not null,
    user_id integer not null,
    balance float not null default 0,
    constraint fk_users
        foreign key (user_id)
            references users(id)
    constraint fk_groups
        foreign key (group_id)
            references groups(id)
);

create table if not exists split_history (
    id integer primary key,
    created_at float not null,
    group_id integer not null,
    doer_id integer not null,
    lander_id integer not null,
    payer_ids string not null, -- JSON array as "[1, 2, 3]"
    amount integer not null,
    constraint fk_lander
        foreign key (lander_id)
            references users(id)
    constraint fk_doer
        foreign key (doer_id)
            references users(id)
    constraint fk_group
        foreign key (group_id)
            references groups(id)
)