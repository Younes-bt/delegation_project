import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

import translationEN from './locales/en/translation.json'
import translationFR from './locales/fr/translation.json'
import translationAR from './locales/ar/translation.json'

// the translations
const resources = {
  en: { translation: translationEN },
  fr: { translation: translationFR },
  ar: { translation: translationAR }
}

i18n
  .use(LanguageDetector) // detect user language
  .use(initReactI18next) // pass i18n down to react-i18next
  .init({
    resources,
    fallbackLng: 'en',
    interpolation: { escapeValue: false }
  })

export default i18n
