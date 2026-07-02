FROM node:22-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY index.html tsconfig.json ./
COPY src ./src
CMD ["pnpm", "run", "dev"]
