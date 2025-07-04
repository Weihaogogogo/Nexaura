import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3001,
    open: true,
    hmr: {
      port: 3001
    },
    proxy: {
      '/auth': {
        target: 'http://localhost',
        changeOrigin: true,
        secure: false,
        configure: (proxy, _options) => {
          proxy.on('proxyReq', (_proxyReq, req, _res) => {
            console.log('Proxying request to auth:', req.url);
            console.log('Headers in auth request:', req.headers.authorization);
          });
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.log('Proxy response from auth:', req.url, proxyRes.statusCode, proxyRes.statusMessage);
          });
        }
      },
      '/api': {
        target: 'http://localhost',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: false,
        configure: (proxy, _options) => {
          proxy.on('proxyReq', (_proxyReq, req, _res) => {
            console.log('Proxying request to api:', req.url);
            console.log('Headers in api request:', req.headers.authorization);
          });
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.log('Proxy response from api:', req.url, proxyRes.statusCode, proxyRes.statusMessage);
          });
        }
      },
      '/workflows': {
        target: 'http://localhost',
        changeOrigin: true,
        secure: false,
        configure: (proxy, _options) => {
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.log('Proxying request to workflows:', req.url);
            console.log('Headers in workflows request:', req.headers.authorization);
            
            // 确保POST请求到 /workflows/ 而不是 /workflows
            if (req.method === 'POST' && req.url === '/workflows') {
              proxyReq.path = '/workflows/';
              console.log('Redirected POST /workflows to /workflows/');
            }
          });
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.log('Proxy response from workflows:', req.url, proxyRes.statusCode, proxyRes.statusMessage);
          });
        }
      }
    }
  },
  build: {
    target: 'es2015',
    sourcemap: false,
    minify: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['element-plus', 'ant-design-vue'],
          utils: ['axios', 'dayjs']
        }
      }
    }
  },
})
