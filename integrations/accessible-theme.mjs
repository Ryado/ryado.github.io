// Derive WCAG AA variants of Shiki themes: every token colour that falls
// below 4.5:1 against the page's code background is darkened (light themes)
// or lightened (dark themes) just enough to pass.
const lum = (hex) => {
  const c = [1, 3, 5]
    .map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((x) => (x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
};
const contrast = (a, b) => {
  const [x, y] = [lum(a), lum(b)];
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
};
const mix = (hex, target, t) =>
  "#" +
  [1, 3, 5]
    .map((i) => {
      const a = parseInt(hex.slice(i, i + 2), 16);
      const b = parseInt(target.slice(i, i + 2), 16);
      return Math.round(a + (b - a) * t).toString(16).padStart(2, "0");
    })
    .join("");

function fix(color, bg, toward, min = 4.6) {
  if (typeof color !== "string" || !/^#[0-9a-f]{6}/i.test(color)) return color;
  const base = color.slice(0, 7);
  const alpha = color.slice(7);
  let out = base;
  for (let t = 0; contrast(out, bg) < min && t <= 1; t += 0.02) out = mix(base, toward, t);
  return out + alpha;
}

export function accessibleTheme(theme, background) {
  const toward = theme.type === "dark" ? "#ffffff" : "#000000";
  return {
    ...theme,
    name: `${theme.name}-aa`,
    colors: {
      ...theme.colors,
      "editor.background": background,
      "editor.foreground": fix(theme.colors?.["editor.foreground"], background, toward),
    },
    tokenColors: (theme.tokenColors ?? []).map((tc) =>
      tc.settings?.foreground
        ? { ...tc, settings: { ...tc.settings, foreground: fix(tc.settings.foreground, background, toward) } }
        : tc,
    ),
  };
}
