# Quiz Cron Agent Prompt

This agent fires Tuesday, Thursday, and Saturday at 9pm SGT. Its only job is to count prioritised quiz items and send a notification. It does NOT run the quiz and must NOT modify any wiki files.

## Instructions

1. Read `/Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/quiz/performance.md`
2. Read `/Users/laowuisme/Documents/MyWork/spanish-wiki/wiki/curriculum/curriculum-map.md`
3. Count items by priority bucket:
   - **New** — vocab or topic pages with `last_updated` within the last 7 days that have never been quizzed (not in performance.md)
   - **Overdue** — rows in curriculum-map where Days Since > 14 AND stage = `encountered` or `understood`
   - **High-miss** — rows in performance.md where Correct/Attempts < 0.5 AND Attempts >= 2
4. Identify the top 3 items by weight using the QUIZ weighting rules from CLAUDE.md (same multipliers: errors 3×, last result incorrect 3×, new 2×, overdue 2×, etc.)
5. Determine today's day name (Tuesday, Thursday, or Saturday).
6. Send a push notification using the PushNotification tool:
   - Message: "🇪🇸 Spanish quiz ready — [N] items prioritised ([X] new, [Y] overdue, [Z] high-miss). Run 'quiz me'."
7. Create a Gmail draft to laowuisme@gmail.com using `mcp__claude_ai_Gmail__create_draft`:
   - Subject: `🇪🇸 Spanish Quiz — [Tuesday/Thursday/Saturday] 9pm`
   - Body:
     ```
     [N] items queued for tonight's quiz.
     Top picks: [slug1] ([reason]), [slug2] ([reason]), [slug3] ([reason])

     Open Claude Code and type: quiz me
     ```
8. Stop. Do not modify any wiki files.
