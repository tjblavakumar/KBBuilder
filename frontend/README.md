# KB Builder Frontend

Vue.js frontend for the Knowledge Base Builder application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The frontend will be available at: http://localhost:5173

## Features

### Create Knowledge Base
1. Enter website URL to scan for PDFs
2. Select PDFs from the discovered list
3. Add multiple URLs if needed
4. Configure KB name and select Bedrock model
5. Click "Build KB" to create

### Chat Interface
- Ask questions about your documents
- View AI-generated responses
- See source references with page numbers
- Chat history automatically saved

## Project Structure

```
src/
├── components/       # Reusable Vue components
├── views/           # Page components
│   ├── HomeView.vue        # KB list
│   ├── CreateKBView.vue    # KB creation wizard
│   └── ChatView.vue        # Chat interface
├── services/        # API communication
│   └── api.js
├── stores/          # Pinia state management
│   └── kb.js
├── router/          # Vue Router configuration
│   └── index.js
├── App.vue          # Root component
├── main.js          # Application entry
└── style.css        # Global styles
```

## API Integration

The frontend communicates with the FastAPI backend through a proxy configured in `vite.config.js`. All `/api/*` requests are forwarded to `http://localhost:8000`.

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.
