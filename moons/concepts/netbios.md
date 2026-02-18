# NetBIOS

Network Basic Input/Output System. Legacy Windows name resolution.

## What it is
- Name resolution protocol predating DNS on local networks
- Windows-centric, used for SMB file sharing discovery
- NetBIOS over TCP/IP (NBT) still present in Windows networks
- Being phased out in favor of mDNS (Windows 10+ added mDNS support)

## Why Saturn rejected it
- **Windows-only**: no native support on macOS or Linux
- **Legacy**: actively being deprecated by Microsoft
- **Name resolution only**: no service metadata capability (no TXT record equivalent)
- **Security**: broadcast-based with no authentication, known attack surface

## Chapters
- Ch 2.1: rejected alternative
