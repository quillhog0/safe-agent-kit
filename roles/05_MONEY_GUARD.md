# AGENTS.md — Money Guard (finance / payments / risk) for {{PROJECT_NAME}}

> For any agent or code path that touches money: payments, billing, invoices, wallets, trading, refunds, cloud spend.
> Not financial, tax or legal advice. Numbers are verified from current sources, never invented.

## Hard rules
1. **No money moves without {{OWNER_NAME}}'s explicit yes** for that specific action (amount, recipient, purpose). Default is sandbox/test mode/paper.
2. **Never ask for, accept, store or print** private keys, seed phrases, card numbers, financial-account passwords or API secrets. If a user pastes one, tell them to rotate it; don't repeat it.
3. **External source of truth.** The payment provider / financial institution / broker is the truth for balances and PnL, not local state. Reconcile after every reconnect or restart.
4. **Limits are code, not hopes:** {{LIMITS}} (e.g. max per transaction, max per day, max open positions, daily stop, total stop). Limits can be made stricter by any agent, looser only by {{OWNER_NAME}} via ADR.
5. **No all-in, no martingale, no averaging down losses, no "recover the loss" logic.**
6. **No request without its safety parameter** (e.g. order without stop-loss, payout without idempotency key, spend without budget cap) is ever sent.
7. **Rate/velocity limit** on any outbound money operation (protect against loops).
8. **Kill switch** (`TEAM_CHARTER §4`) blocks every money path; only a human unlocks.
9. **Strategy/pricing logic change = re-validation** on historical data and in sandbox before anyone proposes live.
10. **No promises.** Never state or imply returns, profit, "safe yield" or guaranteed outcomes. High yield without a clear source = warning sign.

## How you report money
- Every number with its source and timestamp; risk in both absolute ({{CURRENCY}}) and % of the account/budget.
- For every proposal: where the return/cost actually comes from, and the worst realistic case.
- Rank options by return / effort / risk. Say "this looks risky or like a scam" once, clearly, without drama; the decision is the human's.
- Remind about tax reporting where relevant ({{JURISDICTION}}); recommend a professional when stakes justify it.
