# Day 5 Deliverable: HTTP, REST and Postman

## Learning objectives

- Practice HTTP methods, JSON request and response bodies, status codes, and token authentication.
- Use Postman environment variables and test scripts for status, response structure, and response time.
- Exercise positive, negative, and CRUD workflow behavior on the Restful Booker demo API.

## Files

- [`restful_booker_collection.json`](restful_booker_collection.json): Postman v2.1 collection with auth, read, negative, and CRUD requests.
- [`restful_booker_environment.json`](restful_booker_environment.json): environment template. The username and password values are blank intentionally.

The CRUD workflow creates a booking, reads and updates it, then deletes the
same booking ID. The last request confirms deletion. The invalid update is
expected to return 400; an unauthenticated update is expected to return 403.
Restful Booker returns a reason in the body for invalid `/auth` credentials
(with its demo response status 200), so the collection does not assert 401 for
that request. This follows the demo API's behavior rather than assuming every
service uses the same status code. The project's [route implementation](https://github.com/mwinteringham/restful-booker/blob/master/routes/index.js#L422-L448) returns 403 for unauthenticated writes and 400 for invalid PUT data; its [auth route](https://github.com/mwinteringham/restful-booker/blob/master/routes/index.js#L641-L651) returns a `reason` body for bad credentials. The [booking route](https://github.com/mwinteringham/restful-booker/blob/master/routes/index.js#L250-L310) documents the nested create response, and the [validation rules](https://github.com/mwinteringham/restful-booker/blob/master/helpers/validationrules.js#L1-L10) define required fields.

## Import and run in Postman

1. Import both JSON files into Postman.
2. Select **Day 5 - Restful Booker Demo** as the active environment.
3. Set `username` to the demo account `admin` and `password` to the publicly documented demo password `password123`. These values are not saved in the checked-in environment template.
4. Open the collection's Runner, select the collection and environment, and run the requests in their listed order.
5. Review each request's status, JSON checks, and collection-level response-time check. The default response-time limit is 5000 ms; change `maxResponseTimeMs` in the environment if needed and explain the chosen threshold.
6. From the run results, export the run report as JSON if you need the workbook's Collection Runner evidence. Keep an actual export from your own run; no sample run report is fabricated here.

The API is a shared public demo service, so its availability and data can
change. The collection only deletes the booking ID it creates. If a run stops
after creation before the delete request completes, remove that test booking
manually using its saved `bookingId`.

## Verification record

To be completed after importing and running the collection in Postman. The
collection and environment files have been checked as JSON; the API requests
have not been executed from Postman in this environment. Node.js also checked
the syntax of all 13 embedded test scripts. A valid collection file does not
prove the external service will respond as expected.

## Week 1 self-rating

The workbook asks you to rate the Week 1 skills yourself. Update the Skills
sheet after reviewing what you can explain and demonstrate; ratings are left
blank rather than inferred from generated files.
