# Frontend Troubleshooting Guide

## Common Issues and Solutions

### 1. Tailwind CSS Configuration Issues

**Problem**: `Error: It looks like you're trying to use 'tailwindcss' directly as a PostCSS plugin`

**Solution**:
```bash
# Remove problematic packages
npm uninstall tailwindcss @tailwindcss/postcss

# Install stable versions
npm install -D tailwindcss@^3.4.0 postcss@^8.4.0 autoprefixer@^10.4.0

# Reinitialize Tailwind
npx tailwindcss init -p
```

**Configuration Files**:
- `tailwind.config.js` should contain:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

- `postcss.config.js` should contain:
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### 2. TypeScript/Axios Import Issues

**Problem**: `Module '"axios"' has no exported member 'AxiosInstance'`

**Solution**:
```bash
# Remove old axios types
npm uninstall @types/axios

# Use the simplified API service approach
# The api.ts file has been updated to avoid complex type imports
```

**Updated API Service**:
- Uses `axios` directly without complex type imports
- Uses `any` types for interceptors to avoid TypeScript conflicts
- Maintains full functionality while avoiding type issues

### 3. Build Errors

**Problem**: Various compilation errors

**Solutions**:

1. **Clear cache and reinstall**:
```bash
rm -rf node_modules package-lock.json
npm install
```

2. **Check TypeScript configuration**:
```bash
# Ensure tsconfig.json is properly configured
npx tsc --noEmit
```

3. **Update dependencies**:
```bash
npm update
```

### 4. Development Server Issues

**Problem**: React development server won't start

**Solutions**:

1. **Check port availability**:
```bash
# Check if port 3000 is in use
lsof -i :3000
# Kill process if needed
kill -9 <PID>
```

2. **Clear React cache**:
```bash
rm -rf node_modules/.cache
npm start
```

3. **Check environment variables**:
```bash
# Ensure .env file exists
echo "REACT_APP_API_URL=http://localhost:8000" > .env
```

### 5. API Connection Issues

**Problem**: Frontend can't connect to backend

**Solutions**:

1. **Check backend is running**:
```bash
curl http://localhost:8000/health
```

2. **Check CORS configuration**:
- Ensure backend allows frontend origin
- Check browser console for CORS errors

3. **Verify API URL**:
```bash
# Check environment variable
echo $REACT_APP_API_URL
```

### 6. Authentication Issues

**Problem**: Login/logout not working

**Solutions**:

1. **Clear localStorage**:
```javascript
// In browser console
localStorage.clear()
```

2. **Check JWT token**:
```javascript
// In browser console
console.log(localStorage.getItem('token'))
```

3. **Verify backend authentication**:
```bash
# Test login endpoint
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "secret"}'
```

## Development Tips

### 1. Debugging

- Use browser developer tools
- Check Network tab for API calls
- Monitor console for errors
- Use React Developer Tools

### 2. Performance

- Use React.memo for expensive components
- Implement proper loading states
- Optimize bundle size with code splitting

### 3. Testing

- Test on different browsers
- Test responsive design
- Test error scenarios
- Test authentication flow

## Environment Setup

### Required Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Development Commands

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Check for linting issues
npm run lint
```

## Package Versions

### Stable Versions Used

```json
{
  "dependencies": {
    "axios": "^1.11.0",
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "react-router-dom": "^7.8.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

## Getting Help

If you encounter issues not covered here:

1. Check the browser console for errors
2. Check the terminal output for build errors
3. Verify all dependencies are installed correctly
4. Ensure the backend API is running and accessible
5. Check network connectivity and firewall settings

## Common Error Messages

| Error | Solution |
|-------|----------|
| `Module not found` | Run `npm install` |
| `Port already in use` | Kill process on port 3000 |
| `CORS error` | Check backend CORS configuration |
| `JWT token expired` | Clear localStorage and login again |
| `Tailwind CSS not working` | Check PostCSS configuration |
| `TypeScript compilation error` | Check type definitions and imports |
