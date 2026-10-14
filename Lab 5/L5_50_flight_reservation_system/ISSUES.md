# Issues — Flight Reservation System

Line numbers refer to the original `flight_reservation_system.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (`os.system`) | Security (Bandit B605, High) | 63 | `os.system("echo ... " + filename)` passes a caller-controlled filename to the shell, so a name like `x; rm -rf ~` runs arbitrary commands. | Removed the shell call; use `print()` to report the export. |
| Weak hash (MD5) | Security (Bandit B324, High) | 52 | MD5 is broken and unsuitable for hashing passenger identifiers. | Replaced with `hashlib.sha256`. |
| Use of `eval` | Security (Bandit B307 Medium, Pylint W0123) | 47 | `calculateBaggageFee` evaluates an arbitrary string, allowing code execution. `base_fare` only looked unused because `eval` reads it implicitly. | Take a numeric `surcharge_rate` and compute `base_fare * float(surcharge_rate)`. |
| Cancelling a flight with no bookings creates a phantom seat | Logic bug (not flagged by tools) | 27–32, 77 | `cancelBooking("BA202")` adds a seat to a flight nobody booked and marks it not full, so the output shows `Available flights: 3` and the manifest has BA202 with 1 seat and `is_full: False`. | Track a `booked` count per flight and only cancel when `booked > 0`. Revenue is refunded on cancellation. The output now correctly shows 2 available flights. |
| Hardcoded secret printed to stdout | Security (Bandit B105) | 75, 84 | The API token is in the source code and printed to the console. | Removed the hardcoded token and the print. |
| Bare `except: pass` | Error handling (Pylint W0702, Flake8 E722, Bandit B110) | 31–32 | All errors are silently hidden, including an unknown flight number. | Check the flight with `flights.get()` explicitly and return `False` on failure. |
| Mutable default argument | Bug (Pylint W0102) | 15 | `baggage_tags=[]` is shared between every call, so tags pile up across bookings. | Default to `None` and create a new list inside the function. |
| Insecure random for boarding PIN | Security (Bandit B311, Low) | 56 | `random` is predictable and not suitable for security tokens. | Use `secrets.randbelow(9000) + 1000`. |
| Luggage weight truncated | Logic bug (not flagged by tools) | 23 | `%d` truncates a fractional weight (e.g. 20.7 kg logged as 20). | Use an f-string that keeps the actual value. |
| Global state mutated through `global` | Style/design (Pylint W0603, C0103) | 12, 16 | `total_revenue` is changed through a `global` statement. | Store revenue in a module-level dict (`revenue["total"]`). |
| File opened without `with` / encoding | Resource handling (Pylint R1732, W1514) | 60–62 | The file is not closed if `write` fails, and the encoding depends on the platform. | `with open(filename, "w", encoding="utf-8")`. |
| Unused import / variables | Code quality (Pylint W0611/W0612, Flake8 F401/F841) | 4, 36, 68 | `math`, `airport_fee` and loop variable `f` are unused. | Removed them. |
| Parameter shadows global | Code quality (Pylint W0621) | 66 | The `flights` parameter hides the module-level `flights`. | Renamed it to `flight_data`. |
| `== None` comparison, redundant if/else | Style (Pylint C0121/R1703/R1705, Flake8 E711) | 37–42 | Non-idiomatic None check and boolean return. | `is None` and `return not flight["is_full"]`. |
| Non-snake_case names, missing docstrings | Style (Pylint C0103/C0114/C0116) | 1, 15–74 | camelCase function names, and no module or function docstrings. | Renamed to snake_case and added docstrings. |
| Long lines, missing final newline, `%` formatting | Style (Flake8 E501/W292, Pylint C0301/C0304/C0209) | 7–9, 23, 87 | Lines exceed limits, the file has no trailing newline, and it uses old-style formatting. | Wrapped lines, added a newline, and used f-strings. |
| `main()` runs on import | Code quality (not flagged by tools) | 87 | Importing the module runs the whole workflow. | Wrapped the call in `if __name__ == "__main__":`. |

**Result:** Pylint 4.00/10 → 10.00/10. Flake8 and Bandit report no issues.
