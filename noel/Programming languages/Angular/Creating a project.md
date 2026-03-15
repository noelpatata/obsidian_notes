# Angular Project Setup Guide

This guide details how to create and run an Angular project from scratch.

## Prerequisites
- **Node.js**: Ensure you have Node.js installed (LTS recommended).
- **npm**: Usually comes with Node.js.

## Step 1: Install Angular CLI (Optional)
You can install the Angular CLI globally or use `npx` to run it without installation.
```bash
npm install -g @angular/cli
```

## Step 2: Create a New Project
Run the following command to generate a new Angular project.
```bash
npx @angular/cli@latest new directives-app --defaults --style css --routing false
```
- `--defaults`: Uses default settings (like strict mode).
- `--style css`: Sets the CSS preprocessor.
- `--routing false`: Skips routing module for simplicity.

## Step 3: Navigate to Project Directory
```bash
cd directives-app
```

## Step 4: Serve the Application
Start the development server.
```bash
npm start
# OR
npx ng serve
```
By default, the app will be available at `http://localhost:4200/`.

## Step 5: Explore the Structure
- `src/app/app.component.ts`: The main component logic.
- `src/app/app.component.html`: The main HTML template.
- `src/app/app.component.css`: Component-specific styles.