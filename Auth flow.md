```mermaid
graph TD
A[Client Request] -->|Auth Token| B[Authenticator Middleware]
B -->|Validate Token| C[JWT Validation]
C -->|Valid?| D{Yes/No}
D -->|Yes| E[Proceed to Endpoint]
D -->|No| F[Return 401 Unauthorized]
