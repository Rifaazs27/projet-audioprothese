import js from '@eslint/js'

export default [
  js.configs.recommended,
  {
    files: ['src/**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      parserOptions: { ecmaFeatures: { jsx: true } },
      globals: { document: 'readonly', fetch: 'readonly', globalThis: 'readonly' },
    },
    rules: {
      'no-unused-vars': 'warn',
    },
  },
]
