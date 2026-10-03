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

export const SOURCES = {
  clickhouse: { label: "ClickHouse", long: "the ClickHouse blog" },
  medium: { label: "Medium", long: "Medium" },
  "ryadh.net": { label: "Personal", long: "my old blog" },
} as const;

export type Source = keyof typeof SOURCES;

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const MONTHS_LONG = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

/** "25 Sep", or "25 September 2025" with `long`. Dates are stored as UTC midnight. */
export function fmtDate(d: Date, long = false) {
  const day = d.getUTCDate();
  return long
    ? `${day} ${MONTHS_LONG[d.getUTCMonth()]} ${d.getUTCFullYear()}`
    : `${day} ${MONTHS[d.getUTCMonth()]}`;
}
