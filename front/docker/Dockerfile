FROM node:12.6-alpine AS build
COPY . /app
WORKDIR /app
RUN npm install && npm run build

FROM alpine
WORKDIR /data
COPY --from=build /app/dist/ /data
