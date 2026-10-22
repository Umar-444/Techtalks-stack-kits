---
name: django-tailwind-theme
description: Configure, compile, and customize Tailwind CSS design tokens and dark mode for Django templates.
---

# Django Tailwind Theme Skill

## Purpose
Provides end-to-end guidance and scripts to set up Tailwind CSS in a Django 5 project, utilizing modern utility classes, responsive typography, and automated live compilation.

## Key Workflows
1. **Compiling Tailwind Styles**:
   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/dist/styles.css --minify
   ```
2. **Watch Mode for Local Development**:
   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/dist/styles.css --watch
   ```
3. **Template Token Usage**:
   - Primary Buttons: `px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white font-medium rounded-lg shadow-sm transition`
   - Form Inputs: `w-full px-3 py-2 border border-slate-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500`
   - Dark Mode Toggling: Manage `.dark` class on root `<html>` element via lightweight vanilla JavaScript.
