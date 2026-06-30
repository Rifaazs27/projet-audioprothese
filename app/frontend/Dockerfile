# syntax=docker/dockerfile:1
# --- Build de la SPA ---
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Service statique via nginx non-root ---
FROM nginxinc/nginx-unprivileged:1.31-alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
