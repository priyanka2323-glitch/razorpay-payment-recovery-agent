# Failure code: bank_timeout
## What it means

The payment gateway or customer's bank failed to process the transaction due to a network or server timeout.

## Recommended recovery sequence

1. Wait 2–4 hours before retrying (bank network issues usually resolve quickly)

2. First retry: same payment method, same amount

3. If it fails again, wait 12–24 hours for a second retry

4. If 2 retries fail, send a notification/reminder via preferred channel asking the customer to check back or attempt manual payment

5. 
Max 3 automated attempts, then escalate to human

## Timing rules

Space retries by at least 2 hours to avoid repeated gateway congestion

Avoid retrying during peak bank batch processing hours (midnight–3 AM)

## Compliance notes

Do not contact if customer has DND flag set

Max 2 reminder messages per week per customer