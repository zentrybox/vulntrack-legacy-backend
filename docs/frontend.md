# Vulntrack Frontend Documentation

## 1. Introduction

This document provides a comprehensive overview of the **Vulntrack Frontend**, a modern web application for vulnerability management. It is designed to interact with a Supabase backend, which it may share with other services like the `vulnerability-scanner-engine`.

The application is built with a focus on performance, developer experience, and a clean, responsive user interface.

### 1.1. Technology Stack

*   **Framework**: [Next.js](https://nextjs.org/) (App Router)
*   **Language**: [TypeScript](https://www.typescriptlang.org/)
*   **UI Library**: [ShadCN/UI](https://ui.shadcn.com/)
*   **Styling**: [Tailwind CSS](https://tailwindcss.com/)
*   **AI Integration**: [Google Genkit](https://firebase.google.com/docs/genkit)
*   **Database Client**: [Supabase](https://supabase.io/)
*   **Forms**: [React Hook Form](https://react-hook-form.com/) with [Zod](https://zod.dev/) for validation
*   **Deployment**: [Firebase App Hosting](https://firebase.google.com/docs/app-hosting)

---

## 2. Getting Started

Follow these steps to set up and run the project locally.

### 2.1. Prerequisites

*   Node.js (v18 or later)
*   npm or yarn

### 2.2. Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    npm install
    ```

### 2.3. Environment Variables

Create a `.env` file in the root of the project and add the following Supabase credentials. You can find these in your Supabase project settings under "API".

```env
# Supabase Public URL
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url

# Supabase Anonymous Key (for client-side access)
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Supabase Service Role Key (for server-side admin tasks like seeding)
# WARNING: Keep this key secure and never expose it on the client side.
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

### 2.4. Running the Development Server

To run the application in development mode, use:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### 2.5. Seeding the Database

To populate your Supabase database with sample data, navigate to the `/seed` page in your browser (`http://localhost:3000/seed`) and click the "Start Seeding" button. This action can be run multiple times to reset the data.

---

## 3. Project Structure

The project follows a standard Next.js App Router structure.

```
.
├── src/
│   ├── app/                # Application routes (pages)
│   │   ├── (main)/         # Main layout group
│   │   │   ├── dashboard/  # Dashboard page
│   │   │   ├── devices/    # Devices list and detail pages
│   │   │   └── ...         # Other application pages
│   │   ├── login/          # Login page
│   │   ├── seed/           # Database seeding page
│   │   ├── globals.css     # Global styles and CSS variables for theming
│   │   └── layout.tsx      # Root layout
│   ├── ai/                 # Genkit AI integration
│   │   ├── flows/          # AI flows (e.g., summarize, suggest)
│   │   └── genkit.ts       # Genkit configuration
│   ├── components/         # Reusable React components
│   │   ├── ui/             # ShadCN UI components
│   │   ├── common/         # General-purpose components (e.g., Pagination)
│   │   ├── devices/        # Components specific to device features
│   │   └── layout/         # Layout components (AppShell, Sidebar)
│   ├── config/             # Application configuration (e.g., navigation links)
│   ├── hooks/              # Custom React hooks (e.g., useToast)
│   ├── lib/                # Core logic, utilities, and external service clients
│   │   ├── api.ts          # Central API for Supabase data fetching
│   │   ├── seed-data.ts    # Sample data for seeding
│   │   ├── supabase/       # Supabase client configuration
│   │   └── utils.ts        # Utility functions (e.g., cn for classnames)
│   └── types/              # TypeScript type definitions
├── docs/                   # Project documentation
├── public/                 # Static assets
└── ...                     # Config files (next.config.js, tailwind.config.ts)
```

---

## 4. Core Features & Pages

### 4.1. Dashboard (`/dashboard`)
*   **Purpose**: Provides a high-level overview of the organization's security posture.
*   **Data Source**: Fetches data from the `fetchOrganizationSummary` function in `src/lib/api.ts`, which aggregates data from Supabase.
*   **Components**: Features `StatCard` components for key metrics and `recharts` for visualizing scan activity and vulnerability distribution.

### 4.2. Devices (`/devices`)
*   **Purpose**: Lists all registered devices with filtering and pagination. Allows for creating, viewing, and editing devices.
*   **Data Source**: Interacts with `fetchDevices`, `createDevice`, and `updateDevice` in `src/lib/api.ts`.
*   **Components**: Uses a `DeviceTable` for displaying data and a `DeviceForm` in a dialog for creating/editing. `DeviceFilters` provides the search and filter UI.

### 4.3. Device Details (`/devices/[id]`)
*   **Purpose**: Shows detailed information for a single device, its scan history, and allows new scans to be initiated.
*   **Data Source**: `fetchDeviceById` provides the main data. It also triggers scans and fetches AI-powered remediation suggestions.
*   **Features**:
    *   Initiate a "Standard Scan".
    *   View results of completed scans, including AI-enhanced summaries.
    *   Generate remediation suggestions for specific vulnerabilities using Genkit.
    *   Generate PDF/CSV reports for a specific scan.

### 4.4. Scan History (`/scan-history`)
*   **Purpose**: A chronological log of all scans performed across all devices, with filtering capabilities.
*   **Data Source**: `fetchScanHistory` in `src/lib/api.ts`.

### 4.5. Test Console (`/test-console`)
*   **Purpose**: A development tool for simulating events and generating sample data without re-seeding the entire database.
*   **Functionality**: Triggers server actions in `src/app/test-console/actions.ts` to create scans with/without vulnerabilities, failed scans, and notifications.

---

## 5. Data Fetching and Supabase Integration

All interactions with the Supabase database are centralized in `src/lib/api.ts`. This file acts as a data access layer for the application.

### 5.1. Anti-Corruption Layer

The Supabase database schema uses `snake_case` for column names (e.g., `created_at`, `is_active`). However, the frontend components and logic use `camelCase` (e.g., `createdAt`, `isActive`).

To bridge this gap, `src/lib/api.ts` contains mapping functions (e.g., `mapDbDeviceToDevice`). These functions are responsible for converting data from the database format to the application's internal format upon fetching. This isolates the frontend from the specific database schema, making the code cleaner and easier to maintain.

### 5.2. Authentication

Authentication is managed by **Supabase Auth**. The project includes a login page (`/login`) and middleware (`/src/middleware.ts`) to handle user sessions.

For development purposes, the authentication checks in the middleware are currently **commented out**, allowing access to all pages without logging in. To re-enable authentication, uncomment the logic in `src/middleware.ts`.

---

## 6. AI Integration with Genkit

The application leverages **Google Genkit** for its generative AI capabilities. All AI-related code is located in the `src/ai/` directory.

*   **`src/ai/genkit.ts`**: Configures the Genkit instance, specifying the models to be used (e.g., `googleai/gemini-2.0-flash`).
*   **`src/ai/flows/`**: This directory contains the server-side AI "flows." Each flow is a self-contained function that performs a specific AI task, such as:
    *   `suggest-remediation-steps.ts`: Generates remediation advice for a given vulnerability.
    *   `enhance-scan-with-ai-analysis.ts`: Provides an executive summary and prioritized recommendations for a full scan report.
    *   `summarize-scan-findings.ts`: Creates a concise summary of scan results.

These flows are called from the API layer (`src/lib/api.ts`) and are invoked by components on pages like the Device Details page.

---

## 7. Styling and Theming

The application uses **Tailwind CSS** for utility-first styling. The configuration is in `tailwind.config.ts`.

Theming is managed through CSS variables defined in `src/app/globals.css`. This file contains two themes: `light` (default) and `dark`. Colors for primary actions, backgrounds, text, accents, and the sidebar are all defined here using HSL values.

The `ThemeProvider` in `src/app/layout.tsx` and the `ThemeToggle` component in `src/components/settings/ThemeToggle.tsx` work together to allow users to switch between light, dark, and system themes.

---

## 8. Deployment

The project is configured for deployment on **Firebase App Hosting**. The `apphosting.yaml` file at the root of the project contains the basic configuration, such as the maximum number of server instances.
