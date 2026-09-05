# Failure Code: insufficient_funds

## What it means
Customer's account/card didn't have enough balance at the time of charge.

## Recommended recovery sequence
1. Wait 24-48 hours before retry (salary/balance often refreshes)
2. First retry: same payment method, same amount
3. If fails again, send a reminder via preferred channel with a "retry payment" link
4. If 2 retries fail, offer alternate payment method (UPI, different card)
5. Max 3 automated attempts, then escalate to human

## Timing rules
- Never retry more than once per 24 hours
- Avoid retrying on weekends for salaried customers (lower success rate)

## Compliance notes
- Do not contact if customer has DND flag set
- Max 2 reminder messages per week per customer