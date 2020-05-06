
create table Items
(
    item_id   bigint            not null
        constraint Items_pk
            primary key nonclustered,
    item_name varchar(60)       not null,
    min_lvl   int   default 1   not null,
    def_value money default 100 not null,
    use_class varchar(50)       not null,
    dmg       int   default 1   not null
)
go

create index item_id_idx on Items(item_id)

create table Players
(
    player_id    bigint             not null
        constraint players_pk
            primary key nonclustered,
    player_name  varchar(50)        not null,
    player_money money default 1000 not null,
    player_lvl   int   default 1    not null,
    player_class varchar(50)        not null
)
go

create index player_id_idx on Players(player_id)

create table Auctions
(
    auction_id bigint   not null
        constraint Auctions_pk
            primary key nonclustered,
    item_id    bigint   not null
        constraint item_id
            references Items,
    price      money    not null,
    end_time   datetime not null,
    seller_id  bigint
        constraint Auctions_Players_player_id_fk
            references Players
)

create index auction_id_idx on Auctions(auction_id)


