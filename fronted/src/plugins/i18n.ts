import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import zh from '@/locales/zh.json'

const messages = {
  en,
  zh
}

const getDefaultLocale = (): string => {
  const savedLocale = localStorage.getItem('locale')
  if (savedLocale && Object.keys(messages).includes(savedLocale)) {
    return savedLocale
  }
  
  // 检测浏览器语言
  const browserLocale = navigator.language.toLowerCase()
  
  // 如果是中文相关的语言，返回中文
  if (browserLocale.includes('zh') || browserLocale.includes('cn')) {
    return 'zh'
  }
  
  // 默认返回英文
  return 'en'
}

export const i18n = createI18n({
  legacy: false,
  locale: getDefaultLocale(),
  fallbackLocale: 'en',
  messages,
  globalInjection: true,
  allowComposition: true,
  silentTranslationWarn: true,
  silentFallbackWarn: true
})

export const setLocale = (locale: string) => {
  if (Object.keys(messages).includes(locale)) {
    i18n.global.locale.value = locale as any
    localStorage.setItem('locale', locale)
    document.documentElement.lang = locale
  }
}

export const supportedLocales = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'zh', name: '中文', flag: '🇨🇳' }
]