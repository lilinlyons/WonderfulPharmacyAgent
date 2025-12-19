export const I18N = {
  en: {
    greeting: (name) => `Hello ${name}! How can I help you today?`,
    subtitle: "Get answers about medications, dosages, side effects, and more",
    placeholder: "Ask about medications, dosages, side effects...",
    error: "Sorry, something went wrong.",
    requestsTitle: "Prescription Requests",
    supportTitle: "Support Requests",
    noRequests: "No requests found",
    assistantTyping: "Assistant typing…",
    loading: "Loading…",
  },
  he: {
    greeting: (name) => `שלום ${name}! איך אפשר לעזור לך היום?`,
    subtitle: "מידע על תרופות, מינונים, תופעות לוואי ועוד",
    placeholder: "שאל על תרופות, מינונים, תופעות לוואי...",
    error: "אירעה שגיאה, נסה שוב.",
    requestsTitle: "בקשות מרשם",
    supportTitle: "פניות תמיכה",
    noRequests: "לא נמצאו בקשות",
    assistantTyping: "העוזר כותב…",
    loading: "טוען…",
  },
};

export function getTranslations(lang) {
  return I18N[lang] || I18N.en;
}

export function isRTL(lang) {
  return lang === "he";
}