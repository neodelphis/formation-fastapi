# syntax=docker/dockerfile:1.6

# --------------------------------------------------------------- #
# Stage 1 : build de l'application Vite (TypeScript -> JS)
# --------------------------------------------------------------- #
FROM node:20-alpine AS builder

WORKDIR /build

# Copie des manifests de dépendances
COPY package.json ./
# Si package-lock.json ou yarn.lock existe, le copier aussi pour un build reproductible
COPY package-lock.json* ./

RUN npm install

# Copie du code source et build
COPY . .
RUN npm run build

# --------------------------------------------------------------- #
# Stage 2 : nginx sert les fichiers statiques
# --------------------------------------------------------------- #
FROM nginx:1.27-alpine AS runtime

# Copie de la config nginx (reverse proxy /api -> backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copie des fichiers buildés
COPY --from=builder /build/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
