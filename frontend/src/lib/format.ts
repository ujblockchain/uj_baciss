const dateTime = new Intl.DateTimeFormat("en-ZA", {
  dateStyle: "medium",
  timeStyle: "short",
});

export const formatDateTime = (iso: string): string => {
  return dateTime.format(new Date(iso));
};

/** "ready_for_review" becomes "Ready for review". */
export const humanize = (value: string): string => {
  const text = value.replaceAll("_", " ");
  return text.charAt(0).toUpperCase() + text.slice(1);
};
