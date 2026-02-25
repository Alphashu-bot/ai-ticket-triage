# ---------- Stage: Build + Serve ----------
FROM node:20-alpine

WORKDIR /app

# Install dependencies (cached layer)
COPY package.json package-lock.json* ./
RUN npm install

# Copy source
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start Vite in dev mode with host binding
CMD ["npm", "run", "dev", "--", "--host"]
