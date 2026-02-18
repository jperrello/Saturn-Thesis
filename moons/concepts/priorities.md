# Priorities

Admin-controlled routing preference for Saturn services. Lower number = higher priority.

## How it works
- Each Saturn service registers with a `priority` value in its TXT record
- Clients discover all services, sort by priority, select lowest
- Admin sets priority per service in TOML config or LuCI web UI
- Enables policy-based routing without client-side configuration

## Use cases
- Prefer local models (Ollama, priority=1) over cloud (OpenRouter, priority=10)
- Failover: if priority-1 service is down, client auto-selects priority-10
- Institutional policy: IT sets priorities, users get best available automatically
- Design fiction example: Derek's Pi (low priority) vs ISP-injected service

## Comparison to DNS SRV priority
Saturn's priority field mirrors DNS SRV record priority semantics — familiar to network engineers, zero learning curve for IT admins.

## Chapters
- Ch 3.3: concept definition
- Ch 5.1: design fiction — "priority as policy"
