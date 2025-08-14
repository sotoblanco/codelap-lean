# CodeLap Lean Frontend

A React TypeScript frontend for the CodeLap Lean application, featuring AI-powered learning plan generation for GitHub repositories.

## Features

- **User Authentication**: Login and registration with JWT token management
- **Repository Search**: Search GitHub repositories by URL or keywords
- **AI Learning Plans**: Generate comprehensive learning plans using AI
- **Responsive Design**: Modern UI with Tailwind CSS
- **Real-time Updates**: Live search results and plan generation

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

## Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```

3. **Open your browser**:
   Navigate to `http://localhost:3000`

## Available Scripts

- `npm start` - Start the development server
- `npm run build` - Build the app for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Project Structure

```
src/
├── components/          # React components
│   ├── Home.tsx        # Main application page
│   ├── Login.tsx       # Login form
│   ├── Register.tsx    # Registration form
│   ├── RepositoryCard.tsx      # Repository display card
│   ├── LearningPlanModal.tsx   # Learning plan modal
│   └── ProtectedRoute.tsx      # Authentication wrapper
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication context
├── services/           # API services
│   └── api.ts         # API client and methods
├── types/              # TypeScript interfaces
│   └── api.ts         # API response types
└── App.tsx            # Main application component
```

## Authentication

The application uses JWT tokens for authentication:

- Tokens are stored in localStorage
- Automatic token inclusion in API requests
- Automatic redirect to login on authentication failure
- Protected routes for authenticated users only

## API Integration

The frontend communicates with the FastAPI backend through:

- **Authentication**: `/login`, `/register`, `/users/me`
- **Repository Search**: `/search-repo`
- **Learning Plan Generation**: `/generate-plan`

## Usage

1. **Login/Register**: Create an account or use demo credentials (johndoe/secret)
2. **Search Repositories**: Enter a GitHub URL or search term
3. **Select Repository**: Click on a repository to view details
4. **Generate Learning Plan**: Click "Generate Learning Plan" in the modal
5. **Approve & Save**: Review the AI-generated plan and approve it

## Demo Credentials

- **Username**: johndoe
- **Password**: secret

## Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Styling

The application uses Tailwind CSS for styling:

- Responsive design
- Modern UI components
- Consistent color scheme
- Hover effects and transitions

## Development

### Adding New Components

1. Create the component in `src/components/`
2. Add TypeScript interfaces if needed
3. Import and use in the main application

### API Integration

1. Add new types to `src/types/api.ts`
2. Add API methods to `src/services/api.ts`
3. Use in components with proper error handling

### Styling

- Use Tailwind CSS classes
- Follow the existing design patterns
- Ensure responsive design

## Troubleshooting

### Common Issues

1. **API Connection Errors**:
   - Ensure the backend is running on `http://localhost:8000`
   - Check CORS configuration in the backend

2. **Authentication Issues**:
   - Clear localStorage and try logging in again
   - Check JWT token expiration

3. **Build Errors**:
   - Run `npm install` to ensure all dependencies are installed
   - Check TypeScript compilation errors

### Development Tips

- Use the browser's developer tools to debug API calls
- Check the Network tab for request/response details
- Use React Developer Tools for component debugging

## Contributing

1. Follow the existing code structure
2. Add TypeScript types for new features
3. Include error handling for API calls
4. Test the application thoroughly
5. Ensure responsive design works on all screen sizes
