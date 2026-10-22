-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create Items Table
CREATE TABLE IF NOT EXISTS public.items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- Index for RLS and sorting
CREATE INDEX IF NOT EXISTS items_user_id_created_at_idx ON public.items(user_id, created_at DESC);

-- Enable Row Level Security
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own items"
ON public.items FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own items"
ON public.items FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own items"
ON public.items FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own items"
ON public.items FOR DELETE
USING (auth.uid() = user_id);
