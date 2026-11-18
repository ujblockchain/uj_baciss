FROM node:22-slim

WORKDIR /app

# copy dependency manifests
COPY package*.json ./

# clean installation of dependencies
RUN npm install

# copy frontend source code
COPY . .

# next.js requires public api url at build time for client-side embedding
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# build optimized production bundle
RUN npm run build

EXPOSE 3000

ENV PORT=3000
ENV NODE_ENV=production

CMD ["npm", "start"]