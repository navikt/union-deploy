FROM golang:1.26 AS builder
RUN git clone --depth 1 https://github.com/flyteorg/flyte /src
WORKDIR /src/flytecopilot
RUN CGO_ENABLED=0 go build -o /flytecopilot ./main.go
FROM alpine:3.21
COPY --from=builder /flytecopilot /bin/flyte-copilot
ENTRYPOINT ["/bin/flyte-copilot"]
