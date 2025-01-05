# Stage 1: Build the Svelte app
FROM node:20-alpine AS svelte-build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./src ./src
COPY ./static ./static
COPY svelte.config.js vite.config.ts ./
RUN npm run build

# Stage 2: Set up the Python backend
FROM python:3.12-slim AS python-backend
WORKDIR /app
COPY ./kenyare/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./kenyare ./kenyare

# Copy the built Svelte app to the Python backend container
COPY --from=svelte-build /app/build /app/static

# Expose ports for both the Svelte frontend and the Python backend
EXPOSE 3000 8000

# Command to run both the Svelte frontend and the Python backend
CMD ["sh", "-c", "npm run preview & python kenyare/server.py"]

# Add a label for the image
LABEL name="kenyare-multi-stage" version="1.0"
