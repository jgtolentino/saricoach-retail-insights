-- saricoach core schema for SariCoach
create schema if not exists saricoach;

-- BRANDS
create table if not exists saricoach.brands (
  brand_id      integer primary key,
  brand_name    text not null,
  category      text
);

-- STORES
create table if not exists saricoach.stores (
  store_id      integer primary key,
  store_name    text not null,
  region        text,
  city          text,
  barangay      text,
  store_type    text
);

-- PRODUCTS (supports SKU / barcode / pack)
create table if not exists saricoach.products (
  product_id    integer primary key,
  sku           text,
  barcode       text,
  brand_id      integer not null,
  product_name  text not null,
  category      text,
  pack_size     text,
  pack_type     text,
  constraint products_brand_fk
    foreign key (brand_id)
    references saricoach.brands (brand_id)
    on delete restrict
);

-- TRANSACTIONS (header)
create table if not exists saricoach.transactions (
  transaction_id  text primary key,
  store_id        integer not null,
  tx_timestamp    timestamp without time zone not null,
  total_amount    double precision,
  constraint transactions_store_fk
    foreign key (store_id)
    references saricoach.stores (store_id)
    on delete restrict
);

-- TRANSACTION LINES (detail)
create table if not exists saricoach.transaction_lines (
  transaction_id  text not null,
  line_no         integer not null,
  product_id      integer,
  brand_id        integer,
  quantity        integer,
  price_unit      double precision,
  subtotal        double precision,
  constraint transaction_lines_pkey
    primary key (transaction_id, line_no),
  constraint tl_transaction_fk
    foreign key (transaction_id)
    references saricoach.transactions (transaction_id)
    on delete cascade,
  constraint tl_product_fk
    foreign key (product_id)
    references saricoach.products (product_id)
    on delete set null,
  constraint tl_brand_fk
    foreign key (brand_id)
    references saricoach.brands (brand_id)
    on delete set null
);

-- SHELF VISION EVENTS
create table if not exists saricoach.shelf_vision_events (
  id               text primary key,
  store_id         integer not null,
  event_timestamp  timestamp without time zone not null,
  brand_id         integer not null,
  facings          integer,
  share_of_shelf   double precision,
  oos_flag         boolean,
  confidence       double precision,
  constraint sve_store_fk
    foreign key (store_id)
    references saricoach.stores (store_id)
    on delete cascade,
  constraint sve_brand_fk
    foreign key (brand_id)
    references saricoach.brands (brand_id)
    on delete cascade
);

-- STT EVENTS
create table if not exists saricoach.stt_events (
  id               text primary key,
  store_id         integer not null,
  event_timestamp  timestamp without time zone not null,
  brand_id         integer,
  raw_text         text,
  intent_label     text,
  sentiment_score  double precision,
  constraint stt_store_fk
    foreign key (store_id)
    references saricoach.stores (store_id)
    on delete cascade,
  constraint stt_brand_fk
    foreign key (brand_id)
    references saricoach.brands (brand_id)
    on delete set null
);

-- WEATHER
create table if not exists saricoach.weather_daily (
  id            text primary key,
  store_id      integer not null,
  date          date not null,
  temp_c        double precision,
  rainfall_mm   double precision,
  condition     text,
  constraint weather_store_fk
    foreign key (store_id)
    references saricoach.stores (store_id)
    on delete cascade
);

-- FOOT TRAFFIC
create table if not exists saricoach.foot_traffic_daily (
  id            text primary key,
  store_id      integer not null,
  date          date not null,
  traffic_index double precision,
  constraint ft_store_fk
    foreign key (store_id)
    references saricoach.stores (store_id)
    on delete cascade
);

-- INDEXES for typical SariCoach queries

-- per-store / time-series joins
create index if not exists idx_tx_store_ts
  on saricoach.transactions (store_id, tx_timestamp);

create index if not exists idx_sve_store_brand_ts
  on saricoach.shelf_vision_events (store_id, brand_id, event_timestamp);

create index if not exists idx_stt_store_brand_ts
  on saricoach.stt_events (store_id, brand_id, event_timestamp);

create index if not exists idx_weather_store_date
  on saricoach.weather_daily (store_id, date);

create index if not exists idx_traffic_store_date
  on saricoach.foot_traffic_daily (store_id, date);

create index if not exists idx_tl_brand_product
  on saricoach.transaction_lines (brand_id, product_id);
