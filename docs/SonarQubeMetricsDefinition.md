# **Appendix of SonarQube Metrics Definition**
Link: https://docs.sonarsource.com/sonarqube-server/9.8/user-guide/metric-definitions

| Metric | Description |
|---|---|
| **🟨 Security** | Issues in this domain mark potential weaknesses to hackers. |
| Vulnerabilities | Number of vulnerabilities. |
| Security Rating | A–E rating based on the severity of detected vulnerabilities. |
| Remediation Effort | Estimated time required to fix all detected vulnerability issues. |
| **🟦 Reliability** | Issues in this domain mark code where behavior may differ from what was expected. |
| Bugs | Number of bugs. |
| Reliability Rating | Ordinal reliability ranking. |
| Remediation Effort | Estimated time required to fix all reliability issues or bugs. |
| **🟪 Maintainability** | Issues in this domain mark code that will be more difficult to update competently than it should. |
| Maintainability Rating | Ordinal maintainability ranking. |
| Code Smells | Number of code smells. |
| Debt | Estimated effort to fix all code smells. |
| Debt Ratio | Ratio between the estimated cost to fix maintainability issues and the estimated cost to develop the code. |
| **🟦 Security Review** | This domain represents potential security risks in the form of hotspots and their review status. |
| Security Hotspots | Number of security-sensitive code areas that need to be reviewed to determine whether they are safe or require a fix. |
| Security Review Rating | A–E rating based on the percentage of security hotspots that have been reviewed. |
| Hotspots Reviewed | Percentage of reviewed security hotspots compared to the total number of security hotspots. |
| **🟧 Coverage** | Measures how much of the code is covered by tests. |
| Lines to Cover | Number of lines of code that could be covered by unit tests. Blank lines or full comment lines are not counted. |
| Uncovered Lines | Number of lines or conditions that are not covered by unit tests. |
| Line Coverage | Percentage of lines executed during unit tests. |
| **🟪 Duplications** | Measures duplicated code in the codebase. |
| Density | Percentage of duplicated lines in the codebase. Formula: `duplicated_lines / lines_of_code * 100`. |
| Duplicated Lines | Number of lines involved in duplications. |
| Duplicated Blocks | Number of duplicated blocks of lines. |
| Duplicated Files | Number of files involved in duplications. |
| **🟦 Size** | Measures the size and structure of the codebase. |
| Lines of Code | Number of physical lines that contain at least one character and are not whitespace, tabs, or comments. |
| Lines | Number of physical lines. |
| Statements | Number of statements. |
| Functions | Number of functions. Depending on the language, a function may be defined as a function, method, or paragraph. |
| Classes | Number of classes, including nested classes, interfaces, enums, and annotations. |
| Files | Number of files. |
| Comment Lines | Number of lines containing comments or commented-out code. |
| Comments (%) | Comment line density. Formula: `comment_lines / (lines_of_code + comment_lines) * 100`. |
| **🟩 Complexity** | Measures how simple or complicated the control flow of the application is. |
| Cyclomatic Complexity / Complexity | Number of linearly independent paths through the code. Each function has a minimum complexity of 1, and the value increases when the control flow splits. |
| Cognitive Complexity | Measures how difficult the code’s control flow is to understand. |
| **🟥 Issues** | Counts issues by severity level. |
| Blocker Issues | Number of blocker severity issues. |
| Critical Issues | Number of critical severity issues. |
| Major Issues | Number of major severity issues. |
| Minor Issues | Number of minor severity issues. |