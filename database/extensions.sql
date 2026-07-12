-- ============================================
-- GlobePay Database Extensions
-- File: 001_extensions.sql
-- Purpose: Enable PostgreSQL extensions required
-- for the GlobePay database.
-- Run this file only once.
-- ============================================

-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Case-insensitive text (useful for emails)
CREATE EXTENSION IF NOT EXISTS citext;