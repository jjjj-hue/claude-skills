---
name: real-estate-drip-workflows
description: "Use when Lucia asks to build, clean up, or organize real estate work drips, Follow Up Boss/FUB email or SMS templates, StreetEasy/Zillow rental lead follow-up, flip messages, Ric/Bond New York workflows, Notion lead tracking, or Claude/Perplexity handoffs."
metadata:
  version: "1.0"
---

# Real Estate Drip Workflows

## When to Use This Skill

Use this skill when Lucia asks for help with:

- Real estate rental lead drips, work drips, follow-up sequences, or nurture flows.
- Follow Up Boss (FUB) email or text templates.
- StreetEasy, Zillow, ShowMojo, or other rental-inquiry follow-up.
- “Flip” messages that move a lead from one listing to similar alternatives.
- Ric/Bond New York workflows, including messages to or for Ric.
- Notion workspace organization for Lead & Deal Tracker, FUB Template Library, Daily Planner, or Mgmt Updates Tracker.
- Claude cowork / Claude handoff prompts for client-ready writing.

## Core Context

Lucia is a real estate agent working on NYC residential rentals with Ric at Bond New York. Always call him “Ric,” not “Ricardo.” Lucia uses FUB as the lead pipeline and follow-up engine, Notion as the command center, Gmail for company/internal communication, Perplexity/Comet for research and account-connected work, and Claude for final client-ready writing and formatting.

Her preferred style is clear, concise, factual, natural, and not AI-sounding. Avoid cheesy language, over-selling, vague claims, and emotional fluff. For client-facing messages, use plain language and one clear next step.

## Source of Truth

Before creating or changing a drip, identify which source should be treated as authoritative:

1. FUB or Ric’s active listing data for live availability, pricing, and lead status.
2. StreetEasy/Zillow/RealtyMX/current listing pages for rental details and live comp context.
3. Notion for internal tracking, template organization, daily priorities, and process notes.
4. Gmail for company threads, approvals, management updates, or context Lucia was CC’d on.

Do not assume old pricing or availability is still accurate. For any listing, pricing, OP, concession, or availability claim, recommend verification with Ric, FUB, RealtyMX, or the live listing before sending.

## Follow Up Boss Read-Only Rule

Follow Up Boss is always browse/view/read-only for the assistant. Even if browser automation or a future connector makes edits technically possible, do not directly change anything in FUB.

Permitted FUB activities:

- View, browse, search, inspect, and summarize lead records, tasks, notes, tags, templates, and communication history.
- Copy visible information into analysis, triage, drafts, or proposed updates.
- Read FUB exports, screenshots, or data Lucia provides.
- Draft exact message copy, tags, statuses, task text, drip steps, template names, or template edits for Lucia to review and apply manually.
- Give Lucia step-by-step instructions for changes she can make herself inside FUB.

Not permitted in FUB:

- Do not click save, submit, send, archive, delete, merge, assign, reassign, tag, untag, mark dead, mark active, create task, complete task, edit notes, change stage, change lead status, upload files, create template, update template, start/stop automation, import contacts, export contacts, or modify any live FUB object.
- Do not use browser automation to make FUB changes, even with confirmation. If Lucia wants a FUB change, prepare the exact copy/instructions and let her perform it.
- Do not send emails or texts from FUB. Draft only.

If Lucia asks to “update FUB,” interpret that as “prepare the exact update for me to paste or apply,” unless she explicitly clarifies that she is asking for a non-FUB system such as Google Sheets, Notion, Google Docs, Drip, Gmail, or Calendar.

## Workspace Map

### Follow Up Boss

Use FUB for:

- Lead records and source tracking.
- Tasks and reminders.
- Templates, email and SMS.
- Notes and touch history.
- Pipeline status and next actions.

### Notion

Use Notion as Lucia’s command center:

- Bond NY Work Hub: home base.
- Lead & Deal Tracker: active leads, status, next action, source, inquiry, showing date/time, FUB link, notes.
- FUB Template Library: template names, category, type, subject line, neighborhood, building, bedroom type, folder, last used, notes.
- Daily Planner: top outcomes and daily focus.
- Mgmt Updates Tracker: actionable management updates only.
- Claude ↔ FUB ↔ Gmail guide: tool handoff rules.
- FUB Triage: daily prioritization.

### Perplexity and Claude

- Use Perplexity/Comet for research, verification, live web/account-connected tasks, current rental comps, listing summaries, and options.
- Use Claude for polished final client-ready copy, FUB-ready templates, shorter/warmer/firmer variants, and formatting cleanup.
- If drafting in this environment, provide Claude-style final output directly rather than telling Lucia to use Claude, unless she specifically asks for a Claude prompt.

## Daily Triage Rule

Do not try to “clear FUB.” Prioritize today’s highest-value outcomes:

1. Hot leads: people actively replying, asking to tour, or ready to apply.
2. Time-sensitive follow-ups: pending tour, application, promised callback, or management update.
3. Pipeline builders: fresh outreach, strong alt listings, template cleanup, and follow-up systems.

If a lead cannot be fully answered yet, use a holding reply and set a specific next action:

> Got it — let me confirm availability and I’ll circle back shortly. What’s the best time today to connect?

## Drip Architecture

Default rental-lead drip for StreetEasy/Zillow inquiries:

### Stage 1: Immediate Response

Goal: reply quickly, confirm the inquiry, and ask one scheduling or qualification question.

Inputs:

- Lead name if available.
- Original listing address/unit.
- Price, beds/baths, key feature, availability.
- Their desired move date, budget, pets, guarantor/income, and tour availability if known.

Output:

- One short text under 320 characters.
- One email with subject line.
- A FUB task / next action.

### Stage 2: Qualification

Goal: get enough info to schedule efficiently.

Ask only what matters:

- Move-in date.
- Budget range.
- Neighborhood flexibility.
- Bed/bath needs.
- Pets.
- Income or guarantor situation if needed.
- Tour availability.

### Stage 3: Tour Scheduling

Goal: move from interest to showing.

Output should include:

- Specific windows.
- Address/unit.
- One confirmation question.
- Any must-know access or application note.

### Stage 4: Flip / Alternatives

Goal: keep the lead engaged if the original listing is unavailable, not ideal, or has better substitutes.

Use when:

- The original unit is unavailable.
- The lead’s budget or move date does not match.
- There are stronger low-days-on-market or high-value alternatives.
- Ric wants a lead pushed to another unit.

Default structure:

1. Acknowledge the original inquiry.
2. State the useful reason for alternatives.
3. Present 2-4 options max.
4. Keep each option concise: address/unit, price, beds/baths, top 2 features, availability/tour note.
5. End with one CTA.

### Stage 5: Warm Follow-Up

Use when a lead opened/clicked, replied before, toured, or asked direct questions.

Tone: personal, helpful, not pushy.

Ask:

- “Want me to check if it’s still available?”
- “Do you want to see this one or similar options?”
- “Should I send a few close matches under [budget]?”

### Stage 6: No-Response Follow-Up

Use when the lead has not replied.

Tone: short, direct, low pressure.

Avoid guilt-tripping. Do not over-explain. Give an easy out.

### Stage 7: Post-Tour / Application

Use when the lead toured or is ready to apply.

Output should include:

- Specific unit shown.
- Next step.
- Deadline or urgency if factual.
- Documents needed if applying.

## Engagement Branches

When designing Drip/FUB sequences, include simple engagement branches:

- Opened/clicked/replied: warm track.
- No open/no click/no reply: short re-engagement track.
- Tour scheduled: scheduling and confirmation track.
- Toured: post-tour feedback and application track.
- Application sent: application support and deadline track.
- Lease signed: close/wrap-up track.
- Dead/unqualified: stop or long-term nurture.

Suggested tags:

- renter-lead
- buyer-lead
- seller-lead
- tenant-rep
- neighborhood-[area]
- source-streeteasy
- source-zillow
- flip
- hot-lead
- no-response
- toured
- app-sent

## FUB Template Library Rules

Every strong email should have a matching SMS version. When creating or updating a template, output both unless Lucia asks for only one.

Use these template categories:

- New Listing
- Flip/Initial
- Follow-Up
- No Response
- Tour Confirm

Use these template types:

- Email
- Text

Naming convention:

`Neighborhood – Building/Address – Unit/Type – Purpose – YYYY-MM-DD`

Examples:

- `Greenpoint – 116 Franklin #5B – 1BR – Flip Initial – 2026-04-30`
- `UES – 1443 York – 1BR – No Response – 2026-04-30`
- `Nolita – 232 Elizabeth – 2BR – Tour Confirm – 2026-04-30`

For FUB folders, group by use-case:

- Tenant Rep Emails
- Apartment Marketing Emails
- Flip / StreetEasy
- Follow-Up / No Response
- Tour Confirmations

## Email Format Rules

For FUB emails:

- Include a subject line.
- Use a clean body with short paragraphs.
- Use one primary CTA.
- Use plain, client-ready language.
- Do not use markdown syntax in the final email body.
- If HTML is requested, use minimal paste-ready HTML with inline CSS, plain Arial, and bold address lines.
- Do not include raw URLs or fub.direct links as visible link text.
- Label links clearly as “Video Tour,” “Virtual Tour,” “Listing,” or “Application,” depending on the context.

## SMS Format Rules

For texts:

- Keep under 320 characters unless Lucia asks for longer.
- One idea per message.
- End with one clear question.
- Sound like a real person, not a campaign.
- Avoid “just checking in” unless there is a specific reason.

## Flip Message Rules

When building a flip message:

1. Start from the listing the lead asked about.
2. Identify why the lead might still be interested: price, location, layout, move date, laundry, elevator, light, outdoor space, pets, doorman, commute.
3. Find or use 2-4 comparable alternatives.
4. Prefer fresh listings and low days on market when available.
5. Prioritize immediate availability, strong value, and high commission/OP opportunities when relevant.
6. Flag brand/building risk or questionable management reputation if known.
7. Keep the final copy simple and honest.

Do not say a unit is “the best deal” or “will go fast” unless supported by current facts. Safer phrasing: “This one is worth checking quickly because it’s priced well relative to similar options.”

## Output Format for Drip Requests

When Lucia asks to build out a drip, return:

1. Drip name.
2. Use case and trigger.
3. Required fields or merge fields.
4. Timing schedule.
5. Email templates.
6. Matching SMS templates.
7. Branching rules.
8. FUB/Notion logging instructions.
9. Verification notes.

Keep the main answer concise, but include enough detail to paste into FUB or Drip.

## Notion Logging Instructions

For Lead & Deal Tracker:

- Status should reflect the actual pipeline stage, not a random unit name.
- Next Action should be plain English and start with a verb.
- Last Contact should be updated after any sent message.
- FUB Link should be included when available.
- Notes should capture constraints and preferences, not full message history.

Suggested clean status set:

- New Lead
- Contacted
- Active
- Showing Scheduled
- Showed
- App Sent
- App Pending
- Closed
- Dead
- Follow Up
- Hot Lead

For FUB Template Library, log:

- Template Name
- Type
- Category
- Subject Line if email
- Neighborhood
- Building
- Bedroom Type
- FUB Folder
- Date Created
- Last Used
- Notes

## Automation Safety

Do not directly change anything in Follow Up Boss under any circumstances. FUB is view/browse/read-only.

Do not activate a Drip workflow, send email/text, post, modify live CRM records outside FUB, edit connected spreadsheets/databases/docs, create calendar events, or create/update automations without first showing Lucia the exact draft or action and getting explicit confirmation.

It is acceptable to draft plans, templates, Notion schemas, and suggested tags without confirmation. It is not acceptable to send or activate them without confirmation.

## Quality Checklist

Before finalizing:

- Does every email have a matching SMS when appropriate?
- Is there one CTA per message?
- Are links labeled instead of raw?
- Is the tone concise, factual, and natural?
- Are availability, price, OP/concessions, and fees flagged for verification?
- Is Ric called Ric?
- Is the template name FUB-searchable?
- Is the next action clear enough to execute tomorrow?
- Was Follow Up Boss kept strictly read-only?
