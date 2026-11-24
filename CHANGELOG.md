# Changelog

This library follows [semantic versioning](https://semver.org). The API is versioned by date; see the README.

## 2.1.0 (2026-11-25)

- `read_passport`: a passport read from a photo or scan of its identity page and machine-readable zone (POST /passports). Clean fields:
  names, passport number, nationality and issuing state as two-letter codes, dates as yyyy-mm-dd; `read` and `unread` list them.
- `read_id_card`: Pakistan's CNIC and NICOP read from photos (POST /id-cards): the identity number, name, father's or husband's name,
  gender, dates, family number and English addresses, checked for consistency.
- `get_submission_account`: the government portal sign-in for a UK or Canada submission, read fresh each time.
- Website applications: list_visit_slots, submit_site_application, track_site_application, join_site_list, list_site_applications, get_member_card.
- Uploads: the API now reads a file's type from its bytes, so images sent through the library (which labels every upload as a
  PDF) are read as images.

## Unreleased

- The repository moved to the Opaige organisation: github.com/opaige. Old links redirect.
- README: authentication, every method by area, errors and their codes, retries, rate limits, webhooks, versions and support.
- Runnable examples in `examples/`: a quick start against the public test key, and webhook verification.
- SECURITY.md: how to report a vulnerability and how to use the library safely.

## 1.1.0 (2026-11-03)

- New calls: Canada forms (IMM 5257 and IMM 5707), government filing, students, visa-centre appointments, bookings and the
  newer endpoints of the API reference.

## 1.0.1 (2026-11-03)

- Package metadata links to the repository.

## 1.0.0 (2026-11-03)

- First release: every call of the Opaige API, typed errors, retries with idempotency keys, and webhook verification.
