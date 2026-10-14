# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest?

The easiest were the style and cleanup issues: unused imports and variables, `== None`, missing docstrings, long lines, camelCase names and the missing final newline. Each one had an obvious, local fix that the tool's message described.

The hardest was the cancellation bug, which no tool reported. `cancelBooking("BA202")` added a seat to a flight with no bookings, so the program reported 3 available flights when only 2 had seats. To fix it I had to understand what the program is supposed to do and add a per-flight `booked` count, so that only a real booking can be cancelled. Removing `eval` also took some thought, because it meant changing the function's interface from an expression string to a numeric rate.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Partly. Bandit's B105 flagged `"AIRLINE_DISPATCH_SECRET_TOKEN_2026"` with only medium confidence, because it judges by the variable name. Here it was a real problem, but the same rule would also flag harmless strings in variables whose names contain words like "secret" or "token". Pylint's `unused-variable` warning for `base_fare` was also misleading: the variable *was* used, implicitly, by `eval`. Deleting it as the tool suggested would have broken the program. The real fix was to remove `eval`.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Flake8 and Pylint in a pre-commit hook so style and quality problems are caught before code is committed. In CI I would run Pylint, Flake8 and Bandit on every push or pull request, set a minimum Pylint score, and fail the build on any medium or high Bandit finding. Shared configuration files (`.pylintrc`, `.flake8`) would keep the rules the same for everyone.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** no more `eval`, shell commands, MD5, predictable PINs or hardcoded or printed secrets. Bandit went from 6 findings (2 High) to 0.
- **Correctness:** the phantom-seat bug is gone. BA202 stays full, and the program reports 2 available flights. Cancellations now refund revenue, baggage tags no longer leak between calls, and luggage weight is no longer truncated.
- **Robustness:** errors are no longer silently swallowed, files are always closed, and importing the module no longer runs `main()`.
- **Readability:** consistent snake_case names, docstrings and simpler logic. The Pylint score went from 4.00/10 to 10.00/10, and Flake8 reports no issues.
