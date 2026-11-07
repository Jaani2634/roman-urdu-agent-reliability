# Missing tasks (unmeasured runs)

Five of the 80 planned runs could not be measured. Each was attempted 5 times; every attempt returned an API error (HTTP 503 Service Unavailable). They are recorded as unmeasured, not deleted, and the paper reports the range they imply.

| Task | Condition | Attempts | Errors |
|---|---|---|---|
| B10 | real | 5 | attempt 1: HTTPError: HTTP Error 503: Service Unavailable; attempt 2: HTTPError: HTTP Error 503: Service Unavailable; attempt 3: HTTPError: HTTP Error 503: Service Unavailable; attempt 4: HTTPError: HTTP Error 503: Service Unavailable; attempt 5: HTTPError: HTTP Error 503: Service Unavailable |
| D2 | benchmark | 5 | attempt 1: HTTPError: HTTP Error 503: Service Unavailable; attempt 2: HTTPError: HTTP Error 503: Service Unavailable; attempt 3: HTTPError: HTTP Error 503: Service Unavailable; attempt 4: HTTPError: HTTP Error 503: Service Unavailable; attempt 5: HTTPError: HTTP Error 503: Service Unavailable |
| D3 | benchmark | 5 | attempt 1: HTTPError: HTTP Error 503: Service Unavailable; attempt 2: HTTPError: HTTP Error 503: Service Unavailable; attempt 3: HTTPError: HTTP Error 503: Service Unavailable; attempt 4: HTTPError: HTTP Error 503: Service Unavailable; attempt 5: HTTPError: HTTP Error 503: Service Unavailable |
| D3 | real | 5 | attempt 1: HTTPError: HTTP Error 503: Service Unavailable; attempt 2: HTTPError: HTTP Error 503: Service Unavailable; attempt 3: HTTPError: HTTP Error 503: Service Unavailable; attempt 4: HTTPError: HTTP Error 503: Service Unavailable; attempt 5: HTTPError: HTTP Error 503: Service Unavailable |
| D5 | benchmark | 5 | attempt 1: HTTPError: HTTP Error 503: Service Unavailable; attempt 2: HTTPError: HTTP Error 503: Service Unavailable; attempt 3: HTTPError: HTTP Error 503: Service Unavailable; attempt 4: HTTPError: HTTP Error 503: Service Unavailable; attempt 5: HTTPError: HTTP Error 503: Service Unavailable |

Effect on the headline rates: if all five had passed, the benchmark rate would be 95.0% and the real-world rate 90.0%; if all five had failed, 87.5% and 85.0%. The reported rates (94.6% and 89.5%) sit inside those ranges.
