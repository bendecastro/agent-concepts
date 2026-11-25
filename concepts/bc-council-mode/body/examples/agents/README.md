# Example council advisors

Three read-only advisor profiles for `bc-council-mode`, each with a different standing stance. The stances matter: advisors with identical neutral prompts tend to agree in the first round, so the cross-examination never runs.

To use them:

1. Copy the files you want into your user agent directory (`~/.pi/agent/agents/` in Pi) or a project's `.pi/agents/`.
2. Replace `model: provider/your-model-id` in each with a model you can run. Use a different model, ideally a different provider, for each advisor so they make different mistakes.
3. Adjust `thinking` to what your rate limits allow.

Two or three advisors are enough; the skill never uses more than four. Keep the `council-` prefix so the skill finds them, keep them read-only, and edit the stance sentence to fit the decisions you bring to the council.
