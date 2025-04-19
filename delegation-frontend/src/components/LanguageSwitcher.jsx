import i18n from 'i18next'

const LanguageSwitcher = () => {
  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang)
  }

  return (
    <select onChange={(e) => changeLanguage(e.target.value)} defaultValue={i18n.language}>
      <option value="en">EN</option>
      <option value="fr">FR</option>
      <option value="ar">AR</option>
    </select>
  )
}
