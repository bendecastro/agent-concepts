# Surfaces and capture

Record host, dimensions, scale and state for each capture; inspect full-resolution originals. Select sizes from the actual supported context, not arbitrary fixed breakpoints. Capture tools are examples, not prerequisites.

- **Web:** use a headless browser to capture named wide and narrow viewport sizes, relevant zoom, themes and states. Prefer modern platform features appropriate to the supported browsers; consult Modern Web Guidance if available. Check responsive overflow and interaction separately.
- **Host-sized surfaces:** extension popups, side panels and embedded webviews must be captured in the real host at its actual size. A page viewport can hide host-controlled sizing, clipping and expansion bugs. Open the real extension/host, exercise the relevant state, and capture its window or region.
- **Desktop:** capture the actual app/window at stated geometry and scale. On Wayland, `grim` can capture a region using the window geometry supplied by the compositor; on macOS, `screencapture` can capture the window or a selected region. Include relevant theme and resize states.
- **Mobile:** capture the running emulator or simulator at stated device, orientation and text settings; exercise touch targets and relevant states separately.
- **Terminal UI:** state columns × rows and capture the actual terminal via screenshot or text capture. Inspect wrapping, alignment, focus and legibility at supported sizes; a text capture alone cannot establish color or visual rendering.

Use the host's accessibility and interaction conventions. CSS-pixel metrics in web standards are not universal native or terminal units. If the real host or a capture tool is unavailable, report the result visually unverified rather than substituting a misleading viewport.
