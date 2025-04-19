import ModeToggle from "@/components/mode-toggle"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem
} from "@/components/ui/dropdown-menu"
import { Globe } from "lucide-react"
import { Link } from "react-router-dom"
import { useState } from "react"
import { useTranslation } from 'react-i18next'
import i18n from 'i18next'

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false)

  const toggleMenu = () => setMenuOpen(!menuOpen)
  const { t } = useTranslation()

  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang)
  }

  return (
    <header className="bg-white dark:bg-gray-900 shadow-md sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between">
        {/* Left: Logo */}
        <div className="flex items-center gap-3">
          <Link to="/" className="text-xl font-bold text-primary">{t("delegation")}</Link>
        </div>

        {/* Middle: Desktop Menu */}
        <div className="hidden md:flex items-center gap-6">
          <Link to="/" className="text-sm font-medium text-muted-foreground hover:text-primary">{t("home")}</Link>
          <Link to="/about" className="text-sm font-medium text-muted-foreground hover:text-primary">{t("about")}</Link>
          <Link to="/contact" className="text-sm font-medium text-muted-foreground hover:text-primary">{t("contact")}</Link>
        </div>

        {/* Right: Toggles and Login */}
        <div className="flex items-center gap-4">
          {/* Language Switcher */}
          <DropdownMenu>
            <DropdownMenuTrigger className="flex items-center gap-1 text-sm font-medium text-muted-foreground hover:text-primary">
              <Globe size={18} />
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => changeLanguage('en')}>English</DropdownMenuItem>
              <DropdownMenuItem onClick={() => changeLanguage('fr')}>Français</DropdownMenuItem>
              <DropdownMenuItem onClick={() => changeLanguage('ar')}>العربية</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Dark/Light Mode */}
          <ModeToggle />

          {/* Login Button */}
          <Link to="/login" className="text-sm font-semibold hover:text-primary">
            {t("login")}
          </Link>

          {/* Mobile Toggle */}
          <button
            onClick={toggleMenu}
            className="md:hidden inline-flex items-center justify-center p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700"
          >
            <span className="sr-only">Open menu</span>
            <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none">
              <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" strokeWidth="2" />
            </svg>
          </button>
        </div>
      </nav>

      {/* Mobile Menu Dropdown */}
      {menuOpen && (
        <div className="md:hidden px-4 pb-4 space-y-2">
          <Link to="/" className="block text-sm text-muted-foreground hover:text-primary">{t("home")}</Link>
          <Link to="/about" className="block text-sm text-muted-foreground hover:text-primary">{t("about")}</Link>
          <Link to="/contact" className="block text-sm text-muted-foreground hover:text-primary">{t("contact")}</Link>
        </div>
      )}
    </header>
  )
}
