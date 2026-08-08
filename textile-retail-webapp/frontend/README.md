# ASAA Fashion & Beauty House - Frontend

Modern React + Vite application for the ASAA Fashion & Beauty House e-commerce platform.

## 🌐 Live Website

**Access the live application here:** **[https://textile-retail.vercel.app/](https://textile-retail.vercel.app/)**

**Vercel Project:** [https://vercel.com/asaafashion/textile-retail](https://vercel.com/asaafashion/textile-retail)

## Overview

This is the frontend portion of the ASAA e-commerce application. It provides:
- **Storefront** - Product browsing, filtering, and purchasing
- **Admin Dashboard** - Product management and CRUD operations
- **Authentication** - User registration, login, and session management
- **Responsive Design** - Mobile-first design with Tailwind CSS

## Tech Stack

- **React 19** - UI framework
- **Vite 8** - Ultra-fast build tool with HMR
- **Tailwind CSS 4** - Utility-first CSS framework
- **React Router 7** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Icon library

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Storefront.jsx        # Main shopping interface
│   │   └── Admin.jsx              # Admin product management
│   │
│   ├── components/
│   │   ├── AuthModal.jsx         # Login/Register modal
│   │   └── ProductModal.jsx      # Product details modal
│   │
│   ├── App.jsx                   # Main app component & routing
│   ├── App.css                   # Tailwind & custom styles
│   ├── index.css                 # Global styles
│   └── main.jsx                  # React entry point
│
├── public/                        # Static assets
├── package.json                   # Dependencies
├── vite.config.js                # Vite configuration
├── tailwind.config.js            # Tailwind configuration
├── netlify.toml                  # Netlify deployment config
├── vercel.json                   # Vercel deployment config
└── README.md                     # This file
```

## Pages

### Storefront (`Storefront.jsx`)
- Browse all available products
- Filter by category (Clothing, Footwear, Accessories, Beauty)
- View product details in modal
- Add items to cart
- User authentication panel
- Order history display
- Responsive product grid

### Admin Dashboard (`Admin.jsx`)
- Complete product CRUD operations
- Create new products with images
- Edit existing products
- Delete products
- View all products in table format
- Upload images from multiple sources (local, GitHub, Google Drive, URL)
- Admin-only access with authentication

## Components

### AuthModal (`AuthModal.jsx`)
Reusable modal for user authentication:
- Registration form (name, email, password)
- Login form (email, password)
- Admin setup form (with SECRET_KEY)
- Form validation and error handling
- Toggle between login/register modes

### ProductModal (`ProductModal.jsx`)
Product detail view:
- Image gallery/carousel
- Product information (name, description, price, sale price)
- Size and color selection
- Stock availability
- Add to cart functionality
- Close/back navigation

## Setup & Installation

### Prerequisites
- Node.js 16+
- npm or yarn
- Backend API running (see backend README)

### Installation

```bash
cd frontend
npm install
```

### Environment Configuration

Create a `.env.local` file (if needed) for environment variables:

```env
VITE_API_URL=http://localhost:8000
```

### Development Server

```bash
npm run dev
```

Server runs at `http://localhost:5173` with hot module reload (HMR).

### Build for Production

```bash
npm run build
```

Optimized build output goes to `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Linting

```bash
npm run lint
```

Uses Oxlint for code quality checks.

## API Integration

The frontend communicates with the backend API using Axios. Base URL defaults to:
- Development: `http://localhost:8000`
- Production: Backend deployment URL (e.g., https://asaa-fashion.onrender.com)

### Key API Endpoints Used

**Authentication**
- `POST /api/register` - Register new account
- `POST /api/login` - Login and get JWT token
- `POST /api/logout` - Logout
- `GET /api/me` - Get current user

**Products**
- `GET /api/products` - Fetch all products
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)
- `DELETE /api/products/{id}` - Delete product (admin)
- `POST /api/upload-image` - Upload product image (admin)

**Orders**
- `GET /api/orders` - Get user's orders
- `POST /api/orders` - Place new order

## Styling

### Tailwind CSS
- All styling uses Tailwind utility classes
- Configured for responsive design (mobile-first)
- Consistent spacing, colors, and typography
- Custom theme configuration in `tailwind.config.js`

### Custom CSS
- `App.css` - Component-specific styles and animations
- `index.css` - Global styles and custom properties

## State Management

Currently using React's built-in state management with `useState` and `useContext`. For larger applications, consider:
- Redux or Redux Toolkit
- Zustand
- Jotai
- Context API with useReducer

## Performance Optimization

- Lazy loading with React.lazy()
- Code splitting with Vite
- Image optimization
- Memoization for expensive components
- Efficient re-render prevention

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- Mobile responsive design

## Development Guidelines

### Component Structure
- Functional components with hooks
- Proper prop validation
- Clear separation of concerns
- Reusable components for common UI elements

### Naming Conventions
- Components: PascalCase (e.g., `AuthModal.jsx`)
- Functions/utilities: camelCase
- CSS classes: kebab-case

### Best Practices
- Use semantic HTML
- Accessible component design
- Error handling for API calls
- User feedback (loading states, error messages)
- Clean code and comments for complex logic

## Deployment

### Netlify
```bash
npm run build
# Push to Netlify or use Netlify CLI
```

Configuration: `netlify.toml`

### Vercel
```bash
npm run build
# Push to Vercel
```

Configuration: `vercel.json`

### Environment Variables for Production
Set these in your deployment platform:
- `VITE_API_URL` - Backend API base URL

## Troubleshooting

### Hot Module Reload (HMR) Not Working
- Check browser console for errors
- Restart dev server
- Clear browser cache

### API Connection Issues
- Ensure backend is running
- Check CORS configuration in backend
- Verify API URL in environment variables
- Check network tab in browser DevTools

### Build Errors
- Clear `node_modules` and `package-lock.json`
- Run `npm install` again
- Check for TypeScript errors

## Dependencies

See `package.json` for complete list. Key dependencies:

```json
{
  "dependencies": {
    "axios": "^1.18.1",
    "lucide-react": "^1.25.0",
    "react": "^19.2.7",
    "react-dom": "^19.2.7",
    "react-router-dom": "^7.18.1"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.3.3",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^6.0.3",
    "autoprefixer": "^10.5.4",
    "oxlint": "^1.71.0",
    "postcss": "^8.5.22",
    "tailwindcss": "^4.3.3",
    "vite": "^8.1.1"
  }
}
```

## Contributing

When contributing to the frontend:
1. Follow the existing code style
2. Create feature branches
3. Test thoroughly before submitting
4. Update documentation as needed
5. Ensure responsive design works across devices

## License

Part of the ASAA Fashion & Beauty House project.
