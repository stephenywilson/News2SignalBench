# Security Policy

## Scope

News2Signal Bench is a research benchmark and evaluation toolkit. It does not handle:

- Credentials or authentication tokens
- Live market data connections
- Trading execution
- User account data
- Personal information

## What NOT to include in contributions

- Do not include API keys, secrets, or tokens in any dataset or prediction file
- Do not submit private or proprietary news datasets in issues or pull requests
- Do not include personally identifiable information in any contributed file
- Do not add live data feeds, scraping scripts, or external service integrations

## Reporting a sensitive issue

This project is not a security scanner and does not process untrusted user input in production environments. However, if you discover a vulnerability in the package code itself (e.g., path traversal in file handling, unsafe deserialization), please report it by opening a private security advisory on GitHub rather than a public issue.

For general bugs or improvements, open a regular GitHub issue.

## Disclaimer

This project is provided for research and evaluation purposes only. It is not financial advice. It is not a trading tool. No warranty is provided.
