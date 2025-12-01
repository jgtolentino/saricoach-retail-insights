-- 1. Stores Table
create table if not exists stores (
  id bigint primary key generated always as identity,
  name text not null,
  owner_name text,
  created_at timestamptz default now()
);

-- 2. Daily Metrics (The "Hard" Data)
create table if not exists daily_metrics (
  id bigint primary key generated always as identity,
  store_id bigint references stores(id),
  date date not null,
  volume int default 0,
  revenue numeric(10, 2) default 0,
  avg_basket_size numeric(5, 2) default 0,
  avg_duration_seconds int default 0,
  unique (store_id, date) -- prevent duplicate entries for same day
);

-- 3. Hourly Traffic (For the chart)
create table if not exists hourly_traffic (
  id bigint primary key generated always as identity,
  store_id bigint references stores(id),
  date date not null,
  hour_of_day int not null check (hour_of_day between 0 and 23),
  volume int default 0
);

-- 4. AI Insights & Coaching (The "Soft" Data)
create table if not exists daily_insights (
  id bigint primary key generated always as identity,
  store_id bigint references stores(id),
  date date not null,
  insights text[], -- Array of strings
  coach_message text,
  created_at timestamptz default now()
);
