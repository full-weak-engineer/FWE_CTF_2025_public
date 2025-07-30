FROM golang:1.24.1-alpine3.21 AS builder
WORKDIR /app

COPY server.go .

RUN go build -o server server.go

FROM alpine:latest
WORKDIR /app
ARG FLAG
ENV FLAG=${FLAG}
COPY --from=builder /app/server .

CMD ["./server"]