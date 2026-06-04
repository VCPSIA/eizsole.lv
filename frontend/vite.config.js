import { defineConfig } from 'vite'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  build: {
    outDir: path.resolve(__dirname, '../static/dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, 'src/main.js'),
      output: {
        assetFileNames: '[name][extname]',
        entryFileNames: '[name].js',
      },
    },
  },
  css: {
    postcss: path.resolve(__dirname, 'postcss.config.js'),
  },
})
