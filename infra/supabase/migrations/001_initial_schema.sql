-- Enable extensions
create extension if not exists vector;
create extension if not exists pg_trgm;  -- for full-text / keyword search

-- Document jobs table (tracks ingestion status)
create table if not exists document_jobs (
    id           uuid primary key default gen_random_uuid(),
    user_id      uuid not null,
    filename     text not null,
    storage_path text not null,
    status       text not null default 'queued',  -- queued|processing|ready|failed
    chunks_stored int,
    error        text,
    created_at   timestamptz default now()
);

-- Chunks table (stores embedded content)
create table if not exists chunks (
    id           uuid primary key default gen_random_uuid(),
    document_id  uuid references document_jobs(id) on delete cascade,
    user_id      uuid not null,
    content      text not null,
    embedding    vector(1536),
    metadata     jsonb default '{}',
    created_at   timestamptz default now()
);

-- HNSW index for vector similarity search
create index if not exists chunks_embedding_hnsw_idx
    on chunks using hnsw (embedding vector_cosine_ops)
    with (m = 16, ef_construction = 64);

-- GIN index for full-text search
create index if not exists chunks_content_fts_idx
    on chunks using gin (to_tsvector('english', content));

-- Row Level Security
alter table document_jobs enable row level security;
alter table chunks enable row level security;

create policy "users see own docs" on document_jobs
    for all using (user_id = auth.uid());

create policy "users see own chunks" on chunks
    for all using (user_id = auth.uid());

-- Vector similarity search function
create or replace function match_documents(
    query_embedding     vector(1536),
    match_count         int default 10,
    similarity_threshold float default 0.5,
    filter_user_id      uuid default null
)
returns table (id uuid, content text, metadata jsonb, similarity float)
language sql stable as $$
    select id, content, metadata,
           1 - (embedding <=> query_embedding) as similarity
    from chunks
    where (filter_user_id is null or user_id = filter_user_id)
      and 1 - (embedding <=> query_embedding) > similarity_threshold
    order by embedding <=> query_embedding
    limit match_count;
$$;

-- Keyword (BM25-like) full-text search function
create or replace function keyword_search_documents(
    query_text      text,
    match_count     int default 5,
    filter_user_id  uuid default null
)
returns table (id uuid, content text, metadata jsonb, similarity float)
language sql stable as $$
    select id, content, metadata,
           ts_rank(to_tsvector('english', content), plainto_tsquery('english', query_text)) as similarity
    from chunks
    where (filter_user_id is null or user_id = filter_user_id)
      and to_tsvector('english', content) @@ plainto_tsquery('english', query_text)
    order by similarity desc
    limit match_count;
$$;
