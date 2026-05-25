export const calculatePages = (text: string) => {
  if (!text) return 1;

  const words = text.split(/\s+/).length;

  // approx 400 words per page
  return Math.max(1, Math.ceil(words / 400));
};
