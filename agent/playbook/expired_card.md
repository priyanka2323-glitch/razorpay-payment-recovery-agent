# Failure Code: expired_card

## What it means

The customer's credit or debit card past its expiration date and cannot accept auto-debit charges.

## Recommended recovery sequence

1. Do NOT attempt immediate retries on the expired card

2. Send an urgent reminder via preferred channel with an "update payment method" link

3. Wait 48 hours for customer action

4. If no update after 48 hours, send a follow-up reminder offering alternate payment options (UPI, new card, net banking)

5. If no update after 2 reminders, escalate to human or pause subscription

## Timing rules

Send initial update prompt immediately following transaction failure

Space reminder follow-ups by at least 48 hours

## Compliance notes

Do not contact if customer has DND flag set

Max 2 reminder messages per week per customer