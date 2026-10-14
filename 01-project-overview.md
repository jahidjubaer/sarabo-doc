# Sarabo — Project Overview

## 1. The problem

Getting a phone, laptop, TV, fridge, AC or washing machine repaired in Bangladesh
is usually informal: you find a shop by word of mouth, you don't know the price
before you hand the device over, you can't see where the device is, and there is
no record if something goes wrong.

**Sarabo** is a web platform that turns that into a tracked, priced service:
the customer books a repair online, verified technicians in the same area send
offers, the technician collects and inspects the device, sends a final quote,
repairs it, and the customer pays and follows every step.

## 2. Users (roles)

| Role | Stored value | What they do |
|---|---|---|
| Customer | `user` | Creates repair requests, compares technician offers, pays the inspection fee and the repair, tracks progress, reviews or reports the technician |
| Technician | `rider` | Applies to become a technician (admin approves), browses the jobs board, sends offers, inspects, quotes, repairs, gets paid into a wallet and withdraws via bKash |
| Admin | `admin` | Approves technicians, manages service catalogue and prices, watches overdue/missed pickups, handles refunds and withdrawals, moderates reviews/reports, reads reports |
| Public visitor | — | Sees services, service areas, the open jobs board and can track a repair by tracking code |

## 3. The repair journey (main workflow)

1. **Request** — customer picks device + repair service from the catalogue, describes
   the problem (or lets AI fill the form from a description / damage photo), adds up to
   3 damage photos and picks a 2-hour pickup slot. The request is refused if no
   approved technician in that region can do this repair.
2. **Job portal** — the request appears on the public jobs board. Matching technicians
   are notified and send offers (estimate range + inspection fee + note). A price guide
   and an AI-written note help them.
3. **Choose & book** — customer compares offers and chooses one, paying the inspection
   fee via Stripe. The payment books the technician in one database transaction.
   Customer can reject an offer (job is reposted; technician gets one revised offer).
4. **Pickup & inspection** — technician collects the device and submits an inspection.
5. **Quote** — technician sends a final quote (labour / parts / extra). The customer
   approves and pays the rest (quote minus inspection fee already paid) or declines.
6. **Repair** — progress updates, completion with optional evidence photos.
7. **Handover** — customer confirms receipt; technician earns 90%, Sarabo keeps 10%.
8. **Feedback** — customer rates the technician (1–5) or files a private report.

Status values the request moves through (stored names are inherited from the
original parcel app and frozen):
`pending-pickup → driver_assigned → rider_arriving → parcel_picked_up →
inspection_completed → quote_submitted → quote_approved → payment_completed →
repair_in_progress → repair_completed → parcel_delivered` (or `cancelled`).

Anyone with the tracking code (`SRB-…`) can view a sanitized public timeline.

## 4. Feature list

**Customer**
- Email/password and Google sign-in (Firebase), email verification
- Repair request form with live catalogue estimate, damage photo upload
- AI request helper (Bangla / English / Banglish text and/or photo → form draft)
- Pickup slot scheduling (Sat–Thu, 4 slots/day, capacity per region)
- Compare technician offers, accept / reject, pay inspection fee
- Approve quote and pay in one step; cancel visit (refund rules: ≥2 h before = full refund)
- Public tracking page, notifications (in-app + email), PDF payment receipts
- Reviews and private reports on technicians
- AI customer-support chat

**Technician**
- Application with expertise (device, repairs, level, years) and service area
- Public jobs board with photo cards, filters and sorting
- Offer form with price guide and AI-written note
- Inspection, quote, repair progress and completion workflow
- Wallet: earnings, kept inspection fees, bKash withdrawal requests
- Reviews summary

**Admin**
- Approve / reject technicians, manage user roles
- Service catalogue and price editor (versioned prices)
- Attention list: overdue pickups, missed pickups, unmatchable requests, requests
  with no offers in 24 h, refunds waiting
- Reports page with charts and an AI summary (numbers checked against real data)
- Withdrawal handling (bKash TrxID), review/report moderation

## 5. Architecture

```
 Browser (React SPA, hosted on Vercel)
     │  Firebase ID token in Authorization header
     ▼
 Express 5 API (Vercel serverless) ──► MongoDB Atlas (transactions)
     │                               ├► Firebase Admin (verify tokens)
     │                               ├► Stripe (Checkout, webhook, refunds)
     │                               ├► Supabase Storage (private damage photos, signed URLs)
     │                               ├► Google Gemini (support chat, request helper,
     │                               │                 offer note, report summary)
     │                               └► Gmail SMTP (email updates)
     ▼
 Vercel Cron (daily pickup reminders, auto-close declined quotes)
```

- Client: `sarabo-client` — ~337 source files, ~28.7k lines
- Server: `sarabo-server` — ~189 JS files, ~45.1k lines (including tests)
- Production: client `https://sarabo-client-six.vercel.app`, server `https://sarabo-server.vercel.app` (both on Vercel, deployed on push to `main`; the old Firebase site `https://sarabo-jahid.web.app` is no longer updated)

## 6. Technology stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite 7, React Router 7, TanStack Query 5 & Table, Tailwind CSS 4, Radix UI, react-hook-form, Recharts, Leaflet (service-area map), Motion, react-joyride (product tour) |
| Backend | Node.js, Express 5, MongoDB driver 7, express-rate-limit |
| Auth | Firebase Authentication (client) + Firebase Admin (server) |
| Payments | Stripe Checkout (test mode), webhooks, refunds; bKash for technician payouts (manual) |
| Storage | Supabase Storage (private bucket, signed upload/read URLs) |
| AI | Google Gemini (`@google/genai`) |
| Email | Nodemailer via Gmail |
| PDF | pdfkit (receipts) |
| Testing | Server integration test suites (`npm test`), Playwright browser tests (client) |
| CI/CD | GitHub Actions (lint, build, tests on a throwaway MongoDB); Vercel (server and client) |

## 7. Notable engineering points (good material for the report)

- **Transactions everywhere money or assignment changes** — booking, approval,
  completion, settlement and refunds are single MongoDB transactions, so a partial
  failure never leaves inconsistent data. Double booking is prevented.
- **Stripe webhook is the source of truth** for "paid", signature-verified;
  idempotency keys stop double refunds; failed refunds stay "pending" and can be retried.
- **Security** — Firebase token auth, role checks on the server, rate limiting
  (Mongo-backed so it works across serverless instances), CORS allow-list, sanitized
  public tracking (no names/emails/payment data), 128-bit random tracking codes,
  private photo bucket with short-lived signed URLs, safe logging (no request bodies).
- **AI with guard-rails** — AI can only pick ids from the live catalogue, never sets
  prices, strips contact details, and the admin summary drops any sentence containing
  a number not present in the real data. Per-user and site-wide daily limits.
- **Money rules** — inspection fee credited toward the final quote; 90/10 split;
  cancellation refund policy; whole-taka rounding.
- **Region-based matching** — requests only allowed where a qualified technician exists;
  turned-away demand is counted (hashed, 180-day TTL) for admin reports.
- **Migration from a parcel-delivery codebase** ("zap_shift") to a repair domain,
  done in safe phases with dry-run-first scripts and production guards.

## 8. Existing documentation in the repos

- `sarabo-client/README.md`, `sarabo-client/docs/ui-redesign.md`
- `sarabo-server/SETUP.md`
- `sarabo-server/docs/`: data-model glossary, job portal & inspection fee, AI request
  helper, AI offer helper, AI report summary, feedback backend, production runbook,
  production data migration, local QA guide
