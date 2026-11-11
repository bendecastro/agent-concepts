# Existing application

Learn the existing theme, tokens, components and interaction patterns first; reuse them instead of imposing a new palette, typeface or signature. Match all supported themes and states, including focus and disabled. Sweep the whole captured surface for unstyled native elements that escaped the system, without replacing accessible native behavior needlessly.

One primary action per surface; group quieter secondary actions as controls, not loose text. Icons must say what they do; keep visible labels short and give controls full accessible names. Labels name what users control; errors explain and direct recovery; empty states invite the next action. A label wrapping at a supported size is a defect: shorten it or change the layout.

Render structured data as aligned grids where comparison matters. Keep keys and indivisible tokens non-breaking where possible, but allow long values to wrap or overflow deliberately so narrow hosts remain usable. Choose overlay or in-flow placement according to the container and host: an overlay can obscure or clip content, while in-flow expansion can change a host-sized popup. Test the actual container and resulting states.

Cover empty, loading, success, error, disabled, hover and focus as applicable; preserve input and provide recovery on errors. A screenshot of one state cannot establish the others.
