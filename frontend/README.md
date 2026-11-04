# AEGIS Dashboard

Next.js frontend for the AEGIS SOC. It reads events, incidents and detection
alerts from the FastAPI backend.

## Running locally

Start the backend first (see the root README), then:

```bash
npm install
npm run dev
```

Open http://localhost:3000.

The API address defaults to `http://localhost:8000`. Set
`NEXT_PUBLIC_API_URL` in `.env.local` to point somewhere else.

## Checks

```bash
npm run lint
npx tsc --noEmit
```
