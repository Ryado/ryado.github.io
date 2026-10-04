export const SITE = {
  name: "Ryadh Dahimene",
  title: "Ryadh Dahimene",
  headline: "Product, Data, AI and stuff",
  description:
    "Ryadh Dahimene leads AI/ML product at ClickHouse. Essays and posts on databases, observability, AI agents and product management.",
  email: "dahimene.ryadh@gmail.com",
  linkedin: "https://www.linkedin.com/in/ryadh",
  github: "https://github.com/Ryado",
};

/**
 * Posts listed under "Essays" on the home page. Everything else is a launch.
 * Slugs are the file names without the year prefix.
 */
export const ESSAYS = new Set([
  "agent-facing-analytics",
  "evolution-of-sql-based-observability-with-clickhouse",
  "the-state-of-sql-based-observability",
  "cost-predictable-logging-with-clickhouse-vs-datadog-elastic-stack",
  "the-engineering-minded-product-manager",
  "algerie-equation",
  "cdv",
  "elwatan",
  "jdn",
]);

export const SOURCES = {
  clickhouse: { label: "ClickHouse", long: "the ClickHouse blog" },
  medium: { label: "Medium", long: "Medium" },
  "ryadh.net": { label: "Personal", long: "my old blog" },
} as const;

export type Source = keyof typeof SOURCES;

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const MONTHS_LONG = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

/** "25 Sep" by default, "Sep 2025" with "month", "25 September 2025" with true. Dates are UTC midnight. */
export function fmtDate(d: Date, style: boolean | "month" = false) {
  const day = d.getUTCDate();
  if (style === "month") return `${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
  return style
    ? `${day} ${MONTHS_LONG[d.getUTCMonth()]} ${d.getUTCFullYear()}`
    : `${day} ${MONTHS[d.getUTCMonth()]}`;
}
