# Streaming Platform Demo

A video streaming demo platform to show if VPN Detector works properly.
This platform provides video following the HLS protocol.

## API

The following api is being utilized: https://developers.themoviedb.org/3/getting-started/introduction

## How to run

1. Install dependencies

This project uses pnpm as package manager. To install it, run the following command:

```bash
npm install -g pnpm
```

Then, install the dependencies:

```bash
pnpm install
```

2. Run the project

in order to run the project, you should have necessary credentials. otherwise, you cannot run the project.

if you are not a developer of this project, please contact the developer to get the credentials.

necessary credentials are specified in the `.env` file. please create `.env` file in the root directory of this project and specify the credentials as follows:

```bash
NEXT_PUBLIC_THE_MOVIE_DB_V3_API_KEY=
NEXT_PUBLIC_THE_MOVIE_DB_V3_BASE_URL=

NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_SUPABASE_URL=
```

## Blacklist Database

This project uses Supabase as a database. The database is closed to the public. If you want to access the database, please contact the developer.
