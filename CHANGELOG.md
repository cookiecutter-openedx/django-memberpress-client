# CHANGE LOG

## Version 1.0.4 (2023-11-09)

- Add support for retrieving a Member by user_id

## Version 1.0.3 (2023-03-29)

- fix caching to include query parameters in cache key

## Version 1.0.2 (2023-02-15)

- fix webhooks api to receive post requests

## Version 1.0.1 (2022-12-20)

- standardize usage of python3 in Makefile

## Version 1.0.0 (2022-12-20)

- general production release

## Version 0.0.13 (2022-11-21)

- bug fixes.

## Version 0.0.11 (2022-10-28)

- bug fixes. remove django-environ and validators from INSTALLED_APPS
- bug fixes. change django version requirement to >= 3.2

## Version 0.0.6 (2022-10-17)

- validate event.setter against MemberpressEvents.all_events()
- validate event_type.setter against MemberpressEventTypes.all_event_types()
- add more event tests
- create .env-sample for local and production

## Version 0.0.5 (2022-10-17)

- Add webhook event classes, listener and model
- Create base class Membership() and refactor
- Build unit tests for api and webhook events
- Create a Makefile

## Version 0.0.4 (2022-10-14)

- Operational but experimental plugin. Do not use in production.
- Implements REST API only.
- All redundant code moved to the base class
- Added should_raise_paywall property

## Version 0.0.2 (2022-10-13)

- Experimental plugin. Do not use in production.
