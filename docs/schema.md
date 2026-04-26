# Database Schema Reference

This document describes the schema in human terms. The authoritative source is [`backend/alembic/versions/0001_initial_schema.py`](../backend/alembic/versions/0001_initial_schema.py).

## Tables

### `users`

| Column          | Type           | Notes                                              |
|-----------------|----------------|----------------------------------------------------|
| `id`            | UUID PK        |                                                    |
| `username`      | varchar(30)    | unique, public-facing                              |
| `email`         | varchar(255)   | unique, never displayed publicly                   |
| `password_hash` | varchar(255)   | bcrypt; nullable if `google_id` set                |
| `google_id`     | varchar(255)   | unique, nullable                                   |
| `bio`           | text           | optional                                           |
| `avatar_url`    | text           | optional                                           |
| `reputation`    | int            | derived from upvotes; updated via triggers/jobs    |
| `is_verified`   | bool           | email verified                                     |
| `is_admin`      | bool           |                                                    |
| `created_at`    | timestamptz    |                                                    |

### `farms`

The core directory entity. One row per farm/supplier.

| Column                | Type                       | Notes                                                              |
|-----------------------|----------------------------|--------------------------------------------------------------------|
| `id`                  | UUID PK                    |                                                                    |
| `name`                | varchar(255)               | display name                                                       |
| `slug`                | varchar(255)               | unique, URL-safe                                                   |
| `alt_names`           | jsonb                      | array of alternative names ("Amos Miller", etc.)                   |
| `description`         | text                       |                                                                    |
| `address_line1`       | varchar(255)               | nullable (some farms phone-only)                                   |
| `city`                | varchar(100)               |                                                                    |
| `state`               | varchar(50)                |                                                                    |
| `zip`                 | varchar(20)                |                                                                    |
| `country`             | varchar(50)                | default 'USA'                                                      |
| `location`            | GEOGRAPHY(POINT, 4326)     | PostGIS — for map queries                                          |
| `website`             | text                       |                                                                    |
| `phone`               | varchar(50)                |                                                                    |
| `email`               | varchar(255)               |                                                                    |
| `support_email`       | varchar(255)               | separate support contact, if any                                   |
| `contact_person`      | varchar(255)               | useful for small farms ("Mervin Esh")                              |
| `status`              | varchar(20)                | `active`, `closed`, `unknown`                                      |
| `verification_level`  | varchar(20)                | `aajonus_verified`, `dev_recommended`, `community_verified`, `unverified` |
| `verification_source` | text                       | citation text                                                      |
| `submitted_by`        | UUID FK → users            | nullable for seed data                                             |
| `approved_by`         | UUID FK → users            | nullable                                                           |
| `is_approved`         | bool                       |                                                                    |
| `created_at`          | timestamptz                |                                                                    |
| `updated_at`          | timestamptz                |                                                                    |

### `farm_products`

What each farm sells. Many products per farm.

| Column           | Type           | Notes                                                                |
|------------------|----------------|----------------------------------------------------------------------|
| `id`             | UUID PK        |                                                                      |
| `farm_id`        | UUID FK        | cascade delete                                                       |
| `product_type`   | varchar(50)    | controlled vocab — see seed data `_meta.product_types`               |
| `notes`          | text           | "specify single-grind", "no-salt option in glass", etc.              |
| `must_specify`   | text           | what to write at checkout, separate from general notes               |
| `price_per_unit` | varchar(50)    | "$8.50–$15.00" — string because ranges and per-unit vary             |
| `unit`           | varchar(20)    | "lb", "jar", "dozen", etc.                                           |

### `farm_fulfillment`

How customers can buy.

| Column   | Type        | Notes                                                              |
|----------|-------------|--------------------------------------------------------------------|
| `id`     | UUID PK     |                                                                    |
| `farm_id`| UUID FK     | cascade delete                                                     |
| `method` | varchar(50) | `in_person`, `herd_share`, `ships_nationwide`, `ships_regional`, `local_delivery` |

### `farm_tips`

Sourcing tips per farm — the operational knowledge that makes the directory valuable.

| Column         | Type         | Notes                                                              |
|----------------|--------------|--------------------------------------------------------------------|
| `id`           | UUID PK      |                                                                    |
| `farm_id`      | UUID FK      | cascade delete                                                     |
| `tip_type`     | varchar(50)  | `checkout_note`, `phone_script`, `shipping`, `insider`, `warning`  |
| `title`        | varchar(255) |                                                                    |
| `body`         | text         |                                                                    |
| `upvotes`      | int          | derived from `votes` table                                         |
| `submitted_by` | UUID FK      | nullable for seed                                                  |
| `created_at`   | timestamptz  |                                                                    |

### `farm_citations`

Links to primary sources (aajonus.net pages, books). Never reproduces copyrighted text.

| Column          | Type         | Notes                                                              |
|-----------------|--------------|--------------------------------------------------------------------|
| `id`            | UUID PK      |                                                                    |
| `farm_id`       | UUID FK      | cascade delete                                                     |
| `source_type`   | varchar(50)  | `book`, `audio`, `website`, `interview`                            |
| `source_name`   | varchar(255) | "We Want To Live", "aajonus.net Q&A 2009-09-13"                    |
| `source_detail` | varchar(255) | page number, timestamp, etc.                                       |
| `source_url`    | text         | direct link if web                                                 |
| `quote`         | text         | brief paraphrased context — never the full original passage        |
| `verified`      | bool         | maintainer-checked                                                 |

### `farm_verifications`

Community check-ins keeping the directory fresh. Different from `reviews` — these are factual updates ("still operating", "they raised prices"), not opinions.

| Column      | Type        | Notes                                                              |
|-------------|-------------|--------------------------------------------------------------------|
| `id`        | UUID PK     |                                                                    |
| `farm_id`   | UUID FK     | cascade delete                                                     |
| `user_id`   | UUID FK     |                                                                    |
| `status`    | varchar(20) | `still_operating`, `prices_changed`, `closed`, `products_changed`  |
| `notes`     | text        |                                                                    |
| `created_at`| timestamptz |                                                                    |

### `reviews`

Subjective reviews of farms.

| Column             | Type        | Notes                                          |
|--------------------|-------------|------------------------------------------------|
| `id`               | UUID PK     |                                                |
| `farm_id`          | UUID FK     | cascade delete                                 |
| `user_id`          | UUID FK     |                                                |
| `rating`           | smallint    | 1–5, check constraint                          |
| `title`            | varchar(255)|                                                |
| `body`             | text        |                                                |
| `purchase_method`  | varchar(50) | how they bought                                |
| `product_purchased`| varchar(100)|                                                |
| `created_at`       | timestamptz |                                                |
| `updated_at`       | timestamptz |                                                |

### `forum_categories`, `threads`, `posts`

Forum data. Standard nested structure: a category contains threads, a thread contains posts (replies).

### `votes`

Polymorphic voting — works for threads, posts, reviews, tips. Unique constraint on `(user_id, target_type, target_id)`.

## Indexes

- `farms.location` — GIST index (PostGIS)
- `farms.state`, `farms.verification_level` — for filter queries
- `threads.last_activity_at DESC` — sort hot/new feeds
- `posts.thread_id` — load thread by id

## Triggers / derived data

For v1, derived columns (`reputation`, `upvotes`, `reply_count`) update via application code rather than DB triggers. Simpler to debug. Move to triggers if performance demands.
